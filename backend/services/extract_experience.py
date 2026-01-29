import re

JOB_PATTERN = re.compile(
    r"""
    (?P<title>
        [A-Z][A-Za-z/&\-\s]{2,60}      # Job title (reasonable length)
    )
    \s*(?:,|\||\-)?\s*
    (?P<dates>
        (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?\.?\s*\d{4}
        \s*(?:-|–|to)\s*
        (?:
            (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?\.?\s*\d{4}
            |Present|Current
        )
        |
        \d{4}\s*(?:-|–|to)\s*(?:\d{4}|Present|Current)
    )
    """,
    re.IGNORECASE | re.VERBOSE
)


def extract_experience(text: str) -> list[dict]:
    experiences = []

    for match in JOB_PATTERN.finditer(text):
        title = re.sub(r"\s{2,}", " ", match.group("title")).strip()
        dates = match.group("dates").replace("Current", "Present").strip()

        experiences.append({
            "title": title,
            "dates": dates
        })

    return experiences