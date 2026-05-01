from google import genai
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY")) 

GEMINI_MODEL = "gemini-2.5-flash-lite"

LEARNING_SYSTEM_PROMPT = """
You are an expert educational assistant helping students learn effectively.
Your job is to analyze learning materials and help students understand and retain information.

You can:
- Summarize documents and slides into clear, concise notes
- Generate flashcards in question/answer format
- Answer questions based on uploaded material
- Quiz students on topics they are studying
- Explain complex concepts in simple terms

Always:
- Be encouraging and supportive
- Keep explanations clear and structured
- Focus only on the provided learning material
- Ask clarifying questions if needed

Never:
- Make up information not found in the material
- Go off topic from the educational content
"""

async def generate_with_retry(contents, max_retries: int = 3, delay: int = 5):
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=contents,
                config={"system_instruction": LEARNING_SYSTEM_PROMPT}
            )
            return response.text
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                if attempt < max_retries - 1:
                    await asyncio.sleep(delay * (attempt + 1))  # 5s, 10s, 15s
                    continue
            raise e  # re-raise if it's a different error

    raise Exception("Gemini is currently unavailable. Please try again later.")