from extract_text import extract_text_from_pdf
from structure_resume import structure_resume
from fraud_detection import generate_fraud_scorecard
from matching import structure_job_description, score_candidate_match, compute_overall_score

def process_one_resume(resume_path, structured_jd):
    raw_text = extract_text_from_pdf(resume_path)
    resume_data = structure_resume(raw_text)
    fraud_scorecard = generate_fraud_scorecard(resume_data)
    scores = score_candidate_match(resume_data, structured_jd)
    overall_score = compute_overall_score(scores)

    return {
        "candidate": resume_data["full_name"],
        "fraud_risk": fraud_scorecard["overall_risk"],
        "match_score": overall_score,
        "resume_data": resume_data,
        "fraud_scorecard": fraud_scorecard,
        "match_scores": scores
    }

def process_candidates(resume_paths, job_description_text):
    structured_jd = structure_job_description(job_description_text)
    results = [process_one_resume(path, structured_jd) for path in resume_paths]
    results.sort(key=lambda r: r["match_score"], reverse=True)
    return results


if __name__ == "__main__":
    sample_jd_text = """
    We're looking for a Backend Software Engineer to join our growing team.
    Requirements:
    - 3+ years of experience with Python
    - Strong knowledge of Flask or Django
    - Experience with AWS (EC2, Lambda, S3)
    - Familiarity with PostgreSQL or similar relational databases
    Nice to have:
    - Experience with Docker and containerization
    - Familiarity with CI/CD pipelines (Jenkins, GitHub Actions)
    """
    results = process_candidates(
        ["sample_resume_jordan_lee.pdf", "sample_resume_missing_phone_sam_ortiz.pdf"],
        sample_jd_text
    )
    for r in results:
        print(f"\n{r['candidate']} — {r['match_score']}")
        print(f"  Fraud risk: {r['fraud_risk']}")
        print(f"  Required skills: {r['match_scores']['required_skills_match']} ({r['match_scores']['required_skills_explanation']})")
        print(f"  Preferred skills: {r['match_scores']['preferred_skills_match']} ({r['match_scores']['preferred_skills_explanation']})")
        print(f"  Experience: {r['match_scores']['experience_match']} ({r['match_scores']['experience_explanation']})")
        print(f"  Keywords: {r['match_scores']['keyword_match']} ({r['match_scores']['keyword_explanation']})")