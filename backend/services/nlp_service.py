from services.extract_contact import extract_contact_info
from services.extract_skills import extract_skills
from services.extract_experience import extract_experience
from services.extract_education import extract_education

from typing import Dict, Any, Callable

EXTRACTORS: Dict[str, Callable[[str], Any]] = {    #registry of extraction functions, each function takes str as param and return any.
    "contact": extract_contact_info,
    "skills": extract_skills,
    "experience": extract_experience,
    "education": extract_education,
}

def analyze_resume(clean_text: str) -> Dict[str, Any]:
    
    results: Dict[str, Any] = {}   #annotaion type 

    for name, extractor in EXTRACTORS.items():
        try:
            results[name] = extractor(clean_text)
        except Exception as e:
            results[name] = None
            print(f"[WARN] {name} extraction failed: {e}")


    return results