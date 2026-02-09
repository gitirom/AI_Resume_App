from flask import Flask, request, jsonify
from services.pdf_service import extract_text_from_pdf
from services.text_cleaner import clean_text
from services.section_detector import detect_sections
from services.nlp_service import analyze_resume
from services.job_service import fetch_job_requirements
from nlp.chunking import ChunkingService
from dotenv import load_dotenv
import logging
import os


app = Flask(__name__)

logger = logging.getLogger(__name__)

load_dotenv()


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

chunker = ChunkingService()


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    if not os.path.exists(file_path):
        file.save(file_path)
        saved = True
    else:
        saved = False

    raw_text = extract_text_from_pdf(file_path)

    sections = detect_sections(raw_text)

    cleaned_text = clean_text(raw_text)

    return jsonify({
        "sections": sections,
        "cleaned_text": cleaned_text
    })

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True)   #silent: Prevents Flask from throwing an error returns None if JSON is not valid

    if not data or "clean_text" not in data:
        return jsonify({
            "error": "Missing required field: clean_text"
        }), 400
    
    clean_text = data.get("clean_text", "").strip()

    if not clean_text:
        return jsonify({
            "error": "clean_text cannot be empty"
        }), 400
    
    try:
        result = analyze_resume(clean_text)
        return jsonify({
            "status": "success",
            "data": result
        }), 200
    except Exception as e:
        print(f"[ERROR] Resume analysis failed: {e}")

        return jsonify({
            "status": "error",
            "message": "Resume analysis failed"
        }), 500
    

@app.route("/job-search", methods=["POST"])
def job_search():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    job_title = data.get("job_title")

    if not isinstance(job_title, str) or not job_title.strip():
        return jsonify({"error": "job_title must be a non-empty string"}), 400

    job_title = job_title.strip()

    try:
        result = fetch_job_requirements(job_title)

        return jsonify({
            "status": "success",
            "data": result
        }), 200

    except Exception as e:
        logger.exception("Job search failed")

        return jsonify({
            "status": "error",
            "message": "Failed to fetch job requirements"
        }), 500
    
@app.route("/chunk/resume", methods=["POST"])
def chunk_resume():
    data = request.get_json(silent=True)

    if not data or "resume_text" not in data:
        return jsonify({"error": "Missing required field: resume_text"}), 400
    
    resume_text = data.get("resume_text", "").strip()
    if not resume_text:
        return jsonify({"error": "resume_text cannot be empty"}), 400
    
    try:
        chunks = chunker.chunk_resume(resume_text)
        return jsonify({
            "status": "success",
            "data": chunks
        }), 200
    except Exception as e:
        logger.exception("Resume chunking failed")
        return jsonify({
            "status": "error",
            "message": "Failed to chunk resume text"
        }), 500
    
@app.route("/chunk/job", methods=["POST"])
def chunk_job_description():
    data = request.get_json(silent=True)

    if not data or "job_description" not in data:
        return jsonify({"error": "Missing required field: job_description"}), 400

    job_description = data.get("job_description", "").strip()
    if not job_description:
        return jsonify({"error": "job_description cannot be empty"}), 400

    try:
        chunks = chunker.chunk_job_description(job_description)
        return jsonify({
            "status": "success",
            "chunks": chunks
        }), 200
    except Exception as e:
        logger.exception("Job description chunking failed")
        return jsonify({
            "status": "error",
            "message": "Failed to chunk job description"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
