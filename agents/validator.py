from groq import Groq
from dotenv import load_dotenv
import os
import logging
import json
import re

# ---------------- LOAD ENV ---------------- #

load_dotenv()

logging.basicConfig(level=logging.INFO)

# ---------------- GROQ CLIENT ---------------- #

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------- ANALYZE DEAL ---------------- #

def analyze_deal(content):

    try:

        content = content[:6000]

        prompt = f"""
You are an advanced ecommerce deal intelligence AI.

Analyze the ecommerce webpage content.

IMPORTANT:
Return ONLY valid JSON.
Do NOT return markdown.
Do NOT return explanations.
Do NOT return extra text.

If multiple products exist,
analyze the BEST deal available.

Return JSON in this exact format:

{{
  "product_name": "",
  "original_price": "",
  "discounted_price": "",
  "estimated_discount_percentage": 0,
  "deal_quality_rating": "",
  "trust_score": 0,
  "suspicious": false,
  "reasons": "",
  "pros": "",
  "cons": "",
  "final_verdict": "",
  "summary": ""
}}

Webpage Content:
{content}
"""

        logging.info("Sending request to Groq...")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = response.choices[0].message.content

        # ---------------- CLEAN RESPONSE ---------------- #

        result = result.strip()

        # Remove markdown json blocks if present
        result = result.replace("```json", "")
        result = result.replace("```", "")

        # Extract only JSON object
        match = re.search(r"\{.*\}", result, re.DOTALL)

        if match:
            result = match.group(0)

        # Convert to Python dictionary
        parsed_json = json.loads(result)

        logging.info("Analysis completed successfully.")

        return parsed_json

    except Exception as e:

        logging.error(str(e))

        return {
            "error": str(e)
        }