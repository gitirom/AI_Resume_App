import re

SECTION_HEADERS = [
    "experience",
    "work experience",
    "professional experience",
    "education",
    "projects",
    "skills",
    "certifications",
    "summary",
    "about me",
]


def detect_sections(text):
    sections = {}
    lower_text = text.lower()

    for header in SECTION_HEADERS:
        pattern = rf"{header}[:\n]"
        match = re.search(pattern, lower_text)
        if match:
            start = match.start()
            sections[header] = start

    sorted_sections = sorted(sections.items(), key=lambda x: x[1])

    return [s[0] for s in sorted_sections]