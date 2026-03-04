# engine/education_parser.py

import re


DEGREE_PATTERN = re.compile(
    r"\b("
    r"bachelor|master|ph\.?d|doctorate|"
    r"b\.?tech|m\.?tech|"
    r"b\.?e|m\.?e|"
    r"bca|mca|"
    r"bsc|msc|"
    r"mba|"
    r"associate"
    r")\b",
    re.I,
)

INSTITUTE_PATTERN = re.compile(
    r"\b(university|college|institute|school|academy)\b",
    re.I,
)

YEAR_PATTERN = re.compile(r"(20\d{2})\s*[-–]\s*(20\d{2})")

GPA_PATTERN = re.compile(r"\b(CGPA|GPA|Percentage)[:\s]*([0-9.]+)", re.I)


def parse_education_block(text: str):
    """
    ATS-style education parser (pattern + context based)
    """
    if not text:
        return []

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    entries = []
    current = {}

    for line in lines:
        lower = line.lower()

        # 🎓 DEGREE DETECTION (pattern-based, not hardcoded list)
        if DEGREE_PATTERN.search(line):
            if current:
                entries.append(current)
                current = {}
            current["degree"] = line
            continue

        # 🏫 INSTITUTION
        if INSTITUTE_PATTERN.search(line):
            current["institution"] = line
            continue

        # 📅 YEAR RANGE
        year_match = YEAR_PATTERN.search(line)
        if year_match:
            current["start_year"] = int(year_match.group(1))
            current["end_year"] = int(year_match.group(2))
            continue

        # 📊 GPA
        gpa_match = GPA_PATTERN.search(line)
        if gpa_match:
            current["gpa"] = gpa_match.group(2)
            continue

    if current:
        entries.append(current)

    return entries