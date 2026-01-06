const API_BASE = "http://localhost:8000";

async function submitReview() {
  const rating = document.getElementById("rating").value;
  const review = document.getElementById("review").value;
  const status = document.getElementById("status");
  const aiBox = document.getElementById("ai-response");

  status.innerText = "Submitting...";
  aiBox.style.display = "none";

  try {
    const res = await fetch(`${API_BASE}/submit-review`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        rating: Number(rating),
        review_text: review
      })
    });

    if (!res.ok) throw new Error("Failed");

    const data = await res.json();

    status.innerText = "Submitted successfully!";
    aiBox.innerText = data.ai_user_response;
    aiBox.style.display = "block";

  } catch (err) {
    status.innerText = "Error submitting review.";
  }
}
