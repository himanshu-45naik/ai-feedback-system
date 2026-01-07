const API_BASE = "https://ai-feedback-system-ksy7.onrender.com";
//const API_BASE = "http://localhost:8000"; //local

async function submitReview() {
  const rating = document.getElementById("rating").value;
  const review = document.getElementById("review").value;
  const aiBox = document.getElementById("ai-response");
  const submitBtn = document.getElementById("submit-btn");


  if (!review.trim()) {
    alert("Please write a review before submitting.");
    return;
  }

 
  submitBtn.innerText = "Submitting...";
  submitBtn.disabled = true;
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

    if (!res.ok) throw new Error("Server error");

    const data = await res.json();

    // Enter "Submitted" State
    submitBtn.innerText = "Submitted!";
    submitBtn.classList.add("btn-success");

    // Display the AI response
    aiBox.innerText = data.ai_user_response;
    aiBox.style.display = "block";

    // Reset the button after a delay 
    setTimeout(() => {
      submitBtn.innerText = "Submit";
      submitBtn.disabled = false;
      submitBtn.classList.remove("btn-success");
      // Clear text area after submission
      document.getElementById("review").value = "";
    }, 4000);

  } catch (err) {
    // Error State
    console.error("Submission Error:", err);
    submitBtn.innerText = "Error! Try Again";
    submitBtn.disabled = false;
  }
}