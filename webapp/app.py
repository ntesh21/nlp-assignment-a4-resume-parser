from flask import Flask, render_template, request
# import spacy
import pdfplumber
from parser import ResumeParser

app = Flask(__name__)
# nlp = spacy.load("en_core_web_sm")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files:
        return render_template('index.html', error='No file part')

    resume_file = request.files['resume']

    if resume_file.filename == '':
        return render_template('index.html', error='No selected file')

    if resume_file and allowed_file(resume_file.filename):
        # text = extract_text_from_pdf(resume_file)
        resume_details = parse_resume(resume_file)
        return render_template('result.html', resume_details=resume_details)

    return render_template('index.html', error='Invalid file format')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

# def extract_text_from_pdf(file):
#     with pdfplumber.open(file) as pdf:
#         text = ''
#         for page in pdf.pages:
#             text += page.extract_text()
#     return text

def parse_resume(file):
   parser = ResumeParser(file)
   parsed_result = parser.parse()
   return parsed_result

if __name__ == '__main__':
    app.run(debug=True)
