from flask import Flask, request, jsonify
from services.pdf_service import extract_text_from_pdf
from services.text_cleaner import clean_text
from services.section_detector import detect_sections
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


if __name__ == "__main__":
    app.run(debug=True)
