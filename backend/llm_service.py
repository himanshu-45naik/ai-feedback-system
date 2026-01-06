import os
import json
import re
from google import genai

client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

def extract_json(text: str):
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON found")
    return json.loads(match.group())


def analyze_review(rating: int, review: str):

    # This did not only provided Json output but also provided markdowns, explainations.
    #  therefore an extract_json was required to extract info in case of unnecessary info is also given.

    #     prompt = f"""
    # You are an AI assistant.

    # User rating: {rating}
    # User review: {review}

    # Return ONLY valid JSON with this exact schema:
    # {{
    #   "user_response": string,
    #   "summary": string,
    #   "actions": string
    # }}
    # """

    prompt = f"""
    You are a backend API.

    Respond ONLY with valid JSON.
    Do NOT include markdown.
    Do NOT include explanations.
    Do NOT include extra text.

    Schema:
    {{
    "user_response": string,
    "conclusion": string,
    "summary": string,
    "actions": string
    }}

    User rating: {rating}
    User review: {review}

    The schema's attribute must strictly follow these rules:
    - user_response : must have appropriate, polite reponse to the user based on the User review. Remember if the experience was bad, then let the user know that we will get back to you
    - conclusion : based on the User review, strictly categorize into Positive feedback or Negative Feedback or Constructive Feedback.
    - summary : must summarize the user review. Give bulleted points.
    - actions : Recommend appropriate and important actions that should be taken by the admin. Give numbered points.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        raw_text = response.text.strip()
        return extract_json(raw_text)

    except Exception as e:
        print("LLM ERROR:", e)
        return {
            "user_response": "Thanks for your feedback!",
            "conclusion": "System failed to conclude",
            "summary": "System failed to summarize.",
            "actions": "Manual review required."
        }
