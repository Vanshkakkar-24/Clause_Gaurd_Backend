import re
import nltk

def split_into_clauses(text: str):

    text = text.replace("\r", "\n")

    # common legal clause patterns
    pattern = r'\n\s*(\d+\.|\([a-zA-Z]\)|[A-Z][A-Z\s]{3,})'

    splits = re.split(pattern, text)

    clauses = []

    for part in splits:
        part = part.strip()

        if len(part) > 40:
            clauses.append(part)

    # fallback sentence splitting
    if len(clauses) < 3:
        clauses = nltk.sent_tokenize(text)

    return clauses