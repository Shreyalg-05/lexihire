# engine/section_classifier.py

import re

HEADER_KEYWORDS = {
    "summary": [
        "summary", "professional summary", "profile", "about"
    ],
    "experience": [
        "experience", "work experience", "professional experience",
        "employment", "work history", "internship"
    ],
    "education": [
        "education", "academic background"
    ],
    "skills": [
        "skills", "technical skills", "core competencies", "technologies"
    ],
    "projects": [
        "projects", "personal projects"
    ],
    "certifications": [
        "certifications", "licenses"
    ],
    "languages": [
        "languages"
    ],
}

def normalize_section_headers(text: str) -> str:
    """
    ATS-grade aggressive header normalization.
    Handles inline, glued, and multi-header lines.
    """
    if not text:
        return text

    headers = [
        "professional summary",
        "summary",
        "professional experience",
        "work experience",
        "experience",
        "education",
        "academic background",
        "projects",
        "skills",
        "technical skills",
        "certifications",
        "languages",
    ]

    # -----------------------------
    # STEP 1 — force newline before headers
    # -----------------------------
    for h in sorted(headers, key=len, reverse=True):
        pattern = rf"(?i)(?<!\n)\b({re.escape(h)})\b"
        text = re.sub(pattern, r"\n\1", text)

    # -----------------------------
    # STEP 2 — split consecutive ALL-CAPS headers
    # 🔥 THIS is what fixes your case
    # -----------------------------
    text = re.sub(
        r"\n([A-Z][A-Z ]{3,})\s+([A-Z][A-Z ]{3,})",
        r"\n\1\n\2",
        text
    )

    # -----------------------------
    # STEP 3 — clean spacing
    # -----------------------------
    text = re.sub(r"\n{2,}", "\n", text)

    return text.strip()
def _normalize(line: str) -> str:
    return re.sub(r"[^a-z ]", "", line.lower()).strip()


def _header_score(line: str) -> int:
    """
    Multi-signal header scoring (ATS-style)
    """
    if not line:
        return 0

    score = 0
    clean = line.strip()
    lower = clean.lower()

    # signal 1: keyword match (strong)
    for aliases in HEADER_KEYWORDS.values():
        for alias in aliases:
            if lower == alias or lower.startswith(alias):
                score += 3
                break

    # signal 2: ALL CAPS
    if clean.isupper() and 1 <= len(clean.split()) <= 4:
        score += 1

    # signal 3: short line
    if len(clean.split()) <= 4:
        score += 1

    return score


def extract_sections(full_text: str) -> dict:
    """
    ATS-style section splitter (stable version)
    """
    if not full_text:
        return {}

    text = normalize_section_headers(full_text)
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    sections = {}
    current_section = "header"
    buffer = []

    def flush():
        nonlocal buffer
        if buffer:
            sections[current_section] = "\n".join(buffer).strip()
            buffer = []

    for line in lines:
        normalized = _normalize(line)

        matched_section = None
        for sec, aliases in HEADER_KEYWORDS.items():
            if normalized in aliases:
                matched_section = sec
                break

        # ✅ ONLY switch when TRUE header keyword match
        if matched_section:
            flush()
            current_section = matched_section
            continue

        buffer.append(line)

    flush()
    return sections