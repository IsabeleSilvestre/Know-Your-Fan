document.addEventListener("DOMContentLoaded", () => {
    fetch("http://localhost:8000/dashboard")
      .then(response => response.text())
      .then(html => {
        // Extrai apenas o conteúdo da <table> retornada pelo FastAPI (caso seja essa a rota)
        const temp = document.createElement('div');
        temp.innerHTML = html;
        const tableRows = temp.querySelectorAll("table tr");
        const tbody = document.querySelector("#userTable tbody");
  
        // Ignora o cabeçalho
        tableRows.forEach((row, index) => {
          if (index === 0) return;
          tbody.appendChild(row);
        });
      })
      .catch(error => {
        console.error("Erro ao carregar dashboard:", error);
      });
  });
  