import os
from flask import Flask, render_template, request, jsonify
from utils.parser import parse_uploaded_file

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

LAST_RESULTS = []

@app.route("/", methods=["GET", "POST"])
def index():
    global LAST_RESULTS
    if request.method == "POST":
        files = request.files.getlist("file")
        all_results = []

        for file in files:
            if file and file.filename != "":
                path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(path)
                try:
                    data_list = parse_uploaded_file(path)
                    all_results.extend(data_list)
                except Exception as e:
                    print(f"Error processing {file.filename}: {e}")

        LAST_RESULTS = all_results
        return render_template("index.html", results=all_results)

    return render_template("index.html", results=None)

@app.route("/get_resume_detail", methods=["POST"])
def get_resume_detail():
    data = request.get_json()
    name = data.get("name")

    if not LAST_RESULTS or not name:
        return jsonify({"success": False, "text": "無暫存資料"})

    for r in LAST_RESULTS:
        # 關鍵：這裡必須回傳Raw_Text給前端顯示
        if r.get("Name") == name:
            return jsonify({"success": True, "text": r.get("Raw_Text", "無內容")})

    return jsonify({"success": False, "text": "查無此人"})

if __name__ == "__main__":
    app.run(debug=True, port=5050)