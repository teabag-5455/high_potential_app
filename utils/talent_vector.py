# utils/talent_vector.py

# 定義技能清單與加權
all_skills = ['python', 'sql', 'machine learning', 'tensorflow', 'numpy', 'scikit-learn', 'statistics', 'nlp', 'data visualization', 'pandas']
important_skills = ['python', 'machine learning', 'sql', 'tensorflow']
education_weights = {'Bachelor': 1, 'Master': 2, 'PhD': 3}
high_potential_roles = ['data scientist', 'ml engineer', 'ai researcher']

def generate_talent_vector(profile: dict) -> dict:
    """
    將解析後的候選人資料轉換為評分向量，並計算總分。
    """
    vector = {}
    
    # --- 1. 基礎資訊傳遞 (關鍵修正點) ---
    # 必須將 Raw_Text 放入回傳的字典中，API 才能讀取到原始內容
    vector['Name'] = profile.get('Name', 'Unknown')
    vector['Raw_Text'] = profile.get('Raw_Text', '')
    
    # --- 2. 技能評分 (Skills Score) ---
    skills_list = profile.get('Skills_List', [])
    skill_score = 0
    for skill in skills_list:
        if skill in all_skills:
            # 重要技能權重為 2，一般技能為 1
            skill_score += 2 if skill in important_skills else 1
    vector['Skills_Score'] = skill_score
    
    # --- 3. 經驗評分 (Experience Score) ---
    # 設定上限為 10 分，避免極端數值影響模型
    years = profile.get('Years_Experience', 0)
    vector['Experience_Score'] = min(int(years), 10)
    
    # --- 4. 教育評分 (Education Score) ---
    edu_level = profile.get('Education_Level', 'Bachelor')
    vector['Education_Score'] = education_weights.get(edu_level, 1)
    
    # --- 5. 職位加分 (Job Role Score) ---
    job_role = profile.get('Job_Role', '').lower()
    vector['JobRole_Score'] = 1 if any(role in job_role for role in high_potential_roles) else 0
    
    # --- 6. 履歷關鍵字加分 (Resume Score) ---
    # 針對 Resume_Text (已清理過的文字) 進行關鍵字掃描
    resume_text_clean = profile.get('Resume_Text', '').lower()
    keywords = ['project', 'lead', 'research', 'deep learning', 'deployment']
    vector['Resume_Score'] = sum([1 for kw in keywords if kw in resume_text_clean])
    
    # --- 7. 總分計算 (Weighted Total Score) ---
    # 公式：技能(x2) + 經驗(x1.5) + 教育(x1.2) + 職位(x2) + 履歷關鍵字(x1)
    total_score = (
        vector['Skills_Score'] * 2 +
        vector['Experience_Score'] * 1.5 +
        vector['Education_Score'] * 1.2 +
        vector['JobRole_Score'] * 2 +
        vector['Resume_Score'] * 1
    )
    
    vector['Total_Score'] = round(total_score, 2)
    
    # --- 8. 高潛力判定 ---
    # 設定門檻，例如總分大於 15 分即為高潛力人才
    vector['High_Potential'] = total_score >= 15
    
    return vector