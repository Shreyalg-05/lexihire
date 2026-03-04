import re
from datetime import datetime

MONTH_MAP = {
    m.lower(): i for i, m in enumerate(
        ["Jan","Feb","Mar","Apr","May","Jun",
         "Jul","Aug","Sep","Oct","Nov","Dec"], start=1
    )
}


def parse_date_safe(text: str):
    text = text.strip()

    if re.search(r"present|current", text, re.I):
        return datetime.today()

    # try Month Year
    m = re.search(r"([A-Za-z]{3,})\s*(\d{4})", text)
    if m:
        month = MONTH_MAP.get(m.group(1)[:3].lower(), 1)
        year = int(m.group(2))
        return datetime(year, month, 1)

    # try year only
    y = re.search(r"\b(19|20)\d{2}\b", text)
    if y:
        return datetime(int(y.group()), 1, 1)

    return None
def months_between(start, end):
    if not start or not end:
        return 0
    return (end.year - start.year) * 12 + (end.month - start.month)
def format_duration(months: int) -> str:
    years = months // 12
    rem = months % 12
    parts = []
    if years:
        parts.append(f"{years} yr{'s' if years>1 else ''}")
    if rem:
        parts.append(f"{rem} mo{'s' if rem>1 else ''}")
    return " ".join(parts) if parts else "0 mo"
DATE_RANGE_RE = re.compile(
    r"""
    (?P<start>
        (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{4}
        |
        \d{4}
    )
    \s*[-–to]+\s*
    (?P<end>
        Present|Current|
        (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{4}
        |
        \d{4}
    )
    """,
    re.I | re.X,
)

ROLE_LABEL_RE = re.compile(
    r"^(?:Role|Position|Title)\s*:\s*(.+)$",
    re.I,
)

COMPANY_RE = re.compile(
    r"\b(pvt|ltd|llp|inc|technologies|solutions|systems|soft|labs|corp)\b",
    re.I,
)
EXPLICIT_COMPANY_RE = re.compile(
    r"^(?:Client|Company|Employer|Organization)\s*:\s*(.+)$",
    re.I,
)
TECH_RE = re.compile(
    r"^(?:Technologies|Technology Stack|Tech Stack)\s*:\s*(.+)",
    re.I,
)
FIELD_HEADER_RE = re.compile(
    r"^(role|position|title|technologies?|technology stack|tech stack)\s*:",
    re.I,
)

def clean_field(text: str) -> str:
    return text.strip().rstrip(",;:.")
def split_tech_stack(tech_text: str) -> list:
    tech_text = tech_text.strip()

    # -------------------------------------------------
    # STEP 0 — remove trailing sentence punctuation
    # (generic, not hardcoded)
    # -------------------------------------------------
    tech_text = tech_text.rstrip(" .;:")
    tech_text = re.sub(r"\s+", " ", tech_text)

    # -------------------------------------------------
    # STEP 1 — remove leading wrapper like:
    # ANYWORDS ( ... )
    # -------------------------------------------------
    first_paren = tech_text.find("(")
    last_paren = tech_text.rfind(")")

    if first_paren != -1 and last_paren != -1 and last_paren > first_paren:
        prefix = tech_text[:first_paren]

        # if prefix looks like a wrapper label (not a tech)
        if len(prefix.split()) <= 3:
            tech_text = tech_text[first_paren + 1:last_paren]

    # -------------------------------------------------
    # STEP 2 — split on commas NOT inside parentheses
    # -------------------------------------------------
    parts = re.split(r",(?![^()]*\))", tech_text)

    cleaned = []
    for p in parts:
        item = p.strip()
        item = item.strip(" ,;")

        if item:
            cleaned.append(item)

    return cleaned

def looks_like_new_experience_block(line: str) -> bool:
    """
    Production-safe new experience detector.
    Prevents false positives.
    """

    text = line.strip()
    lower = text.lower()

    # 🚫 never trigger on field labels
    if FIELD_HEADER_RE.match(text):
        return False

    # ✅ explicit company label (strongest)
    if COMPANY_RE.search(text):
        return True

    # 🚫 very short lines are rarely companies
    words = text.split()
    if len(words) <= 2:
        return False

    # 🚫 lines ending with colon are headers
    if text.endswith(":"):
        return False

    # ✅ role + company pattern
    if ROLE_LABEL_RE.search(lower) and COMPANY_RE.search(lower):
        return True

    # ✅ company-style heuristic (tightened)
    if (
        2 <= len(words) <= 7
        and COMPANY_RE.search(lower)
    ):
        return True

    return False
def split_experience_blocks(exp_lines: list) -> list:
    """
    Split experience section into job blocks
    using strong anchors only.
    """
    blocks = []
    current = []

    for line in exp_lines:
        text = line.strip()

        # strong anchor only
        if re.match(r"^(Client|Company)\s*:", text, re.I):
            if current:
                blocks.append(current)
            current = [text]
        else:
            if current:
                current.append(text)

    if current:
        blocks.append(current)

    return blocks
def extract_experience_json(sections: dict) -> list:
    exp_lines = sections.get("experience", [])
    if not exp_lines:
        return []

    blocks = split_experience_blocks(exp_lines)
    experiences = []

    for block in blocks:
        current = {
            "company": None,
            "role": None,
            "technologies": [],
            "description": [],
            "start_date": None,
            "end_date": None,
            "duration_months": 0,
            "duration_text": None,
        }

        for line in block:
            text = line.strip()

            # company
            comp_match = re.match(r"^(?:Client|Company)\s*:\s*(.+)", text, re.I)
            if comp_match:
                current["company"] = clean_field(comp_match.group(1))
                continue

            # role
            role_match = ROLE_LABEL_RE.match(text)
            if role_match:
                current["role"] = clean_field(role_match.group(1))
                continue

            # tech
            tech_match = TECH_RE.match(text)
            if tech_match:
                current["technologies"] = split_tech_stack(
                    tech_match.group(1)
                )
                continue
            # =============================
            # DATE RANGE
            # =============================
            date_match = DATE_RANGE_RE.search(text)
            if date_match and current:
                start_dt = parse_date_safe(date_match.group("start"))
                end_dt = parse_date_safe(date_match.group("end"))

                current["start_date"] = date_match.group("start")
                current["end_date"] = date_match.group("end")

                months = months_between(start_dt, end_dt)
                current["duration_months"] = months
                current["duration_text"] = format_duration(months)
                continue

            # description
            clean_line = re.sub(r"^[•\-]\s*", "", text)
            if len(clean_line.split()) > 2:
                current["description"].append(clean_line)

        if current["company"]:
            experiences.append(current)
    return experiences
def compute_total_experience(experiences: list) -> dict:
    total_months = sum(exp.get("duration_months", 0) for exp in experiences)

    return {
        "total_months": total_months,
        "total_experience": format_duration(total_months),
    }