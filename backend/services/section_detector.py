import re
from typing import List, Dict

SECTION_HEADERS = [
    "profile",
    "professional experience",
    "experience",
    "education",
    "projects",
    "skills",
    "languages",
    "publications",
    "certificates",
    "volunteer",
]

SECTION_PATTERNS = {
    header: re.compile(
        rf"(?m)^\s*{re.escape(header)}\s*$",
        re.IGNORECASE
    )
    for header in SECTION_HEADERS
}


def detect_sections(text: str) -> List[Dict]:

    sections = []

    for header, pattern in SECTION_PATTERNS.items():
        match = pattern.search(text)
        if match:
            sections.append({
                "name": header,
                "start": match.start()
            })

    # Sort by document position
    sections.sort(key=lambda x: x["start"])

    return sections
