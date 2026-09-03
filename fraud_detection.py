from datetime import datetime

def parse_date(date_str):
    if date_str is None:
        return datetime.max
    return datetime.strptime(date_str, "%B %Y")


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