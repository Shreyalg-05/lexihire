import fitz
import re
import unicodedata
from engine.experience_structurer import extract_experience_json
SECTION_HEADERS = {
    "summary": ["summary", "professional summary", "profile"],
    "experience": ["experience", "professional experience", "work experience"],
    "education": ["education", "academic background"],
    "skills": ["skills", "technical skills", "core competencies","key expertise","expertise"],
    "languages": ["languages"],
    "projects": ["projects"],
    "certifications": ["certifications"],
}

def normalize_text_for_matching(text: str) -> str:
    """
    Remove emoji/symbol noise in a generic way.
    NOT hardcoded.
    """
    cleaned = "".join(
        ch for ch in text
        if unicodedata.category(ch)[0] != "S"  # remove symbols
    )
    return cleaned.strip()
def detect_section_header(line_text: str):
    clean = re.sub(r"[^a-z ]", "", line_text.lower()).strip()

    for section, aliases in SECTION_HEADERS.items():
        for alias in aliases:
            # ⭐ allow contains match for robustness
            if clean == alias or clean.startswith(alias):
                return section
    return None
def split_lines_into_columns(lines):
    """
    Robust column detection using clustering.
    Works for uneven resume layouts.
    """
    if not lines:
        return [], []

    try:
        from sklearn.cluster import KMeans
        import numpy as np
    except ImportError:
        # fallback to midpoint if sklearn missing
        min_x = min(l["x0"] for l in lines)
        max_x = max(l["x1"] for l in lines)
        mid_x = min_x + (max_x - min_x) * 0.5

        left, right = [], []
        for l in lines:
            (left if l["x0"] < mid_x else right).append(l)
        return left, right

    # -----------------------------
    # cluster by x coordinate
    # -----------------------------
    X = np.array([[l["x0"]] for l in lines])

    kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    # determine which cluster is left/right
    centers = kmeans.cluster_centers_.flatten()
    left_cluster = centers.argmin()
    right_cluster = centers.argmax()

    left_lines = []
    right_lines = []

    for line, label in zip(lines, labels):
        if label == left_cluster:
            left_lines.append(line)
        else:
            right_lines.append(line)

    return left_lines, right_lines
def looks_like_body_text(text: str) -> bool:
    """
    Detects start of resume body to stop header capture.
    """
    t = text.lower()

    if len(text.split()) > 6:
        return True

    body_keywords = [
        "developer", "experience", "education",
        "project", "technologies", "responsible",
        "developed", "worked", "client"
    ]

    return any(k in t for k in body_keywords)
def looks_like_summary(text: str) -> bool:
    """
    Detect summary paragraph before explicit SUMMARY header.
    """
    if len(text.split()) < 12:
        return False

    t = text.lower()

    summary_keywords = [
        "developer", "experience", "years",
        "skilled", "proficient", "expertise",
        "full stack", "software engineer"
    ]

    return any(k in t for k in summary_keywords)
def build_sections_from_lines(lines):
    """
    Clean ATS-style section builder.
    Handles:
    - parallel headers
    - summary before header
    - bullet noise
    - deterministic section flow
    """

    sections = {}
    current_section = "header"
    pending_section = None
    last_header_y = -1
    last_header_x = -1
    header_line_count = 0

    for line in lines:
        text = line["text"].strip()
        y = line["y0"]
        x = line["x0"]

        if not text:
            continue

        detected = detect_section_header(text)

        # =====================================================
        # 1. HEADER DETECTED → ARM PENDING SECTION
        # =====================================================
        if detected:
            pending_section = detected
            last_header_y = y
            last_header_x = x
            sections.setdefault(detected, [])
            continue

        # =====================================================
        # 2. FORCE FIRST CONTENT AFTER HEADER
        # =====================================================
        if pending_section:
            current_section = pending_section
            sections.setdefault(current_section, []).append(text)
            pending_section = None
            continue

        # =====================================================
        # 3. AUTO SUMMARY PROMOTION (STRUCTURAL)
        # =====================================================
        if (
                current_section == "header"
                and looks_like_summary(text)
                and len(text.split()) >= 12
        ):
            current_section = "summary"
            sections.setdefault(current_section, []).append(text)
            continue

        # =====================================================
        # 4. BULLET NOISE FILTER
        # =====================================================
        if text in {"•", "-", "–"}:
            continue

        if len(text) == 1 and not text.isalnum():
            continue

        # =====================================================
        # 5. NORMAL APPEND
        # =====================================================
        sections.setdefault(current_section, []).append(text)

    return sections

def clean_section_content(sections: dict) -> dict:
    """
    Final ATS cleanup pass.
    Removes contact leakage and bullet noise.
    """

    EMAIL_RE = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b")
    PHONE_RE = re.compile(r"\+?\d[\d\s\-]{8,}\d")
    LOCATION_ONLY_RE = re.compile(
        r"^[A-Za-z\s]+(?:,?\s*[A-Za-z\s]+)?\s*📍?$"
    )

    cleaned = {}   # ⭐⭐⭐ THIS LINE WAS MISSING

    for sec, lines in sections.items():
        new_lines = []

        for line in lines:
            t = line.strip()

            if re.fullmatch(r"[•\-–]+", t):
                continue

            if sec not in {"header", "languages"}:
                normalized = normalize_text_for_matching(t)
                if EMAIL_RE.search(normalized) or PHONE_RE.search(normalized):
                    continue

                if (
                    LOCATION_ONLY_RE.fullmatch(t)
                    and len(t.split()) <= 3
                ):
                    continue

            new_lines.append(t)

        cleaned[sec] = merge_wrapped_lines(new_lines)

    return cleaned
