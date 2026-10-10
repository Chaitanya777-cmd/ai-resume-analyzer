import json
import requests


def analyze_resume(resume_data):

    prompt = f"""
You are an expert AI Resume Analyzer.

Analyze the following resume data:

{json.dumps(resume_data, indent=2)}

Give a professional resume analysis.

Return ONLY valid JSON in exactly this format:

{{
    "overall_score": 0,
    "ats_score": 0,
    "strengths": [],
    "weaknesses": [],
    "missing_skills": [],
    "suggestions": []
}}

Rules:
- overall_score must be an integer from 0 to 100.
- ats_score must be an integer from 0 to 100.
- strengths must contain useful points from the resume.
- weaknesses must contain actual problems or missing areas.
- missing_skills should contain relevant skills that could improve the resume.
- suggestions should contain practical improvement suggestions.
- Do not include markdown.
- Return JSON only.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    result = response.json()

    raw_response = result["response"].strip()

    # Remove markdown code fences if the AI adds them
    raw_response = raw_response.replace("```json", "")
    raw_response = raw_response.replace("```", "")
    raw_response = raw_response.strip()

    # Convert AI JSON string into a Python dictionary
    analysis = json.loads(raw_response)

    return analysis