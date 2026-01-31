import re

DEGREE_PATTERN = re.compile(
    r"""
    (?P<degree>
        (?:
            Bachelor(?:\s+of\s+[A-Za-z &]+)? |
            Master(?:\s+of\s+[A-Za-z &]+)? |
            Doctor(?:ate)?(?:\s+of\s+[A-Za-z &]+)? |
            Ph\.?\s?D |
            B\.?\s?Sc(?:\.\s*in\s+[A-Za-z &]+)? |
            M\.?\s?Sc(?:\.\s*in\s+[A-Za-z &]+)? |
            B\.?\s?Eng(?:\.\s*in\s+[A-Za-z &]+)? |
            M\.?\s?Eng(?:\.\s*in\s+[A-Za-z &]+)? |
            Engineering\s+Degree |
            Licence |
            License
        )
    )
    """,
    re.IGNORECASE | re.VERBOSE
)

YEAR_PATTERN = re.compile(
    r"""
    (?P<start>
        (?:0[1-9]|1[0-2])?/?\s*(19|20)\d{2}
    )
    \s*(?:–|—|-|to)\s*
    (?P<end>
        Present|
        Current|
        (?:0[1-9]|1[0-2])?/?\s*(19|20)\d{2}
    )
    """,
    re.IGNORECASE | re.VERBOSE
)

SCHOOL_PATTERN = re.compile(
    r"""
    ,\s*                                   # comma and optional spaces
    (?P<school>                             # capture school name
        [A-Z][A-Za-z0-9&.,\-\s]+?         # school name: starts with capital letter
    )
    (?=\s*(?:0[1-9]|1[0-2])?/?\s*(?:19|20)\d{2}  # stop before year
        |$                                 # or end of string
        |[A-Z][A-Z\s]{2,}                  # or next all-caps section (e.g., PROFESSIONAL EXPERIENCE)
    )
    """,
    re.VERBOSE
)


def extract_education(text: str) -> list[dict]:
    results = []
    
    # Step 1: Locate EDUCATION section
    edu_match = re.search(r'EDUCATION\s*(.*?)(?:\n[A-Z][A-Z\s]+|$)', text, re.DOTALL | re.IGNORECASE)
    if not edu_match:
        return results  # no education section found

    edu_text = edu_match.group(1).strip()
    lines = [l.strip() for l in edu_text.splitlines() if l.strip()]

    for i, line in enumerate(lines):
        degree_match = DEGREE_PATTERN.search(line)
        if not degree_match:
            continue

        # look for year in the same line or next line
        year_match = YEAR_PATTERN.search(line)
        if not year_match and i + 1 < len(lines):
            year_match = YEAR_PATTERN.search(lines[i + 1])

        # look for school using SCHOOL_PATTERN
        school_match = SCHOOL_PATTERN.search(line)
        school = school_match.group("school").strip() if school_match else None

        results.append({
            "degree": degree_match.group("degree").strip(),
            "school": school,
            "year": year_match.group(0) if year_match else None,
            "raw": line
        })

    return results
