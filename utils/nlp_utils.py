import spacy

nlp = spacy.load("en_core_web_sm")

def extract_sentences(text: str):
    if not text:
        return []

    doc = nlp(text)

    return [
        sent.text.strip()
        for sent in doc.sents
        if len(sent.text.strip()) >= 20  # 🔥 better threshold
    ]