def sections_to_text(sections: dict) -> str:
    parts = []

    order = [
        "header",
        "summary",
        "education",
        "experience",
        "skills",
        "languages",
        "projects",
        "certifications",
    ]

    for sec in order:
        if sec in sections and sections[sec]:
            parts.append(sec.upper())
            parts.extend(sections[sec])
            parts.append("")

    return "\n".join(parts)
def extract_lines_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    lines = []

    for page_num, page in enumerate(doc):
        text_dict = page.get_text("dict")

        for block in text_dict["blocks"]:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                line_text = "".join(
                    span["text"] for span in line["spans"]
                ).strip()

                if not line_text:
                    continue

                lines.append({
                    "text": line_text,
                    "x0": line["bbox"][0],
                    "y0": line["bbox"][1],
                    "x1": line["bbox"][2],
                    "y1": line["bbox"][3],
                    "page": page_num
                })

    return lines
# ===============================
# STEP 2 — column ordering
# ===============================
def order_lines_reading_order(lines):
    if not lines:
        return []

    min_x = min(l["x0"] for l in lines)
    max_x = max(l["x1"] for l in lines)
    page_width = max_x - min_x
    mid_x = min_x + page_width * 0.5

    left = []
    right = []

    for l in lines:
        if l["x0"] < mid_x:
            left.append(l)
        else:
            right.append(l)

    left_sorted = sorted(left, key=lambda l: (l["page"], l["y0"]))
    right_sorted = sorted(right, key=lambda l: (l["page"], l["y0"]))

    return left_sorted + right_sorted
# ===============================
# STEP 3 — blocks → text
# ===============================
def lines_to_text(lines):
    return "\n".join(l["text"] for l in lines)
def merge_section_dicts(sec1, sec2):
    merged = {}

    all_keys = list(dict.fromkeys(list(sec1.keys()) + list(sec2.keys())))

    for key in all_keys:
        merged[key] = []

        # left column has priority
        if key in sec1:
            merged[key].extend(sec1[key])

        if key in sec2:
            merged[key].extend(sec2[key])

    return merged

def merge_wrapped_lines(lines: list) -> list:
    """
    Smarter merge:
    - merges real wrapped sentences
    - preserves headers and field lines
    """

    merged = []
    buffer = ""

    def looks_incomplete(line: str) -> bool:
        line = line.strip()

        if not line:
            return False

        # ✅ if line ends with strong sentence punctuation → complete
        if re.search(r"[.!?]$", line):
            return False

        # ✅ lines ending with colon are usually headers/fields
        if line.endswith(":"):
            return False

        # ✅ ALL CAPS short lines are usually headers
        if line.isupper() and len(line.split()) <= 6:
            return False

        # ✅ very short lines are usually list items
        if len(line.split()) <= 3:
            return False

        # otherwise likely wrapped
        return True

    FIELD_PREFIXES = (
        "client:",
        "role:",
        "technologies:",
        "technology stack:",
        "programming languages:",
        "web development:",
        "database:",
        "api tools:",
        "backend",
        "software development tools:",
    )

    for line in lines:
        t = line.strip()
        if not t:
            continue

        lower = t.lower()

        # 🚫 NEVER merge structured field lines
        if lower.startswith(FIELD_PREFIXES):
            if buffer:
                merged.append(buffer)
                buffer = ""
            merged.append(t)
            continue

        # 🚫 NEVER merge ALL CAPS headers
        if t.isupper() and len(t.split()) <= 6:
            if buffer:
                merged.append(buffer)
                buffer = ""
            merged.append(t)
            continue

        # ✅ normal wrap merge
        is_short_item = len(t.split()) <= 3

        if buffer and looks_incomplete(buffer):
            buffer += " " + t
        else:
            if buffer:
                merged.append(buffer)
            buffer = t

    if buffer:
        merged.append(buffer)


    return merged
# ===============================
# MAIN TEST
# ===============================
if __name__ == "__main__":
    pdf_path = "uploads/resumes/64/Basavaraju_MNResume.pdf"

    lines = extract_lines_pymupdf(pdf_path)
    # 🔥 FIRST split by columns
    left_lines, right_lines = split_lines_into_columns(lines)

    # 🔥 THEN order inside each column
    left_lines = order_lines_reading_order(left_lines)
    right_lines = order_lines_reading_order(right_lines)

    left_sections = build_sections_from_lines(left_lines)
    right_sections = build_sections_from_lines(right_lines)
    sections = merge_section_dicts(left_sections, right_sections)
    sections = clean_section_content(sections)
    ordered = order_lines_reading_order(lines)
    text = sections_to_text(sections)

    for sec, content in sections.items():
        print("\n" + "=" * 30)
        print(sec.upper())
        print("=" * 30)
        print("\n".join(content[:20]))
    print("\n" + "=" * 80)
    print("RECONSTRUCTED TEXT")
    print("=" * 80)
    print(text[:3000])
    exp_json = extract_experience_json(sections)

    print("\n" + "=" * 30)
    print("EXPERIENCE JSON")
    print("=" * 30)

    import json

    print(json.dumps(exp_json, indent=2))