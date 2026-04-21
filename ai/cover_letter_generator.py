# ai/cover_letter_generator.py

import os
import time
import random
from dotenv import load_dotenv
from openai import OpenAI
from ai.pdf_generator import generate_cover_letter_pdf  # your PDF generator

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Models and retry settings
PRIMARY_MODEL = "gpt-4o-mini"
SECONDARY_MODEL = "gpt-4o"
FREE_BACKUP_MODEL = "gpt-4o-mini"
MAX_RETRIES = 4
BASE_DELAY = 2


def run_completion(model, prompt):
    return client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=450,
        temperature=0.55
    )


def generate_cover_letter(job_description, resume_path=None, output_txt=None, model=None, user_name="Candidate"):
    """
    Generates a tailored cover letter (retry + fallback) and saves as .txt file.
    Returns the generated text.
    """

    prompt = f"""
Write a professional, ATS-friendly cover letter for the following job description:

{job_description}

Requirements:
- 3 short paragraphs
- Highlight skills from resume
- Max 200 words
- Address to Hiring Manager
- Close professionally
"""

    # Select model
    primary_model = model if model else PRIMARY_MODEL

    # --- Retry primary ---
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = run_completion(primary_model, prompt)
            cover_text = response.choices[0].message.content.strip()
            break
        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed: {e}")
            if "quota" in str(e).lower() or "429" in str(e):
                print("➡️ Switching to fallback model...")
                break
            time.sleep(BASE_DELAY * attempt + random.random())
    else:
        # --- Secondary Model ---
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = run_completion(SECONDARY_MODEL, prompt)
                cover_text = response.choices[0].message.content.strip()
                break
            except Exception as e:
                print(f"⚠️ Secondary attempt {attempt} failed: {e}")
                time.sleep(BASE_DELAY * attempt + random.random())
        else:
            # --- Free Backup ---
            print("🆓 Using FREE BACKUP MODEL or fallback text")
            try:
                response = run_completion(FREE_BACKUP_MODEL, prompt)
                cover_text = response.choices[0].message.content.strip()
            except Exception:
                # Fail-safe
                cover_text = f"""
Dear Hiring Manager,

I am writing to express my interest in this position. Although AI service failed,
I bring strong experience in automation testing, problem-solving, and quality delivery.

Sincerely,
{user_name}
                """.strip()

    # Save .txt
    if output_txt:
        os.makedirs(os.path.dirname(output_txt), exist_ok=True)
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(cover_text)

    return cover_text
