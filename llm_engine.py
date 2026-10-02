import ollama


def analyze_resume(
    text,
    skills,
    recommendations
):

    top_jobs = "\n".join(
        f"{job['title']}: {job['score']}%"
        for job in recommendations[:3]
    )

    prompt = f"""
You are an AI career assistant.

Analyze this resume.

Resume:
{text[:6000]}

Detected Skills:
{", ".join(skills)}

Top Job Matches:
{top_jobs}

Give the following:

1. Resume Summary
2. Main Strengths
3. Missing or Recommended Skills
4. Suitable Career Directions
5. Resume Improvement Suggestions

Keep the response professional,
clear and useful for a student.
"""

    try:

        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response[
            "message"
        ]["content"]

    except Exception:

        return (
            "LLM analysis unavailable. "
            "Please make sure Ollama is running "
            "and llama3.2:3b is installed."
        )