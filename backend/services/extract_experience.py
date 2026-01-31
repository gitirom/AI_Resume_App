import re

def extract_experience(text: str) -> list[dict]:
    experiences = []

    # Isolate the PROFESSIONAL EXPERIENCE section
    experience_section = ""
    match = re.search(r"PROFESSIONAL EXPERIENCE(.*?)(EDUCATION|PROJECTS|SKILLS|CERTIFICATES|VOLUNTEER|$)", text, re.IGNORECASE | re.DOTALL)
    if match:
        experience_section = match.group(1)

    EXPERIENCE_PATTERN = re.compile(
        r"""
        (?P<title>[A-Z][A-Za-z&/\- ]{2,50}          # Title: capitalized words
            (?:\s+(?:Intern|Engineer|Instructor|Developer|Researcher))?)   # Optional role
        \s*,\s*
        (?P<company>[A-Z][A-Za-z0-9&.\- ]{2,50})    # Company name
        .*?                                          # Non-greedy skip bullets / description
        (?P<dates>
            (?:0[1-9]|1[0-2])/\d{4}                 # MM/YYYY
            \s*(?:–|-|to)\s*
            (?:0[1-9]|1[0-2])/\d{4}|Present
            |
            \d{4}\s*(?:–|-|to)\s*(?:\d{4}|Present)
        )
        """,
        re.VERBOSE | re.DOTALL
    )

    # Apply regex only to PROFESSIONAL EXPERIENCE section
    for match in EXPERIENCE_PATTERN.finditer(experience_section):
        experiences.append({
            "title": match.group("title").strip(),
            "company": match.group("company").strip(),
            "dates": match.group("dates").replace("Current", "Present").strip(),
        })

    return experiences



