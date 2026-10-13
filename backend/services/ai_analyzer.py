
import json
import os
import requests


def analyze_resume(resume_data):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured on the server.")

    prompt = f"""
You are an expert AI Resume Analyzer.

Analyze this resume data:
{json.dumps(resume_data, indent=2)}

Return ONLY valid JSON in this exact format:
{{
  "overall_score": 0,
  "ats_score": 0,
  "strengths": [],
  "weaknesses": [],
  "missing_skills": [],
  "suggestions": []
}}

Rules:
- overall_score and ats_score must be integers from 0 to 100.
- strengths, weaknesses, missing_skills, suggestions must be arrays of strings.
- Return valid JSON only, without Markdown.
"""

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-2.5-flash:generateContent"
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

    analysis = json.loads(raw_response)

    return analysis
