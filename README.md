# Know Your Fan - Dashboard

📌 Visão Geral
Este projeto é um dashboard interativo para análise de usuários, fornecendo métricas essenciais sobre distribuição de idade, interesses, esportes assistidos, redes sociais conectadas e validação de documentos.

O sistema foi projetado para ter um design moderno, inspirado no estilo FURIA, com uma paleta de cores escura e roxa, garantindo um layout impactante e competitivo.

## **🚀 Tecnologias Utilizadas**
Front-end: HTML, CSS e JavaScript

Gráficos: Chart.js

Estilo: CSS personalizado com animações e responsividade

Dados: Mock JSON (pode ser integrado a um banco de dados real)

## **📂 Estrutura do Projeto**
```bash
📂 KnowYourFan
│── 📂 backend/         # Código do servidor e lógica da aplicação
│   ├── main.py        # Arquivo principal do backend
│── 📂 frontend/        # Interface do dashboard
│   ├── index.html     # Página principal do dashboard
│   ├── scripts.js     # Código JavaScript para interatividade
│   ├── style.css      # Arquivo CSS para estilização
│── 📂 venv/            # Ambiente virtual do Python
│── 📂 image/           # Imagens utilizadas no projeto
│── 📜 README.md        # Documentação do projeto
```

## **🎨 Design**
Paleta de Cores: Preto, roxo e violeta

Tipografia: 'Segoe UI', garantindo legibilidade e modernidade

Animações: Hover suave nos cards para melhor experiência

Filtros Interativos: Seleção dinâmica de dados em um dropdown estilizado

## **📊 Funcionalidades**
```
✅ Total de Usuários → Exibe o número total de usuários cadastrados 
✅ Distribuição por Idade → Gráfico que mostra a quantidade de usuários por faixa etária 
✅ Top Interesses → Lista os interesses mais populares entre os usuários 
✅ Esportes Mais Assistidos → Gráfico de preferência esportiva dos usuários 
✅ Redes Sociais Conectadas → Quantidade de usuários que conectaram redes sociais 
✅ Documentos Validados e Pendentes → Exibe números de usuários com documentação validada
```
## **🔎 Como Funciona?**

1️⃣ Instalação
Para rodar o dashboard, basta abrir index.html em um navegador compatível (Chrome, Edge, Firefox).

Se quiser rodar localmente com um servidor:

```sh npx serve .```

2️⃣ Uso
Filtros Interativos → Selecione quais dados quer visualizar no dropdown.

Gráficos Dinâmicos → Os dados são atualizados instantaneamente conforme os filtros são aplicados.

Visualização Completa → Interface moderna e otimizada para diferentes dispositivos.

## **🛠 Possíveis Melhorias**
```
🔹 Integração com Banco de Dados → Usar uma API real para puxar informações. 
🔹 Autenticação de Usuário → Criar um sistema de login para análises personalizadas. 
🔹 Exportação de Relatórios → Permitir baixar gráficos e tabelas em PDF ou CSV.
```
## **📜 Licença**
Este projeto está sob a licença MIT, permitindo uso livre com atribuição.
