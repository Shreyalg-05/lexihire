import re
from datetime import datetime


DATE_RANGE_RE = re.compile(
    r"(?P<start>\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?\s*\d{4})\s*[-–]\s*(?P<end>Present|\d{4})",
    re.I,
)

def parse_year(text: str):
    if not text:
        return None

    year_match = re.search(r"(19|20)\d{2}", text)
    if year_match:
        return int(year_match.group())

    return None

def calculate_total_experience(exp_json: list) -> float:
    """
    Calculates total years of experience.
    Safe for messy resumes.
    """

    total_years = 0.0
    current_year = datetime.now().year

    for job in exp_json:
        desc_text = " ".join(job.get("description", []))

        match = DATE_RANGE_RE.search(desc_text)
        if not match:
            continue

        start_year = parse_year(match.group("start"))
        end_text = match.group("end")

        if not start_year:
            continue

        if end_text.lower() == "present":
            end_year = current_year
        else:
            end_year = parse_year(end_text)

        if end_year and start_year:
            total_years += max(0, end_year - start_year)

    return round(total_years, 2)