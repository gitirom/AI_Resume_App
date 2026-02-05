import os
from tavily import TavilyClient
import re
from collections import Counter

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

SKILLS = {
    # Programming
    "python", "javascript", "typescript",

    # Frontend / Backend
    "react", "next.js", "node.js",

    # DevOps / Cloud
    "docker", "kubernetes", "aws",

    # Databases
    "sql", "postgresql", "mongodb", "redis",
    "neo4j", "elasticsearch",

    # AI / ML
    "machine learning", "deep learning", "nlp",
    "data analysis", "pytorch", "tensorflow",
    "scikit-learn", "hugging face", "transformers",
    "llms", "rag", "embeddings", "fine-tuning", "mlops",

    # Vector Databases
    "faiss", "qdrant", "pinecone",

    # Data Engineering
    "etl", "data pipelines", "apache spark",
    "apache kafka", "airflow", "data warehousing",
    "bigquery", "redshift", "snowflake", "hadoop",
    "parquet", "delta lake",

    # Web basics
    "html", "css", "tailwind",

    # Tools
    "git"
}

RESPONSIBILITY_PATTERN = re.compile(
    r"(responsibilities|what you will do|your role).*?:?(.*?)(requirements|skills|qualifications|$)",
    re.IGNORECASE | re.DOTALL
)

STOPWORDS = {
    "with", "that", "this", "will", "have", "from",
    "your", "about", "into", "using", "their", "they",
    "them", "able", "work", "role", "team", "skills",
    "requirements"
}

def fetch_job_requirements(job_title: str) -> dict:
    query = f"Job description, required skills, responsibilities for {job_title} role."

    try:
        response = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )
    except Exception as e:
        return {
            "job_title": job_title,
            "skills": [],
            "responsibilities": [],
            "keywords": [],
            "raw_text": "",
            "error": str(e)
        }

    # Collect all content safely
    results = response.get("results", [])
    contents = [r.get("content", "") for r in results if r.get("content")]

    combined_text = " ".join(contents)

    if not combined_text:
        return {
            "job_title": job_title,
            "skills": [],
            "responsibilities": [],
            "keywords": [],
            "raw_text": ""
        }

    # Run extraction once (much faster)
    skills = list(set(extract_skills_from_job(combined_text)))
    responsibilities = list(set(extract_responsibilities(combined_text)))
    keywords = list(set(extract_keywords(combined_text)))

    return {
        "job_title": job_title,
        "skills": skills,
        "responsibilities": responsibilities,
        "keywords": keywords,
        "raw_text": combined_text
    }


def extract_skills_from_job(text: str) -> list:
    text_lower = text.lower()

    found_skills = {
        skill for skill in SKILLS
        if skill in text_lower
    }

    return sorted(found_skills)



def extract_responsibilities(text: str) -> list:
    match = RESPONSIBILITY_PATTERN.search(text)

    if not match:
        return []

    section = match.group(2)

    lines = [
        re.sub(r"^[\-\•\*\d\.\)\s]+", "", line).strip()
        for line in section.split("\n")
    ]

    return [line for line in lines if len(line) > 8]



def extract_keywords(text: str, top_n: int = 20) -> list:
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())

    filtered = [w for w in words if w not in STOPWORDS]

    freq = Counter(filtered)

    return [word for word, _ in freq.most_common(top_n)]

