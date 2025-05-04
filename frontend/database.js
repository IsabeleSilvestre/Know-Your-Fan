document.addEventListener("DOMContentLoaded", () => {
  fetch("http://localhost:8000/dashboard")
    .then(response => response.json())
    .then(users => {
      const tbody = document.querySelector("#userTable tbody");
      tbody.innerHTML = "";

      users.forEach(user => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${user.name}</td>
          <td>${user.cpf}</td>
          <td>${user.email || "-"}</td>
          <td>${user.age ?? "-"}</td>
          <td>${user.interests ? user.interests.join(", ") : "-"}</td>
          <td>${user.social_links ? user.social_links.join(", ") : "-"}</td>
        `;

        tbody.appendChild(row);
      });

      document.getElementById("total-users").textContent = users.length;

      // Top Interesses
      const interestsCount = {};
      users.forEach(u => {
        u.interests?.forEach(interest => {
          interestsCount[interest] = (interestsCount[interest] || 0) + 1;
        });
      });
      const sortedInterests = Object.entries(interestsCount)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3);

      const interestsList = document.getElementById("top-interests");
      interestsList.innerHTML = "";
      sortedInterests.forEach(([interest, count]) => {
        const li = document.createElement("li");
        li.textContent = `${interest} (${count})`;
        interestsList.appendChild(li);
      });

      // Redes Sociais
      const socialConnected = users.reduce((acc, u) => acc + (u.social_links?.length || 0), 0);
      document.getElementById("social-connected").textContent = socialConnected;

      // Esportes Mais Assistidos
      const eventsCount = {};
      users.forEach(u => {
        u.esports_events?.forEach(ev => {
          eventsCount[ev] = (eventsCount[ev] || 0) + 1;
        });
      });
      const sortedEvents = Object.entries(eventsCount)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3);

      const eventsList = document.getElementById("top-events");
      eventsList.innerHTML = "";
      sortedEvents.forEach(([event, count]) => {
        const li = document.createElement("li");
        li.textContent = `${event} (${count})`;
        eventsList.appendChild(li);
      });

    })
    .catch(error => {
      console.error("Erro ao carregar dashboard:", error);
    });
});
