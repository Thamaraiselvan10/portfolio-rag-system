import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
def generate_answer(query, context):
    prompt = f"""
You are a financial assistant.

Answer the question using ONLY the provided context.
Do NOT make up numbers.
If the answer is not in the context, say "Insufficient data".

Context:
{context}

Question:
{query}

Answer:
"""

    response = client.models.generate_content(
    model="models/gemini-2.5-flash",
    contents=prompt
)

    return response.text