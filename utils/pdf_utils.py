import pdfplumber


def extract_full_text(file_path):
    full_text = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text(layout=True)

            if text:
                full_text.append(text)

    return "\n".join(full_text).strip()