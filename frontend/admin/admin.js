const API_BASE = "https://ai-feedback-system-ksy7.onrender.com";
// const API_BASE = "http://localhost:8000"; //local

async function loadReviews() {
  const tbody = document.getElementById("reviews");
  tbody.innerHTML = "";

  const statsDiv = document.getElementById("dashboard-stats");
  if (statsDiv) {
    updateStats(await getAllReviews());
  }

  const data = await getAllReviews();

  const conclusionFilter = document.getElementById("conclusion-filter").value;
  let filteredData = data;

  if (conclusionFilter === "positive"){
    filteredData = data.filter(r =>
      r.ai_conclusion && r.ai_conclusion.toLowerCase().includes("positive")
    );
  }

  if (conclusionFilter === "negative") {
    filteredData = data.filter(r =>
      r.ai_conclusion && r.ai_conclusion.toLowerCase().includes("negative")
    );
  }

  // Sorting Logic
  const sortFilter = document.getElementById("sort-filter").value;

  if (sortFilter === "asc") {
    filteredData.sort((a, b) => a.rating - b.rating);
  } else if (sortFilter === "desc") {
    filteredData.sort((a, b) => b.rating - a.rating);
  } else if (sortFilter === "latest") {
    filteredData.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    
  }

  filteredData.forEach(r => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${r.rating}</td>
      <td class="review-cell">${r.review_text || ""}</td>
      <td>${r.ai_conclusion || ""}</td>
      <td class="ai-cell">${formatText(r.ai_summary)}</td>
      <td class="ai-cell">${formatText(r.ai_actions)}</td>
    `;

    tbody.appendChild(row);
  });
}

async function getAllReviews() {
  const res = await fetch(`${API_BASE}/admin/reviews`);
  return await res.json();
}

function formatText(text) {
  if (!text) return "";

  return `
    <div class="ai-box">
      ${text
        .replace(/\n/g, "<br>")
        .replace(/- /g, "• ")
        .replace(/\d\. /g, "<br><strong>$&</strong>")
      }
    </div>
  `;
}

function updateStats(reviews) {
  let negative = 0;
  let positive = 0;
  let constructive = 0;
  let totalRating = 0;

  reviews.forEach(r => {
    const c = (r.ai_conclusion || "").toLowerCase();

    if (c.includes("negative")) negative++;
    else if (c.includes("constructive")) constructive++;
    else if (c.includes("positive")) positive++;

    totalRating += r.rating;
  });

  const avgRating = reviews.length
    ? (totalRating / reviews.length).toFixed(2)
    : 0;

  const statsDiv = document.getElementById("dashboard-stats");

  if (!statsDiv) return;

  statsDiv.innerHTML = `
    <strong>Total Reviews:</strong> ${reviews.length}<br>
    <strong>Negative:</strong> ${negative}<br>
    <strong>Constructive:</strong> ${constructive}<br>
    <strong>Positive:</strong> ${positive}<br>
    <strong>Average Rating:</strong> ${avgRating}
  `;
}

loadReviews();
