
import json
import os
import requests


def analyze_resume_improvements(resume_data, job_description=""):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured on the server.")

    prompt = f"""
You are a professional resume improvement expert.

Analyze this resume:
{json.dumps(resume_data, indent=2)}

Target job description:
{job_description}

Return ONLY valid JSON in this format:
{{
  "priority_improvements": [],
  "section_suggestions": {{
    "summary": [],
    "skills": [],
    "education": [],
    "projects": [],
    "experience": [],
    "certifications": []
  }},
  "ats_improvements": [],
  "keyword_suggestions": [],
  "final_advice": []
}}

Rules:
- Give practical suggestions.
- Focus on ATS optimization.
- Do not invent experience or skills.
- Suggestions should be useful for a student applying for internships.
- Return JSON only.
"""

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-3.5-flash:generateContent"
    )

    response = requests.post(
        url,
        params={"key": api_key},
        json={
            "contents": [
                {"parts": [{"text": prompt}]}
            ],
            "generationConfig": {
                "responseMimeType": "application/json"
            }
        },
        timeout=60
    )

    response.raise_for_status()
    result = response.json()

    raw_response = (
        result["candidates"][0]["content"]["parts"][0]["text"].strip()
    )

    return json.loads(raw_response)
