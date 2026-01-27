from flask import Flask, request, jsonify
from services.pdf_service import extract_text_from_pdf
from services.text_cleaner import clean_text
from services.section_detector import detect_sections
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']

    # Save the uploaded file temporarily
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # Extract text from PDF
    raw_text = extract_text_from_pdf(file_path)

    cleaned = clean_text(raw_text)

    sections = detect_sections(cleaned)

    return jsonify({
        'raw_text': raw_text,
        'cleaned_text': cleaned,
        'sections': sections
        })


if __name__ == '__main__':
    app.run(debug=True)