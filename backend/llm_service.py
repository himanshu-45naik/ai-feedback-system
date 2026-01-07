import os
import json
import re
from google import genai

client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

def extract_json(text: str):
    """Extract JSON from LLM response, handling markdown and extra text"""
    try:
        # Remove markdown code blocks
        text = text.strip()
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        
        # Find JSON object
        match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        
        if not match:
            raise ValueError("No JSON found in response")
        
        json_str = match.group().strip()
        return json.loads(json_str)
        
    except Exception as e:
        raise ValueError(f"Failed to extract JSON: {str(e)}")

def normalize_response(result: dict) -> dict:
    """Convert list fields to formatted strings
        - summary and actions: are given as list of bulleted points and numbered points respectively
        - conclusion: incase output is given as more positive, less positive,netc
        """
    
    # Handle summary - convert list to bullet points
    if isinstance(result.get('summary'), list):
        summary_lines = [line.strip().lstrip('•-*').strip() for line in result['summary'] if line.strip()]
        result['summary'] = '\n'.join([f"• {line}" for line in summary_lines])
    elif isinstance(result.get('summary'), str):
        if not result['summary'].strip().startswith('•'):
            lines = [line.strip() for line in result['summary'].split('\n') if line.strip()]
            result['summary'] = '\n'.join([f"• {line.lstrip('•-*').strip()}" for line in lines])
    
    # Handle actions - convert list to numbered points
    if isinstance(result.get('actions'), list):
        action_lines = [line.strip().lstrip('0123456789.-').strip() for line in result['actions'] if line.strip()]
        result['actions'] = '\n'.join([f"{i+1}. {line}" for i, line in enumerate(action_lines)])
    elif isinstance(result.get('actions'), str):
        if not result['actions'].strip()[0].isdigit():
            lines = [line.strip() for line in result['actions'].split('\n') if line.strip()]
            result['actions'] = '\n'.join([f"{i+1}. {line.lstrip('0123456789.-').strip()}" 
                                          for i, line in enumerate(lines)])
    
    # Normalize conclusion
    valid_conclusions = ["Positive Feedback", "Negative Feedback", "Constructive Feedback"]
    if result.get('conclusion') not in valid_conclusions:
        conclusion_lower = result['conclusion'].lower()
        if "positive" in conclusion_lower:
            result['conclusion'] = "Positive Feedback"
        elif "negative" in conclusion_lower:
            result['conclusion'] = "Negative Feedback"
        else:
            result['conclusion'] = "Constructive Feedback"
    
    return result

def analyze_review(rating: int, review: str):

    # ------------------This did not only provided Json output but also provided markdowns, explainations.--------------
    # ------------------therefore an extract_json was required to extract info in case of unnecessary info is also given.------------

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

    # ------------------ This prompt did not consistently provide the output as per the requirement, ------------------
    # ------------------at times the numbered points where not right, inner json structure was given ------------------
    # prompt = f"""
    # You are a backend API.

    # Respond ONLY with valid JSON.
    # Do NOT include markdown.
    # Do NOT include explanations.
    # Do NOT include extra text.

    # Schema:
    # {{
    # "user_response": string,
    # "conclusion": string,
    # "summary": string,
    # "actions": string
    # }}

    # User rating: {rating}
    # User review: {review}

    # The schema's attribute must strictly follow these rules:
    # - user_response : must have appropriate, polite reponse to the user based on the User review. Remember if the experience was bad, then let the user know that we will get back to you
    # - conclusion : based on the User review, strictly categorize into Positive feedback or Negative Feedback or Constructive Feedback.
    # - summary : must summarize the user review. Give bulleted points.
    # - actions : Recommend appropriate and important actions that should be taken by the admin. Give numbered points.
    # """

    prompt = f"""You are a customer feedback analysis API. Return ONLY a JSON object, nothing else.

    User Rating: {rating}/5
    User Review: {review}

    Return this EXACT JSON structure:
    {{
    "user_response": "<polite response to the user based on their feedback>",
    "conclusion": "<must be EXACTLY one of: 'Positive Feedback' OR 'Negative Feedback' OR 'Constructive Feedback'>",
    "summary": "<bullet points summarizing key points from the review>",
    "actions": "<numbered action items for the admin team>"
    }}

    RULES:
    1. user_response: Write a polite, empathetic response to the customer. If negative, acknowledge concerns and mention follow-up. If positive, thank them warmly. If neutral, thank them and note their feedback.

    2. conclusion: Choose EXACTLY ONE: Based user review categorize into 'Positive Feedback' OR 'Negative Feedback' OR 'Constructive Feedback'.

    3. summary: Provide 3-5 bullet points starting with "• " covering:
    - Overall sentiment
    - Specific issues or praise mentioned
    - Key details about product/service

    4. actions: Provide 3-5 numbered action items starting with "1. ", "2. ", etc. covering:
    - Immediate actions needed
    - Investigation steps
    - Follow-up recommendations
    - Quality improvement suggestions

    Return ONLY the JSON object. No markdown, no explanations, no extra text."""
    try:
        response = client.models.generate_content(
            model="gemma-3-27b-it",
            contents=prompt,
            config={
                "temperature": 0.1,
                "max_output_tokens": 1000,
                
            }
        )

        raw_text = response.candidates[0].content.parts[0].text.strip()
        result = extract_json(raw_text)
        
        # Validate required fields
        required_fields = ["user_response", "conclusion", "summary", "actions"]
        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing field: {field}")
        
        # Normalize the response 
        result = normalize_response(result)
        
        return result

        

    except Exception as e:
        print("LLM ERROR:", e)
        return {
            "user_response": "Thanks for your feedback!",
            "conclusion": "System failed to conclude",
            "summary": "System failed to summarize.",
            "actions": "Manual review required."
        }
