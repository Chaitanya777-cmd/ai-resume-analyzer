import re


def analyze_resume_quality(text, resume_data):
    """
    Analyze the quality and completeness of a resume.
    Returns a structured quality report.
    """

    text_lower = text.lower()

    score = 0
    max_score = 100

    strengths = []
    issues = []
    recommendations = []

    # --------------------------------------------------
    # 1. CONTACT INFORMATION
    # --------------------------------------------------

    contact_score = 0

    # Email
    if resume_data.get("email"):
        contact_score += 10
    else:
        issues.append("Email address is missing.")
        recommendations.append(
            "Add a professional email address to the resume."
        )

    # Phone
    phone_pattern = r"(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}"

    if re.search(phone_pattern, text):
        contact_score += 10
    else:
        issues.append("Phone number is missing.")
        recommendations.append(
            "Add a valid phone number to your resume."
        )

    # LinkedIn
    if "linkedin.com" in text_lower:
        contact_score += 5
    else:
        issues.append("LinkedIn profile is missing.")
        recommendations.append(
            "Add your LinkedIn profile URL."
        )

    # GitHub
    if "github.com" in text_lower:
        contact_score += 5
    else:
        recommendations.append(
            "Consider adding your GitHub profile if you have technical projects."
        )

    score += contact_score

    # --------------------------------------------------
    # 2. IMPORTANT SECTIONS
    # --------------------------------------------------

    sections = {
        "Education": ["education", "academic"],
        "Skills": ["skills", "technical skills"],
        "Projects": ["projects", "project"],
        "Experience": [
            "experience",
            "work experience",
            "internship"
        ],
        "Certifications": [
            "certifications",
            "certificates"
        ]
    }

    section_results = {}

    for section_name, keywords in sections.items():

        found = any(
            keyword in text_lower
            for keyword in keywords
        )

        section_results[section_name] = found

        if found:
            score += 8
            strengths.append(
                f"{section_name} section is present."
            )
        else:
            issues.append(
                f"{section_name} section is missing."
            )
            recommendations.append(
                f"Add a clear {section_name} section."
            )

    # --------------------------------------------------
    # 3. ACTION VERBS
    # --------------------------------------------------

    action_verbs = [
        "developed",
        "created",
        "built",
        "implemented",
        "designed",
        "developed",
        "optimized",
        "analyzed",
        "managed",
        "led",
        "automated",
        "engineered",
        "deployed",
        "improved",
        "integrated",
        "configured",
        "tested"
    ]

    action_verb_count = 0

    for verb in action_verbs:
        action_verb_count += text_lower.count(verb)

    if action_verb_count >= 5:

        score += 10

        strengths.append(
            "Resume uses strong action verbs."
        )

    elif action_verb_count >= 2:

        score += 5

        recommendations.append(
            "Use more strong action verbs such as developed, implemented, optimized and deployed."
        )

    else:

        issues.append(
            "Resume uses very few strong action verbs."
        )

        recommendations.append(
            "Start bullet points with strong action verbs."
        )

    # --------------------------------------------------
    # 4. QUANTIFIED ACHIEVEMENTS
    # --------------------------------------------------

    number_patterns = [
        r"\d+%",
        r"\d+\+",
        r"\d+\s*(users|projects|students|customers|records)",
        r"\$\d+",
        r"\d+\s*(days|months|years)"
    ]

    quantified_count = 0

    for pattern in number_patterns:

        matches = re.findall(
            pattern,
            text_lower
        )

        quantified_count += len(matches)

    if quantified_count >= 3:

        score += 10

        strengths.append(
            "Resume contains measurable achievements."
        )

    elif quantified_count >= 1:

        score += 5

        recommendations.append(
            "Add more numbers, percentages or measurable results."
        )

    else:

        issues.append(
            "Resume has very few measurable achievements."
        )

        recommendations.append(
            "Quantify achievements using numbers, percentages or measurable results."
        )

    # --------------------------------------------------
    # 5. PROJECT QUALITY
    # --------------------------------------------------

    projects = resume_data.get("projects", [])

    if len(projects) >= 2:

        score += 5

        strengths.append(
            "Resume contains multiple projects."
        )

    elif len(projects) == 1:

        score += 3

        recommendations.append(
            "Consider adding another relevant project."
        )

    else:

        issues.append(
            "No projects were detected."
        )

        recommendations.append(
            "Add 2–3 relevant academic or personal projects."
        )

    # --------------------------------------------------
    # 6. SKILLS
    # --------------------------------------------------

    skills = resume_data.get("skills", [])

    if len(skills) >= 5:

        score += 5

        strengths.append(
            "Resume contains a good number of technical skills."
        )

    elif len(skills) > 0:

        score += 3

        recommendations.append(
            "Add more relevant technical skills."
        )

    else:

        issues.append(
            "Technical skills were not detected."
        )

        recommendations.append(
            "Add a dedicated Technical Skills section."
        )

    # --------------------------------------------------
    # 7. LENGTH / CONTENT
    # --------------------------------------------------

    word_count = len(text.split())

    if 250 <= word_count <= 1000:

        score += 5

        strengths.append(
            "Resume has a reasonable amount of content."
        )

    elif word_count < 250:

        issues.append(
            "Resume appears too short."
        )

        recommendations.append(
            "Add relevant projects, achievements and experience."
        )

    else:

        recommendations.append(
            "Consider reducing unnecessary content and keeping the resume concise."
        )

    # --------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------

    score = min(score, max_score)

    # Remove duplicate recommendations
    recommendations = list(dict.fromkeys(recommendations))

    # Remove duplicate issues
    issues = list(dict.fromkeys(issues))

    # Remove duplicate strengths
    strengths = list(dict.fromkeys(strengths))

    return {
        "quality_score": score,

        "contact_information": {
            "email": bool(resume_data.get("email")),
            "phone": bool(
                re.search(
                    phone_pattern,
                    text
                )
            ),
            "linkedin": "linkedin.com" in text_lower,
            "github": "github.com" in text_lower
        },

        "sections": section_results,

        "content_quality": {
            "action_verbs": action_verb_count,
            "quantified_achievements": quantified_count,
            "word_count": word_count,
            "project_count": len(projects),
            "skill_count": len(skills)
        },

        "strengths": strengths,

        "issues": issues,

        "recommendations": recommendations
    }