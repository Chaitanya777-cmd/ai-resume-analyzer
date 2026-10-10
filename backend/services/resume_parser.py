import re


def parse_resume(text):
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    resume = {
        "name": "",
        "email": "",
        "phone": "",
        "skills": [],
        "education": [],
        "projects": [],
        "experience": [],
        "certifications": [],
        "achievements": []
    }

    # -------------------------
    # EMAIL
    # -------------------------
    email_match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    if email_match:
        resume["email"] = email_match.group(0)

    # -------------------------
    # PHONE
    # -------------------------
    phone_match = re.search(
        r'(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)',
        text
    )

    if phone_match:
        resume["phone"] = phone_match.group(0)

    # -------------------------
    # NAME
    # -------------------------
    if lines:
        first_line = lines[0]

        if (
            len(first_line.split()) <= 5
            and "@" not in first_line
            and not any(char.isdigit() for char in first_line)
        ):
            resume["name"] = first_line

    # -------------------------
    # SECTION KEYWORDS
    # -------------------------
    section_keywords = {
        "skills": [
            "skills",
            "technical skills",
            "skills & technologies",
            "technical skills and tools"
        ],

        "education": [
            "education",
            "educational background",
            "academic background"
        ],

        "projects": [
            "projects",
            "academic projects",
            "personal projects"
        ],

        "experience": [
            "experience",
            "work experience",
            "professional experience",
            "internship",
            "internships"
        ],

        "certifications": [
            "certifications",
            "certificates"
        ],

        "achievements": [
            "achievements",
            "awards",
            "accomplishments"
        ]
    }

    current_section = None

    # -------------------------
    # EXTRACT SECTIONS
    # -------------------------
    for line in lines:

        clean_line = line.lower().strip()

        found_section = None

        for section, keywords in section_keywords.items():

            if clean_line in keywords:
                found_section = section
                break

        if found_section:
            current_section = found_section
            continue

        if current_section:
            resume[current_section].append(line)

    return resume