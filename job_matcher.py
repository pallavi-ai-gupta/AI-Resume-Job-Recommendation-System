import json


def load_jobs():

    with open(
        "jobs/jobs.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def calculate_match(
    resume_skills,
    job_skills
):

    resume = set(
        skill.lower()
        for skill in resume_skills
    )

    job = set(
        skill.lower()
        for skill in job_skills
    )

    matched = sorted(
        resume & job
    )

    missing = sorted(
        job - resume
    )

    score = round(
        (len(matched) / len(job)) * 100,
        2
    ) if job else 0

    return score, matched, missing


def recommend_jobs(resume_skills):

    results = []

    for job in load_jobs():

        score, matched, missing = calculate_match(
            resume_skills,
            job["skills"]
        )

        results.append({
            "title": job["title"],
            "score": score,
            "matched": matched,
            "missing": missing
        })

    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )