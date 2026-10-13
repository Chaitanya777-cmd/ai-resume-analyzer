
import json
import os
import requests


def match_resume_with_job(resume_data, job_description):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured on the server.")

    prompt = f"""
You are an expert ATS and job matching system.

Compare the candidate's resume with the job description.

CANDIDATE RESUME:
{json.dumps(resume_data, indent=2)}

JOB DESCRIPTION:
{job_description}

Analyze:
1. Overall match percentage
2. Skills that match
3. Skills missing from the resume
4. Candidate strengths for this job
5. Candidate weaknesses for this job
6. Practical recommendations

Return ONLY valid JSON in this format:
{{
  "match_percentage": 0,
  "matching_skills": [],
  "missing_skills": [],
  "strengths": [],
  "weaknesses": [],
  "recommendations": []
}}

Rules:
- match_percentage must be an integer from 0 to 100.
- Do not invent skills or experience.
- Keep recommendations practical.
- Return JSON only.
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

    return json.loads(raw_response)
