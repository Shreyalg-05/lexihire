from engine.debug_extraction import extract_lines_pymupdf, split_lines_into_columns, order_lines_reading_order, lines_to_text

def test_resume(pdf_path):
    print("\n" + "="*80)
    print("TESTING:", pdf_path)
    print("="*80)

    lines = extract_lines_pymupdf(pdf_path)

    # column split
    left, right = split_lines_into_columns(lines)

    # order inside columns
    left = order_lines_reading_order(left)
    right = order_lines_reading_order(right)

    ordered = left + right

    text = lines_to_text(ordered)

    print("\n--- FIRST 800 CHARS ---\n")
    print(text[:800])


if __name__ == "__main__":
    resumes = [
        "uploads/resumes/66/Spoorth_resume.pdf",
        "uploads/resumes/67/Basavaraju_MNResume.pdf",
    ]

    for r in resumes:
        test_resume(r)