import re


# Common technical skills
KNOWN_SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "sql",
    "html",
    "css",
    "react",
    "angular",
    "vue",
    "node.js",
    "nodejs",
    "express",
    "fastapi",
    "flask",
    "django",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "natural language processing",
    "nlp",
    "computer vision",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "power bi",
    "tableau",
    "excel",
    "mongodb",
    "mysql",
    "postgresql",
    "redis",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "google cloud",
    "git",
    "github",
    "linux",
    "rest api",
    "rest apis",
    "graphql",
    "spark",
    "hadoop",
]


def extract_skills(text):
    """
    Extract known technical skills from text.
    """

    text_lower = text.lower()

    found_skills = []

    for skill in KNOWN_SKILLS:

        # Escape special characters like + and .
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text_lower):

            # Normalize duplicate names
            if skill == "nodejs":
                normalized_skill = "Node.js"

            elif skill == "nlp":
                normalized_skill = "Natural Language Processing"

            elif skill == "rest apis":
                normalized_skill = "REST API"

            else:
                normalized_skill = skill.title()

            if normalized_skill not in found_skills:
                found_skills.append(normalized_skill)

    return found_skills


def analyze_skill_gap(resume_text, job_description):
    """
    Compare resume skills with skills required by a job description.
    """

    resume_skills = extract_skills(resume_text)

    required_skills = extract_skills(job_description)

    resume_skill_set = {
        skill.lower()
        for skill in resume_skills
    }

    required_skill_set = {
        skill.lower()
        for skill in required_skills
    }

    matched_skills = []

    missing_skills = []

    for skill in required_skills:

        if skill.lower() in resume_skill_set:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    # Calculate match percentage
    if len(required_skills) > 0:

        match_percentage = round(
            (len(matched_skills) / len(required_skills)) * 100
        )

    else:

        match_percentage = 0

    return {
        "match_percentage": match_percentage,

        "resume_skills": resume_skills,

        "required_skills": required_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "skill_gap_count": len(missing_skills)
    }