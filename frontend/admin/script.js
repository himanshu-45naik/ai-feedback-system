const API_BASE = "http://localhost:8000";

async function loadReviews() {
  const tbody = document.getElementById("reviews");
  tbody.innerHTML = "";

  const res = await fetch(`${API_BASE}/admin/reviews`);
  const data = await res.json();

  data.forEach(r => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${r.rating}</td>
      <td>${r.review_text}</td>
      <td>${r.ai_summary}</td>
      <td>${r.ai_actions}</td>
    `;
    tbody.appendChild(row);
  });
}

loadReviews();
