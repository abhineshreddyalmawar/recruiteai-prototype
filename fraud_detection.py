import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

from datetime import datetime

def parse_date(date_str):
    if date_str is None:
        return datetime.max
    return datetime.strptime(date_str, "%B %Y")

def total_career_years(job_history):
    earliest_start = min(parse_date(job["start_date"]) for job in job_history)
    latest_end = max(
        datetime.now() if job["end_date"] is None else parse_date(job["end_date"])
        for job in job_history
    )
    return (latest_end - earliest_start).days / 365.25


def jobs_overlap(job_a, job_b):
    a_start = parse_date(job_a["start_date"])
    a_end = parse_date(job_a["end_date"])
    b_start = parse_date(job_b["start_date"])
    b_end = parse_date(job_b["end_date"])

    return a_start < b_end and b_start < a_end

def check_all_overlaps(job_history):
    overlapping_pairs = []
    for i in range(len(job_history)):
        for j in range(i + 1, len(job_history)):
            if jobs_overlap(job_history[i], job_history[j]):
                overlapping_pairs.append((job_history[i], job_history[j]))
    return overlapping_pairs

tech_stack_tool = {
    "name": "check_tech_stack_plausibility",
    "description": "Check whether claimed technologies are plausible given job dates and career duration.",
    "input_schema": {
        "type": "object",
        "properties": {
            "flags": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "skill": {"type": "string"},
                        "issue_type": {
                            "type": "string",
                            "enum": ["technology_predates_release", "implausible_duration"]
                        },
                        "explanation": {"type": "string"},
                        "confidence": {
                            "type": "string",
                            "enum": ["high", "medium", "low"]
                        }
                    },
                    "required": ["skill", "issue_type", "explanation", "confidence"]
                }
            }
        },
        "required": ["flags"]
    }
}

def check_tech_stack_plausibility(skills, job_history, summary, career_years):
    prompt = f"""Given this candidate's claimed skills, summary, and job history, identify any implausible claims.

Skills: {skills}
Summary: {summary}
Job History: {job_history}
Total career span (already calculated): {career_years:.1f} years

Check for:
1. A technology claimed that didn't exist yet at the time of a job (technology_predates_release)
2. A claimed duration in the summary or skills that EXCEEDS {career_years:.1f} years (implausible_duration) — only flag OVERSTATED experience, never understated experience.

Only flag genuine issues. If everything is plausible, return an empty flags list."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        tools=[tech_stack_tool],
        tool_choice={"type": "tool", "name": "check_tech_stack_plausibility"},
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].input


if __name__ == "__main__":
    jordan_jobs = [
        {"title": "Senior Software Engineer", "employer": "Brightpath Systems", "start_date": "June 2022", "end_date": None},
        {"title": "Software Engineer", "employer": "Alden Data Co.", "start_date": "August 2019", "end_date": "May 2022"},
        {"title": "Junior Developer", "employer": "Alden Data Co.", "start_date": "July 2018", "end_date": "August 2019"}
    ]
    print("Jordan overlaps (expect []):", check_all_overlaps(jordan_jobs))

    test_history_with_overlap = [
        {"title": "Role 1", "employer": "Company X", "start_date": "January 2020", "end_date": "December 2020"},
        {"title": "Role 2", "employer": "Company Y", "start_date": "June 2020", "end_date": "May 2021"},
        {"title": "Role 3", "employer": "Company Z", "start_date": "June 2021", "end_date": None}
    ]
    print("Test overlaps (expect 1 pair, Role 1 vs Role 2):", check_all_overlaps(test_history_with_overlap))

    single_job_history = [
        {"title": "Only Role", "employer": "Company Q", "start_date": "January 2022", "end_date": None}
    ]
    print("Single job overlaps (expect []):", check_all_overlaps(single_job_history))

    double_overlap_history = [
        {"title": "Role A", "employer": "Company 1", "start_date": "January 2020", "end_date": "December 2020"},
        {"title": "Role B", "employer": "Company 2", "start_date": "September 2020", "end_date": "August 2021"},
        {"title": "Role C", "employer": "Company 3", "start_date": "June 2021", "end_date": None}
    ]
    print("Double overlap (expect 2 pairs, A-B and B-C):", check_all_overlaps(double_overlap_history))   

    print("\nJordan tech stack check (expect []):")
    print(check_tech_stack_plausibility(
        skills=["Python", "Java", "Flask", "Spring Boot", "AWS (Lambda, EC2, S3)", "Docker", "Jenkins", "PostgreSQL", "REST APIs", "Git", "Selenium", "pytest"],
        job_history=jordan_jobs,
        summary="Backend-focused software engineer with 5 years of experience building REST APIs and cloud-deployed services. Comfortable across Python, Java, and AWS infrastructure.",
        career_years=total_career_years(jordan_jobs)
    ))

    print("\nSuspicious tech stack check (expect implausible_duration, high confidence):")
    suspicious_jobs = [
        {"title": "Software Engineer", "employer": "StartupCo", "start_date": "January 2024", "end_date": None}
    ]
    print(check_tech_stack_plausibility(
        skills=["Python"],
        job_history=suspicious_jobs,
        summary="Software engineer with 10 years of experience in Python development.",
        career_years=total_career_years(suspicious_jobs)
    ))

    print("\nRelease-date check, well-known tech (expect technology_predates_release):")
    old_tech_jobs = [
        {"title": "Software Engineer", "employer": "Old Corp", "start_date": "January 2010", "end_date": "December 2012"}
    ]
    print(check_tech_stack_plausibility(
        skills=["Kubernetes"],
        job_history=old_tech_jobs,
        summary="Software engineer with experience in container orchestration.",
        career_years=total_career_years(old_tech_jobs)
    ))

    print("\nRelease-date check, lesser-known tech (expect technology_predates_release; confidence field known to be unverified/self-reported, not calibrated):")
    obscure_tech_jobs = [
        {"title": "Backend Developer", "employer": "Legacy Systems Inc", "start_date": "January 2019", "end_date": "December 2021"}
    ]
    print(check_tech_stack_plausibility(
        skills=["Bun"],
        job_history=obscure_tech_jobs,
        summary="Backend developer with experience in modern JavaScript tooling.",
        career_years=total_career_years(obscure_tech_jobs)
    ))