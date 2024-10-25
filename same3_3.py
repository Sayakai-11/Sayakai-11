from flask import Flask, jsonify, request
import os
import cv2
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 画像保存フォルダ
known_folder = './known'
danger_folder = './danger'
static_known_folder = './images/known'  # フロントエンドに表示するためのフォルダ
static_danger_folder = './images/danger'

# モデルファイルのパス
model_path = "./face_detection_yunet_2023mar_int8.onnx"

# YuNetモデルの読み込み
face_detector = cv2.FaceDetectorYN.create(model_path, "", (0, 0))
known_encodings = []
danger_encodings = []

# 閾値
COSINE_THRESHOLD = 0.363

# knownフォルダとdangerフォルダの画像をエンコード
def load_encodings(folder, encoding_list):
    for filename in os.listdir(folder):
        if filename.endswith('.jpg'):
            img_path = os.path.join(folder, filename)
            image = cv2.imread(img_path)
            height, width, _ = image.shape
            face_detector.setInputSize((width, height))
            
            # 顔検出
            _, faces = face_detector.detect(image)
            if faces is not None and len(faces) > 0:
                # 顔の位置を取得
                x, y, w, h = map(int, faces[0][:4])
                aligned_face = image[y:y+h, x:x+w]  # 顔部分を切り抜き
                face_feature = cv2.resize(aligned_face, (112, 112))  # 特徴量抽出のためにリサイズ
                encoding_list.append(face_feature)

# エンコード済み顔特徴量を読み込み
load_encodings(known_folder, known_encodings)
load_encodings(danger_folder, danger_encodings)

def compare_faces(face_feature, encodings):
    for encoding in encodings:
        score = cv2.norm(face_feature, encoding, cv2.NORM_L2)
        if score < COSINE_THRESHOLD:
            return True
    return False

@app.route('/detect', methods=['POST'])
def detect_face():
    """画像を受け取り、既知の人物か危険人物かを判定し、画像を保存"""
    image_file = request.files['image']
    image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

    height, width, _ = image.shape
    face_detector.setInputSize((width, height))

    # 顔検出
    _, faces = face_detector.detect(image)
    if faces is None:
        print("顔が検出されませんでした")
        return jsonify({'result': 'no_face_detected'})  # 顔が検出されなかった場合

    # 最初に検出された顔を処理
    x, y, w, h = map(int, faces[0][:4])
    aligned_face = image[y:y+h, x:x+w]  # 顔部分を切り抜き
    face_feature = cv2.resize(aligned_face, (112, 112))  # 特徴量抽出のためにリサイズ

    result = "unknown"
    # knownフォルダの顔と比較
    if compare_faces(face_feature, known_encodings):
        result = "known"
        save_path = os.path.join(static_known_folder, f"mew_known_{len(known_encodings) + 1}.jpg")
        image_file.seek(0)
        image_file.save(save_path)
        return jsonify({'result': 'known', 'image_url': f"./images/known/{os.path.basename(save_path)}"})
    
    # dangerフォルダの顔と比較
    elif compare_faces(face_feature, danger_encodings):
        result = "danger"
        save_path = os.path.join(static_danger_folder, f"new_danger_{len(danger_encodings) + 1}.jpg")
        image_file.seek(0)
        image_file.save(save_path)
        return jsonify({'result': 'danger', 'image_url': f"./images/danger/{os.path.basename(save_path)}"})

    return jsonify({'result': 'unknown'})

@app.route('/register', methods=['POST'])
def register_face():
    """未知の人物をknownまたはdangerとして登録"""
    person_type = request.form['person_type']  # 'known' か 'danger'
    image_file = request.files['image']
    image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

    height, width, _ = image.shape
    face_detector.setInputSize((width, height))

    # 顔検出
    _, faces = face_detector.detect(image)
    if faces is None:
        return jsonify({'message': '顔が検出されませんでした'})

    # 最初の顔を登録
    x, y, w, h = map(int, faces[0][:4])
    aligned_face = image[y:y+h, x:x+w]  # 顔部分を切り抜き
    face_feature = cv2.resize(aligned_face, (112, 112))  # 特徴量抽出のためにリサイズ
    save_folder = known_folder if person_type == 'known' else danger_folder
    save_path = os.path.join(save_folder, f"new_{person_type}_{len(known_encodings) + 1}.jpg")
    image_file.seek(0)
    image_file.save(save_path)

    # 特徴量リストに追加
    if person_type == 'known':
        known_encodings.append(face_feature)
    elif person_type == 'danger':
        danger_encodings.append(face_feature)

    return jsonify({'message': f'new_{person_type}として登録されました'})

if __name__ == '__main__':
    app.run(debug=True)

