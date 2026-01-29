import re
from typing import Optional, Dict

EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
)

PHONE_PATTERN = re.compile(
    r"\+?\d[\d\s\-().]{7,}\d"
)

LINKEDIN_PATTERN = re.compile(
    r"https?://(?:www\.)?linkedin\.com/[^\s]+",
    re.IGNORECASE
)

GITHUB_PATTERN = re.compile(
    r"https?://(?:www\.)?github\.com/[^\s]+",
    re.IGNORECASE
)

def extract_contact_info(text: str) -> Dict[str, Optional[str]]:
    
    email_match = EMAIL_PATTERN.search(text)
    phone_match = PHONE_PATTERN.search(text)
    linkedin_match = LINKEDIN_PATTERN.search(text)
    github_match = GITHUB_PATTERN.search(text)

    return {
        "email": email_match.group(0) if email_match else None,     # 0 = test@gmail.com
        "phone": phone_match.group(0) if phone_match else None,
        "linkedin": linkedin_match.group(0) if linkedin_match else None,
        "github": github_match.group(0) if github_match else None
    }