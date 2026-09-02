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
    job_d = {"start_date": "January 2021", "end_date": "December 2021"}
    job_e = {"start_date": "June 2021", "end_date": "May 2022"}
    sam_job_a = {"start_date": "January 2022", "end_date": None}
    sam_job_b = {"start_date": "June 2021", "end_date": "December 2021"}
    alex_job_a = {"start_date": "March 2021", "end_date": None}
    alex_job_b = {"start_date": "July 2019", "end_date": "February 2021"}


    print("A vs B:", jobs_overlap(job_a, job_b))
    print("B vs C:", jobs_overlap(job_b, job_c))
    print("D vs E:", jobs_overlap(job_d, job_e))
    print("Sam A vs B:", jobs_overlap(sam_job_a, sam_job_b))
    print("Alex A vs B:", jobs_overlap(alex_job_a, alex_job_b))