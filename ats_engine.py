import re


def calculate_ats_score(text, skills):

    score = 0
    details = []

    text_lower = text.lower()

    # Skills
    if len(skills) >= 8:
        score += 30
        details.append("Good number of technical skills detected.")
    elif len(skills) >= 4:
        score += 20
        details.append("Moderate number of technical skills detected.")
    elif len(skills) > 0:
        score += 10
        details.append("Few technical skills detected.")
    else:
        details.append("No technical skills detected.")

    # Contact information
    email = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    phone = re.search(
        r"\+?\d[\d\s-]{8,}\d",
        text
    )

    if email:
        score += 10
        details.append("Email address detected.")
    else:
        details.append("Email address not detected.")

    if phone:
        score += 10
        details.append("Phone number detected.")
    else:
        details.append("Phone number not detected.")

    # Important sections
    sections = [
        "education",
        "experience",
        "projects",
        "skills",
        "certification"
    ]

    found_sections = sum(
        1 for section in sections
        if section in text_lower
    )

    score += found_sections * 6

    if found_sections >= 4:
        details.append("Resume contains most important sections.")
    else:
        details.append("Some important resume sections are missing.")

    # Resume length
    words = len(text.split())

    if words >= 250:
        score += 10
        details.append("Resume contains sufficient content.")
    elif words >= 100:
        score += 5
        details.append("Resume content is moderate.")
    else:
        details.append("Resume contains very little content.")

    score = min(score, 100)

    return score, details