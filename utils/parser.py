import os
import pandas as pd
import docx
from PyPDF2 import PdfReader
import nltk
from nltk import pos_tag, ne_chunk
from nltk.tree import Tree
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from .talent_vector import generate_talent_vector, all_skills

def init_nltk():
    required_resources = [
        'punkt', 
        'punkt_tab', 
        'stopwords', 
        'averaged_perceptron_tagger',      # 舊版相容
        'averaged_perceptron_tagger_eng',  # 新版英文標註器
        'maxent_ne_chunker',
        'maxent_ne_chunker_tab',
        'words'
    ]# 如果跳出需要nltk.download提示，請在此補上
    
    for res in required_resources:
        try:
            # 嘗試下載，如果已存在會自動跳過
            nltk.download(res, quiet=True)
        except Exception as e:
            print(f"下載 {res} 失敗: {e}")

init_nltk()

STOP_WORDS = set(stopwords.words('english'))

def extract_name_smart(raw_text, file_path=None):
    # NER與位置判斷抓取名字
    BLACK_LIST = {'name', 'resume', 'cv', 'curriculum', 'page', 'profile', 'contact', 'email', 'phone'}#過濾黑名單
    # raw_text為空，回傳檔名。檔名為空回傳Unknown
    if not raw_text or len(raw_text.strip()) == 0:
        return os.path.basename(file_path) if file_path else "Unknown"
    
    # NLTK NER
    target_text = raw_text[:150] # 在文件前150字中尋找名字(效益化)
    try:
        tokens = word_tokenize(target_text)
        tags = pos_tag(tokens)
        chunks = ne_chunk(tags)
        
        for chunk in chunks:
            if isinstance(chunk, Tree) and chunk.label() == 'PERSON':
                name = " ".join([leaf[0] for leaf in chunk.leaves()])
                # 過濾:名字通常由2-3組單字組成
                cuts = name.split() #切片
                filter = [n for n in cuts if n.lower() not in BLACK_LIST and n.isalpha()] #過濾黑名單與非字母
                if len(filter) >= 2 and len(filter) < 4:
                    return " ".join(filter) #回傳過濾後的名字
    except Exception as e:
        print(f"NER Error: {e}")

    # 首行過濾，如果NER失敗，抓取前三行中第一條非空白、非標題的文字
    lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
    for line in lines[:3]:
        # 如果這行字數適中，且不在黑名單中，猜測是名字
        if 2 <= len(line.split()) <= 4 and not any(b in line.lower() for b in BLACK_LIST) and line.isalpha():
            return line

    return os.path.basename(file_path).split('.')[0] if file_path else "Unknown" #毫無結果，直接去除副檔名作名字

def clean_text_simple(text):
    if not text: return ""
    tokens = word_tokenize(str(text).lower())
    cleaned = [t for t in tokens if t.isalpha() and t not in STOP_WORDS]
    return ' '.join(cleaned)

# 提取文件內容(除excel)
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

#解析上傳文件，主要功能函式
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
        condidate_name = extract_name_smart(raw_text, file_path)
        clean_resume = clean_text_simple(raw_text)
        profile = {
            'Name': condidate_name,
            'Resume_Text': clean_resume,
            'Raw_Text': raw_text,   # 確保原始文字存在
            'Skills_List': [s for s in all_skills if s in raw_text.lower()],
            'Years_Experience': 0, #須修正
            'Education_Level': 'Bachelor',
            'Job_Role': ''
        }
        results.append(generate_talent_vector(profile))
        
    return results