import re
SKILL_HEADER_WORDS = {
    "skills",
    "technical skills",
    "core competencies",
    "key skills",
    "key expertise"
}
def merge_skill_lines(lines: list) -> list:
    """
    Merge wrapped skill lines.
    Prevents broken tokens across lines.
    """
    merged = []
    buffer = ""

    for line in lines:
        t = line.strip()
        if not t:
            continue


        # if previous line ended with comma → merge
        if buffer and buffer.endswith(","):
            buffer += " " + t
        else:
            if buffer:
                merged.append(buffer)
            buffer = t

    if buffer:
        merged.append(buffer)

    return merged
def normalize_skill(text: str) -> str:
    """Clean individual skill token."""
    text = text.strip()
    text = text.rstrip(",;:.")

    # normalize spacing
    text = re.sub(r"\s+", " ", text)

    # smart casing (preserve things like Node.js)
    if text.isupper():
        text = text.title()

    return text


def split_skill_tokens(line: str) -> list:
    """
    Split skill lines safely.
    Handles commas and multiple spaces.
    """
    parts = re.split(r"[,\|/•]+|\s{2,}", line)
    return [normalize_skill(p) for p in parts if p.strip()]


def extract_skills(sections: dict) -> list:
    """
    Production-safe skill extractor.
    Works on section-based parsing.
    """

    skill_lines = merge_skill_lines(sections.get("skills", []))
    if not skill_lines:
        return []

    skills = []

    for line in skill_lines:
        text = line.strip()

        if not text:
            continue
        if text.lower() in SKILL_HEADER_WORDS:
            continue

        # remove labels like "Programming Languages:"
        if ":" in text:
            text = text.split(":", 1)[1]

        tokens = split_skill_tokens(text)

        for t in tokens:
            # ignore very short junk
            if len(t) <= 1:
                continue
            skills.append(t)

    # -----------------------------
    # deduplicate (important)
    # -----------------------------
    seen = set()
    unique = []

    for s in skills:
        key = s.lower()
        if key not in seen:
            seen.add(key)
            unique.append(s)

    return unique