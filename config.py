
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')
    DB_NAME = os.getenv('DB_NAME', 'resume_analyzer')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    
    # Model Paths
    MODEL_DIR = 'models/'
    NER_MODEL_PATH = os.path.join(MODEL_DIR, 'resume_ner')
    SECTION_CLASSIFIER_PATH = os.path.join(MODEL_DIR, 'section_classifier.pth')
    QUALITY_SCORER_PATH = os.path.join(MODEL_DIR, 'quality_scorer.pth')
    
    # Upload Configuration
    UPLOAD_DIR = 'uploaded_resumes/'
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS = ['pdf', 'docx']
    
    # ML Model Configuration
    # USE_GPU = os.getenv('USE_GPU', 'False').lower() == 'true'
    # BERT_MODEL = 'bert-base-uncased'
    # SENTENCE_TRANSFORMER_MODEL = 'all-mpnet-base-v2'
    
    # Scoring Thresholds
    MIN_RESUME_SCORE = 0
    MAX_RESUME_SCORE = 100
    SKILL_MATCH_THRESHOLD = 0.65
    
    # Application Settings
    APP_NAME = "AI Resume Analyzer"
    APP_VERSION = "2.0.0"
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Create necessary directories
os.makedirs(Config.MODEL_DIR, exist_ok=True)
os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)
os.makedirs('data/training', exist_ok=True)