import requests
import json


def analyze_resume_improvements(resume_data, job_description=""):

    prompt = f"""
You are a professional resume improvement expert.

Analyze this resume:

{json.dumps(resume_data, indent=2)}

Target job description:

{job_description}

Return ONLY valid JSON in exactly this format:

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
- Do not invent experience.
- Do not invent skills.
- Suggestions should be useful for a student applying for internships.
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

    raw_response = raw_response.replace("```json", "")
    raw_response = raw_response.replace("```", "")
    raw_response = raw_response.strip()

    return json.loads(raw_response)