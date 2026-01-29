from flask import Flask, request, jsonify
from services.pdf_service import extract_text_from_pdf
from services.text_cleaner import clean_text
from services.section_detector import detect_sections
from services.nlp_service import analyze_resume
import os

app = Flask(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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


if __name__ == "__main__":
    app.run(debug=True)
