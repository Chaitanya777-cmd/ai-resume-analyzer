from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os


def generate_report(
    resume,
    ai_analysis,
    skill_gap=None,
    improvement_analysis=None
):

    file_path = "uploads/resume_analysis_report.pdf"

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]

    document = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    story = []

    # --------------------------------
    # TITLE
    # --------------------------------

    story.append(
        Paragraph(
            "AI Resume Analyzer Report",
            title_style
        )
    )

    story.append(Spacer(1, 20))

    # --------------------------------
    # CANDIDATE
    # --------------------------------

    story.append(
        Paragraph(
            "Candidate Information",
            heading_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Name:</b> {resume.get('name', 'N/A')}",
            normal_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Email:</b> {resume.get('email', 'N/A')}",
            normal_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Phone:</b> {resume.get('phone', 'N/A')}",
            normal_style
        )
    )

    story.append(Spacer(1, 15))

    # --------------------------------
    # AI SCORES
    # --------------------------------

    story.append(
        Paragraph(
            "Resume Scores",
            heading_style
        )
    )

    if ai_analysis:

        story.append(
            Paragraph(
                f"<b>Overall Score:</b> "
                f"{ai_analysis.get('overall_score', 'N/A')}/100",
                normal_style
            )
        )

        story.append(
            Paragraph(
                f"<b>ATS Score:</b> "
                f"{ai_analysis.get('ats_score', 'N/A')}/100",
                normal_style
            )
        )

    story.append(Spacer(1, 15))

    # --------------------------------
    # STRENGTHS
    # --------------------------------

    if ai_analysis:

        story.append(
            Paragraph(
                "Strengths",
                heading_style
            )
        )

        strengths = ai_analysis.get(
            "strengths",
            []
        )

        story.append(
            ListFlowable(
                [
                    ListItem(
                        Paragraph(
                            str(item),
                            normal_style
                        )
                    )
                    for item in strengths
                ],
                bulletType="bullet"
            )
        )

        story.append(Spacer(1, 15))

    # --------------------------------
    # WEAKNESSES
    # --------------------------------

    if ai_analysis:

        story.append(
            Paragraph(
                "Weaknesses",
                heading_style
            )
        )

        weaknesses = ai_analysis.get(
            "weaknesses",
            []
        )

        story.append(
            ListFlowable(
                [
                    ListItem(
                        Paragraph(
                            str(item),
                            normal_style
                        )
                    )
                    for item in weaknesses
                ],
                bulletType="bullet"
            )
        )

        story.append(Spacer(1, 15))

    # --------------------------------
    # SKILL GAP
    # --------------------------------

    if skill_gap:

        story.append(
            Paragraph(
                "Skill Gap Analysis",
                heading_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Skill Match:</b> "
                f"{skill_gap.get('match_percentage', 'N/A')}%",
                normal_style
            )
        )

        missing_skills = skill_gap.get(
            "missing_skills",
            []
        )

        if missing_skills:

            story.append(
                Paragraph(
                    "<b>Missing Skills:</b>",
                    normal_style
                )
            )

            story.append(
                ListFlowable(
                    [
                        ListItem(
                            Paragraph(
                                str(skill),
                                normal_style
                            )
                        )
                        for skill in missing_skills
                    ],
                    bulletType="bullet"
                )
            )

        story.append(Spacer(1, 15))

    # --------------------------------
    # IMPROVEMENTS
    # --------------------------------

    if improvement_analysis:

        story.append(
            Paragraph(
                "Resume Improvement Plan",
                heading_style
            )
        )

        improvements = improvement_analysis.get(
            "priority_improvements",
            []
        )

        story.append(
            ListFlowable(
                [
                    ListItem(
                        Paragraph(
                            str(item),
                            normal_style
                        )
                    )
                    for item in improvements
                ],
                bulletType="bullet"
            )
        )

        story.append(Spacer(1, 15))

        # ATS improvements

        story.append(
            Paragraph(
                "ATS Improvements",
                heading_style
            )
        )

        ats = improvement_analysis.get(
            "ats_improvements",
            []
        )

        story.append(
            ListFlowable(
                [
                    ListItem(
                        Paragraph(
                            str(item),
                            normal_style
                        )
                    )
                    for item in ats
                ],
                bulletType="bullet"
            )
        )

        story.append(Spacer(1, 15))

        # Final advice

        story.append(
            Paragraph(
                "Final Advice",
                heading_style
            )
        )

        advice = improvement_analysis.get(
            "final_advice",
            []
        )

        story.append(
            ListFlowable(
                [
                    ListItem(
                        Paragraph(
                            str(item),
                            normal_style
                        )
                    )
                    for item in advice
                ],
                bulletType="bullet"
            )
        )

    document.build(story)

    return file_path