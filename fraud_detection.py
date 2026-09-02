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


if __name__ == "__main__":
    job_a = {"start_date": "June 2022", "end_date": None}
    job_b = {"start_date": "August 2019", "end_date": "May 2022"}
    job_c = {"start_date": "July 2018", "end_date": "August 2019"}

    print("A vs B:", jobs_overlap(job_a, job_b))
    print("B vs C:", jobs_overlap(job_b, job_c))