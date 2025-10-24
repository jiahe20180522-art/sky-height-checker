import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import cv2
from skimage.metrics import structural_similarity as ssim
import cloudinary
import cloudinary.uploader

# --------------------
# 設定
# --------------------
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")
ALLOWED_EXT = {"png", "jpg", "jpeg"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Cloudinary 設定
cloudinary.config(
    cloud_name="Root",
    api_key="318682921687747",
    api_secret="h3RNlITtT8ZGY-cZpEb-rgkHdjM"
)

app = Flask(__name__)
CORS(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# --------------------
# 工具函數
# --------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

def upload_to_cloudinary(file_path):
    result = cloudinary.uploader.upload(file_path)
    return result["secure_url"]  # 圖片網址

def compare_image(upload_path):
    uploaded = cv2.imread(upload_path, cv2.IMREAD_GRAYSCALE)
    best_score = -1
    best_file = None

    for file in os.listdir(DATA_FOLDER):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            ref_path = os.path.join(DATA_FOLDER, file)
            ref_img = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
            ref_img = cv2.resize(ref_img, (uploaded.shape[1], uploaded.shape[0]))
            score = ssim(uploaded, ref_img)
            if score > best_score:
                best_score = score
                best_file = file

    if best_file:
        return os.path.splitext(best_file)[0]
    return None

# --------------------
# 上傳 API
# --------------------
@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"ok": False, "error": "沒有上傳欄位 (image)"}), 400
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"ok": False, "error": "沒有選擇檔案"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)

        # 上傳到 Cloudinary
        cloud_url = upload_to_cloudinary(save_path)

        # 圖片比對
        height_id = compare_image(save_path)

        return jsonify({
            "ok": True,
            "filename": filename,
            "cloud_url": cloud_url,
            "height_id": height_id,
            "message": f"檔案上傳成功，最接近身高編號：{height_id}"
        }), 200

    return jsonify({"ok": False, "error": "檔案類型不允許"}), 400

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

