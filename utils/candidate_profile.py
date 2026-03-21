# utils/candidate_profile.py

import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from .talent_vector import all_skills
from datetime import datetime

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    """文字清理 + NLTK 處理"""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(t.lower()) for t in tokens if t.lower() not in stop_words]
    return ' '.join(tokens)

def extract_skills(text):
    """從文字中抓技能"""
    text_lower = text.lower()
    skills_found = [s for s in all_skills if s in text_lower]
    return skills_found

def extract_years_experience(text):
    """嘗試從文字抓工作年資"""
    matches = re.findall(r'(\d+)\s+(?:years|yrs)\s+(?:of\s+)?experience', text, flags=re.I)
    if matches:
        return int(matches[0])
    #新增:嘗試抓正確年份，因覆蓋問題還未測試
    year_range = re.findall(r'(19\d{2})\s*-\s*(20\d{2}|Present|Current)', text, flags=re.I)
    total_years = 0
    for start, end in year_range:
        start_year = int(start)
        end_year = datetime.now().year if any(x in end.lower() for x in ['present', 'current']) else int(end)
        total_years += (end_year - start_year)
    return total_years if total_years > 0 else 0


def extract_education_level(text):
    """從文字抓教育程度"""
    text_lower = text.lower()
    if 'phd' in text_lower or 'doctor' in text_lower:
        return 'PhD'
    elif 'master' in text_lower or 'msc' in text_lower or 'ma' in text_lower:
        return 'Master'
    elif 'bachelor' in text_lower or 'bsc' in text_lower or 'ba' in text_lower:
        return 'Bachelor'
    else:
        return 'Bachelor'  # 預設值

# 主要功能:建立候選人資料
def create_candidate_profile(row):
    """
    將 CSV row 或單檔案字典轉為統一候選人資料 dict
    """
    resume_text = row.get('Resume_Text', '') or row.get('Resume', '')
    resume_text_clean = clean_text(resume_text)
    
    profile = {
        'Name': row.get('Name', ''),
        'Resume_Text': resume_text_clean,
        'Skills_List': extract_skills(resume_text),
        'Years_Experience': int(row.get('Years_Experience', extract_years_experience(resume_text))),
        'Education_Level': row.get('Education_Level', extract_education_level(resume_text)),
        'Job_Role': row.get('Job_Role', ''),
        'University': row.get('University', '')
    }
    return profile