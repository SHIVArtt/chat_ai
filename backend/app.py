from flask import Flask, request, jsonify
import PyPDF2
import os
from transformers import pipeline

app = Flask(__name__)

# Load the question-answering pipeline
qa_pipeline = pipeline('question-answering', model='distilbert-base-uncased-distilled-squad')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename.endswith('.pdf'):
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''.join(page.extract_text() for page in reader.pages)
        
        return jsonify({'text': text}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question')
    context = data.get('context')
    
    if not question or not context:
        return jsonify({'error': 'Question and context are required'}), 400
    
    response = qa_pipeline(question=question, context=context)
    return jsonify(response), 200

if __name__ == '__main__':
    # Ensure the uploads directory exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True, port=5000)
