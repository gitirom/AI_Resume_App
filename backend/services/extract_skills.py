import re
from typing import List

SKILLS = [
    # Programming
    "python",
    "javascript",
    "typescript",

    # Frontend / Backend
    "react",
    "next.js",
    "node.js",

    # DevOps / Cloud
    "docker",
    "kubernetes",
    "aws",

    # Databases
    "sql",
    "postgresql",
    "mongodb",
    "redis",
    "neo4j",
    "elasticsearch",

    # AI / ML
    "machine learning",
    "deep learning",
    "nlp",
    "data analysis",
    "pytorch",
    "tensorflow",
    "scikit-learn",
    "hugging face",
    "transformers",
    "llms",
    "rag",
    "embeddings",
    "fine-tuning",
    "mlops",

    # Vector Databases
    "faiss",
    "qdrant",
    "pinecone",

    # Data Engineering
    "etl",
    "data pipelines",
    "apache spark",
    "apache kafka",
    "airflow",
    "data warehousing",
    "bigquery",
    "redshift",
    "snowflake",
    "hadoop",
    "parquet",
    "delta lake",

    # Web basics
    "html",
    "css",
    "tailwind",

    # Tools
    "git",
]



SKILL_PATTERNS = {
    skill: re.compile(
        rf"\b{re.escape(skill)}\b",
        re.IGNORECASE
    )
    for skill in SKILLS
}

def extract_skills(text: str) -> List[str]:

    found: List[str] = []

    for skill, pattern in SKILL_PATTERNS.items():
        if pattern.search(text):
            found.append(skill)

    return found