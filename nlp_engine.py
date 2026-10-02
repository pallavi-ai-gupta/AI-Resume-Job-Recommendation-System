import re


SKILLS = {
    "python", "java", "c", "c++", "javascript",
    "html", "css", "react", "node.js", "flask",
    "django", "sql", "mysql", "mongodb",
    "machine learning", "deep learning",
    "artificial intelligence",
    "nlp",
    "natural language processing",
    "tensorflow", "pytorch", "scikit-learn",
    "pandas", "numpy", "matplotlib", "keras",
    "data science", "data analysis",
    "power bi", "tableau",
    "aws", "azure", "gcp",
    "docker", "kubernetes",
    "git", "github", "linux",
    "spark", "hadoop",
    "opencv", "computer vision",
    "llm", "generative ai",
    "rag", "langchain"
}


def clean_text(text):

    return re.sub(
        r"\s+",
        " ",
        text.lower()
    ).strip()


def extract_skills(text):

    text = clean_text(text)

    found = []

    for skill in SKILLS:

        if skill.lower() in text:
            found.append(skill)

    return sorted(set(found))


def extract_email(text):

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return match.group(0) if match else "Not detected"


def extract_phone(text):

    match = re.search(
        r"\+?\d[\d\s-]{8,}\d",
        text
    )

    return match.group(0) if match else "Not detected"