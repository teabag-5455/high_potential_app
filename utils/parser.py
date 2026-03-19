import os
import pandas as pd
import docx
from PyPDF2 import PdfReader
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from .talent_vector import generate_talent_vector, all_skills

# NLTK 組件檢查
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

STOP_WORDS = set(stopwords.words('english'))

def clean_text_simple(text):
    if not text: return ""
    tokens = word_tokenize(str(text).lower())
    cleaned = [t for t in tokens if t.isalpha() and t not in STOP_WORDS]
    return ' '.join(cleaned)

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    if ext == '.docx':
        doc = docx.Document(file_path)
        text = '\n'.join([p.text for p in doc.paragraphs])
    elif ext == '.pdf':
        reader = PdfReader(file_path)
        text = '\n'.join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    return text

def parse_uploaded_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    results = []

    if ext == '.csv':
        df = pd.read_csv(file_path, on_bad_lines='skip', encoding='utf-8-sig')
        for _, row in df.iterrows():
            raw_resume = str(row.get('Resume_Text') or row.get('Resume') or "")
            profile = {
                'Name': row.get('Name', 'Unknown'),
                'Resume_Text': clean_text_simple(raw_resume),
                'Raw_Text': raw_resume,  # 確保原始文字存在
                'Skills_List': [s for s in all_skills if s in raw_resume.lower()],
                'Years_Experience': int(row.get('Years_Experience', 0)),
                'Education_Level': row.get('Education_Level', 'Bachelor'),
                'Job_Role': row.get('Job_Role', '')
            }
            results.append(generate_talent_vector(profile))
    else:
        raw_text = extract_text_from_file(file_path)
        profile = {
            'Name': os.path.basename(file_path),
            'Resume_Text': clean_text_simple(raw_text),
            'Raw_Text': raw_text,   # 確保原始文字存在
            'Skills_List': [s for s in all_skills if s in raw_text.lower()],
            'Years_Experience': 0, 
            'Education_Level': 'Bachelor',
            'Job_Role': ''
        }
        results.append(generate_talent_vector(profile))
        
    return results