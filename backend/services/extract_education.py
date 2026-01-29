import re

DEGREE_PATTERN = re.compile(
    r"""
    (?P<degree>
        bachelor|master|ph\.?d|doctorate|
        b\.?sc|m\.?sc|b\.?eng|m\.?eng|
        license|licence|engineering|degree
    )
    """,
    re.IGNORECASE | re.VERBOSE
)

YEAR_PATTERN = re.compile(r"\b(19|20)\d{2}\b")

def extract_education(text: str) -> list[dict]:
    results = []
    seen = set()

    for line in text.splitlines():
        clean_line = line.strip()
        if not clean_line:
            continue  #Immediately moves to the next iteration

        if DEGREE_PATTERN.search(clean_line):
            year_match = YEAR_PATTERN.search(clean_line)

            entry = {
                "degree": DEGREE_PATTERN.search(clean_line).group(0),
                "year": year_match.group(0) if year_match else None,
                "raw": clean_line
            }

            key = clean_line.lower()
            if key not in seen:
                seen.add(key)
                results.append(entry)

    return results