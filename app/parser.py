import fitz
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.matcher import Matcher
import re

class ResumeParser:
    def __init__(self, pdf_file):
        self.nlp = spacy.load("en_core_web_sm")
        self.file = pdf_file

    def extract_pdf(self):
        resume_text = ''
        doc = fitz.open('../data/sample.pdf') 
        for page in doc:
            resume_text += ' '+page.get_text() 
        return resume_text
    
    def preprocessing(self, doc):
        stopwords    = list(STOP_WORDS)
        clean_tokens = []
        for token in doc:
            if token.text not in stopwords and token.pos_ != 'PUNCT' and token.pos_ != 'SYM' and \
                token.pos_ != 'SPACE':
                    processed_text = re.sub(
                        '[^a-zA-Z0-9@( )\s-]',
                        " ",
                    token.lemma_)
                    processed_text = processed_text.lower().strip()
                    clean_tokens.append(processed_text)
        return " ".join(clean_tokens)
    
    def extract_email(self, doc):
        for token in doc:
            if token.like_email:
                return token.text
            else:
                email = None
        return email
    
    def extract_phone_number(self, text):
        phone_number_pattern = re.compile(
            r'(?:(?:\+\d{1,2}\s?)?[\(\[\{]?\d{3}[\)\]\}]?[\s\-]?\d{3}[\s\-]?\d{4})|'
            r'(?:\d{3}[\s\-]?\d{3}[\s\-]?\d{4})|'
            r'(?:\(\d{3}\)\s?\d{3}[\s\-]?\d{4})'
        )
        matches = re.findall(phone_number_pattern, text)
        if matches:
            return matches[0]
        else:
            return None
    
    def extract_address(self, doc):
        address = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
        if address:
            return ' '.join(list(set(address[:3])))
        else:
            return None
    
    def extract_skills(self, text):
        skill_path = '../data/skills.jsonl'
        try:
            ruler = self.nlp.add_pipe("entity_ruler")
            ruler.from_disk(skill_path)
        except ValueError:
            pass
        try:
            doc = self.nlp(text)
            skills = list(doc.ents)
            gpe_entities = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
            gpe_entities = [gpe.lower() for gpe in gpe_entities]
            skills = [sk.text for sk in skills if sk.text.lower() not in gpe_entities]
            skills = list(set(skills))
            if skills:
                pattern2 = "(\d{1})"
                skills =  [sk for sk in skills if len(re.findall(pattern2, sk)) < 2]
                return [sk for sk in skills if len(sk) > 2]
            else:
                return []
        except:
            return []
        
    def extract_certifications(self, text):
        matcher = Matcher(self.nlp.vocab)
        #pattern
        certification_pattern = [
            {"LOWER": {"in": ["certification", "certificate", "course", "certifications"]}}, 
            {"ENT_TYPE": {"in": ["ORG", "PRODUCT"]}, "OP": "?"}, 
            {"ENT_TYPE": "DATE", "OP": "?"},
        ]
        matcher.add("CertificationPattern", [certification_pattern])
        doc = self.nlp(text)
        matches = matcher(doc)
        matched_spans = [doc[start:] for match_id, start, end in matches]
        certificates = []
        if matched_spans:
            for span in matched_spans:
                cert_details = {}
                matched_cert = span.text
                doc = self.nlp(matched_cert)
                for ent in doc.ents:
                    if ent.label_ == 'DATE':
                        date_span = span.text.find(ent.text)
                        cert_details['title'] = span.text[:date_span]
                        cert_details['date'] = ent.text
                        certificates.append(cert_details)
                        break
                    else:
                        cert_details['title'] = span.text[:5]
                        cert_details['date'] = None
            return certificates
        else:
            return certificates

    def parse(self):
        resume_details = {}
        resume_text = self.extract_pdf()
        doc = self.nlp(resume_text)
        processed_text = self.preprocessing(doc)
        resume_details['Email'] = self.extract_email(doc) 
        resume_details['Phone Number'] = self.extract_phone_number(processed_text)
        resume_details['Address'] = self.extract_address(doc)
        resume_details['Skills'] = self.extract_skills(processed_text)
        resume_details['Certification'] = self.extract_certifications(processed_text)
        return resume_details
        


