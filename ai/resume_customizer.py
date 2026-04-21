# ai/resume_customizer.py

import os
import time
import random
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# MAIN + BACKUP MODELS
PRIMARY_MODEL = "gpt-4o-mini"
SECONDARY_MODEL = "gpt-4o"
FREE_BACKUP_MODEL = "gpt-4o-mini"

# Retry settings
MAX_RETRIES = 4
BASE_DELAY = 2  # seconds


def run_completion(model, prompt):
    """Helper to call the OpenAI API safely."""
    return client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=550,
        temperature=0.5
    )


def customize_resume(job_description, base_resume_text):
    """
    Generates a resume aligned to job description.
    Includes:
    - Retry logic (429, timeouts, server errors)
    - Fallback models
    """

    prompt = f"""
You are an ATS resume optimization engine.

JOB DESCRIPTION:
{job_description}

BASE RESUME:
{base_resume_text}

TASK:
1. Rewrite the resume specifically for the job.
2. Enhance professional summary.
3. Add missing relevant skills from the JD.
4. Keep it fully ATS-friendly (plain text only).
5. Maximum 500 words.
    """

    # Try primary model first
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = run_completion(PRIMARY_MODEL, prompt)
            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"⚠️ GPT Error (Primary Model, Attempt {attempt}): {e}")

            # If model exhausted/quota → break immediately
            if "insufficient_quota" in str(e).lower() or "rate limit" in str(e).lower():
                print("➡️ Moving to SECONDARY model...")
                break

            # retry with exponential backoff
            sleep_time = BASE_DELAY * attempt + random.uniform(0.2, 1.0)
            print(f"⏳ Retrying in {sleep_time:.1f}s...")
            time.sleep(sleep_time)

    # SECONDARY MODEL
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = run_completion(SECONDARY_MODEL, prompt)
            print("✅ SECONDARY MODEL SUCCESS")
            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"⚠️ GPT Error (Secondary, Attempt {attempt}): {e}")

            # same retry cooldown
            sleep_time = BASE_DELAY * attempt + random.uniform(0.2, 1.0)
            time.sleep(sleep_time)

    # FINAL FREE BACKUP — guarantee resume generation
    try:
        print("🆓 Using FREE BACKUP MODEL...")
        response = run_completion(FREE_BACKUP_MODEL, prompt)
        return response.choices[0].message.content.strip()

    except Exception:
        print("❌ All models failed. Returning safe fallback resume.")

        # Guaranteed fallback
        return f"""
PROFESSIONAL SUMMARY:
Experienced professional skilled in automation testing, problem-solving, and delivering 
quality solutions. Strong understanding of agile delivery, SDLC, and modern QA practices.

KEY SKILLS MATCHED:
- {', '.join(job_description.split()[:15])}

WORK EXPERIENCE:
Details unavailable due to API limit. Please retry with valid API quota.
        """.strip()
