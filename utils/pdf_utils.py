import pdfplumber

def extract_full_text(file_path):
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text(
                x_tolerance=2,
                y_tolerance=2
            )

            if page_text:
                text += page_text + "\n"

    return text.strip()
