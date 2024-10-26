from flask import Flask, jsonify, request
from datetime import datetime
import os
import face_recognition
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 画像保存フォルダ
known_folder = './known'
danger_folder = './danger'
static_known_folder = './static/images/known'  # フロントエンドに表示するためのフォルダ
static_danger_folder = './static/images/danger'

# 初回起動時にstaticフォルダの画像をエンコード
known_encodings = []
for filename in os.listdir(static_known_folder):
    if filename.endswith('.jpg'):
        image = face_recognition.load_image_file(os.path.join(static_known_folder, filename))
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_encodings.append(encoding[0])

danger_encodings = []
for filename in os.listdir(static_danger_folder):
    if filename.endswith('.jpg'):
        image = face_recognition.load_image_file(os.path.join(static_danger_folder, filename))
        encoding = face_recognition.face_encodings(image)
        if encoding:
            danger_encodings.append(encoding[0])


def generate_filename(prefix):
    """カウント、日付、時間を含むファイル名を生成"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{prefix}_{timestamp}.jpg"



@app.route('/detect', methods=['POST'])
def detect_face():
    """画像を受け取り、既知の人物か危険人物かを判定し、画像を保存"""
    image_file = request.files['image']
    image = face_recognition.load_image_file(image_file)
    face_encodings = face_recognition.face_encodings(image)

    if not face_encodings:
        return jsonify({'result': 'no_face_detected'})

    face_encoding = face_encodings[0]
    result = "unknown"

    # dangerフォルダの顔と比較
    for danger_encoding in danger_encodings:
        if face_recognition.compare_faces([danger_encoding], face_encoding)[0]:
            result = "danger"
            break

    # knownフォルダの顔と比較
    if result == "unknown":
        for known_encoding in known_encodings:
            if face_recognition.compare_faces([known_encoding], face_encoding)[0]:
                result = "known"
                break

    # 結果に応じて画像を保存し、そのパスをフロントエンドに返す
    if result == "danger":
        save_path = os.path.join(static_danger_folder, generate_filename("danger"))
        image_file.seek(0)
        image_file.save(save_path)
        return jsonify({'result': 'danger', 'image_url': save_path.replace('./static', '')})

    elif result == "known":
        save_path = os.path.join(static_known_folder, generate_filename("known"))
        image_file.seek(0)
        image_file.save(save_path)
        return jsonify({'result': 'known', 'image_url': save_path.replace('./static', '')})

    return jsonify({'result': 'unknown'})

@app.route('/register', methods=['POST'])
def register_face():
    """未知の人物をknownまたはdangerとして登録"""
    person_type = request.form['person_type']  # 'known' か 'danger'
    image_file = request.files['image']
    
    # ファイルの保存先を設定
    if person_type == 'known':
        save_path = os.path.join(known_folder, generate_filename("known"))
        known_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(image_file))[0])
    elif person_type == 'danger':
        save_path = os.path.join(danger_folder, generate_filename("danger"))
        danger_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(image_file))[0])

    # 画像を保存
    image_file.save(save_path)

    return jsonify({'message': f'{person_type}として登録されました'})

if __name__ == '__main__':
    app.run(debug=True)
