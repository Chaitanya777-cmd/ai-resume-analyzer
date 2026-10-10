import requests
import json


def match_resume_with_job(resume_data, job_description):

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

Return ONLY valid JSON.

Use exactly this format:

{{
    "match_score": 0,
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "recommendations": []
}}

match_score must be an integer from 0 to 100.
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

    # Remove markdown code fences if AI adds them
    raw_response = raw_response.replace("```json", "")
    raw_response = raw_response.replace("```", "")
    raw_response = raw_response.strip()

    analysis = json.loads(raw_response)

    return analysis