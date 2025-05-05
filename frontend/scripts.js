document.addEventListener("DOMContentLoaded", async () => {
  try {
      const response = await fetch("http://localhost:8000/dashboard");
      const users = await response.json();

      document.getElementById("total-users").textContent = users.length;

      const validatedDocs = users.filter(u => u.documents_validated).length;
      const pendingDocs = users.length - validatedDocs;

      document.getElementById("validated-docs").textContent = validatedDocs;
      document.getElementById("pending-docs").textContent = pendingDocs;

      const countOccurrences = array => Object.entries(array.reduce((acc, item) => {
          acc[item] = (acc[item] || 0) + 1;
          return acc;
      }, {})).sort((a, b) => b[1] - a[1]).slice(0, 5);

      // Gráficos iniciais
      const sortedInterests = countOccurrences(users.flatMap(u => u.interests ?? []));
      const interestsChart = new Chart(document.getElementById("interestsChart"), {
          type: 'bar',
          data: {
              labels: sortedInterests.map(i => i[0]),
              datasets: [{
                  label: "Interesses Populares",
                  data: sortedInterests.map(i => i[1]),
                  backgroundColor: 'rgba(255, 99, 132, 0.6)',
                  borderColor: '#ff6384',
                  borderWidth: 1
              }]
          }
      });

      document.getElementById("social-connected").textContent = users.reduce((acc, u) => acc + (u.social_links?.length || 0), 0);

      // Atualiza filtros instantaneamente
      document.querySelectorAll(".dropdown-content input").forEach(filter => {
          filter.addEventListener("change", () => {
              const selectedFilters = Array.from(document.querySelectorAll(".dropdown-content input:checked")).map(f => f.value);
              
              const filteredUsers = users.filter(user => {
                  return selectedFilters.some(filter => user[filter]);
              });

              // Atualizar gráficos conforme filtros
              const filteredInterests = countOccurrences(filteredUsers.flatMap(u => u.interests ?? []));
              interestsChart.data.labels = filteredInterests.map(i => i[0]);
              interestsChart.data.datasets[0].data = filteredInterests.map(i => i[1]);
              interestsChart.update();
              
              document.getElementById("total-users").textContent = filteredUsers.length;
          });
      });

  } catch (error) {
      console.error("Erro ao carregar dashboard:", error);
  }
});
