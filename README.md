Class ResumeParser
==================================

The ResumeParser class extracts essential information from resumes in PDF format. It utilizes the spaCy natural language processing library to analyze the text and extract details such as email, phone number, address, skills, and certifications.

**Key Features:**

Text Extraction from PDF:
    Extracts text from a PDF resume file using the PyMuPDF library.

- Text Preprocessing:
    Performs text preprocessing on the spaCy Doc object, including lemmatization, lowercasing and removal of stopwords, punctuation, symbols, and spaces.

- Email Extraction:
    Extracts the email address from the spaCy token with the help of **like_email** method of spacy. 

- Phone Number Extraction:
   Extracts the all types of phone number from the provided text using a regular expression.

- Address Extraction:
    Extracts the address from the text with the help of spacy ner **GPE**.

- Skills Extraction:
    Extracts skills from the text using an spacy's entity ruler. With the help of **skills.jsonl** file ruler is added to spacy object
    Also preprocessing is performed.

-   Certification Extraction
    Utilizes spaCy's Matcher to extract certification titles and dates from the text.

- Resume Parsing:
    Integrates all the extraction methods to parse the resume and return a dictionary with relevant details.



Web app Documentation
====================================

##### **Overview**
This is flask web application allows users to upload the resuke in **pdf** format and on parser the app lands the user in the result page.
- This app uses the parser class mentioned above to parse the resume details from the uploaded pdf.
- This web application consists of two web pages - Home Page(*index.html*) and Result Page(*result.html*)
   * Home Page: 
   ![alt text](./webapp/static/homepage.png?raw=true)
   Here user can upload the pdf version of the resume.

   * Result Page:
   ![alt text](./webapp/static/resultpage.png?raw=true)
   Here the results parsed from the resume is displayed in the tabular format.
   The fields displayed are:
      - phone number
      - email
      - address
      - skills
      - work details
      - certifications


##### **Running the Application**
The Flask application is run using python app.py in the terminal, and the web interface can be accessed at http://127.0.0.1:5000/..

