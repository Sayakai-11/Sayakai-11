from flask import Flask, jsonify, request
import os
import face_recognition
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# 画像保存フォルダ
known_folder = './known'
danger_folder = './danger'
static_known_folder = './images/known'  # フロントエンドに表示するためのフォルダ
static_danger_folder = './images/danger'

# knownフォルダとdangerフォルダの画像をエンコード
known_encodings = []
for filename in os.listdir(known_folder):
    if filename.endswith('.jpg'):
        image = face_recognition.load_image_file(os.path.join(known_folder, filename))
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_encodings.append(encoding[0])

danger_encodings = []
for filename in os.listdir(danger_folder):
    if filename.endswith('.jpg'):
        image = face_recognition.load_image_file(os.path.join(danger_folder, filename))
        encoding = face_recognition.face_encodings(image)
        if encoding:
            danger_encodings.append(encoding[0])

def compare_faces(known_encoding, unknown_encoding):
    """既知の顔と未知の顔を比較する"""
    return face_recognition.compare_faces([known_encoding], unknown_encoding)[0]

# 仮データベース: 誰がどの日に来たかを管理するデータ
visit_data = {
    "2024-10-24": ["known_1.jpg", "danger_2.jpg"],  # 例: 2024年10月24日に来た人物
    "2024-10-25": ["known_3.jpg"],                 # 例: 2024年10月25日に来た人物
    # ここに他の日付データを追加
}

@app.route('/get_photos', methods=['POST'])
def get_photos():
    """特定の日付に来た人物の写真一覧を返す"""
    data = request.get_json()
    date = data.get('date')  # リクエストで送られた日付

    # その日付に対応する写真ファイルを取得（なければ空リスト）
    photo_files = visit_data.get(date, [])

    # 画像のフルパスを作成して返す
    photo_urls = [f"/images/known/{photo}" if 'known' in photo else f"/images/danger/{photo}" for photo in photo_files]

    return jsonify({'photos': photo_urls})

@app.route('/detect', methods=['POST'])
def detect_face():
    """画像を受け取り、既知の人物か危険人物かを判定し、画像を保存"""
    image_file = request.files['image']

    # フレーム送信成功をターミナルに表示
    print("フレームがバックエンドに送信されました")

    # 受け取ったファイルの情報を表示
    print(f"受信したファイルのサイズ: {len(image_file.read())} バイト")
    image_file.seek(0)  # ファイルのポインタを元に戻す

    image = face_recognition.load_image_file(image_file)
    face_encodings = face_recognition.face_encodings(image)

    if not face_encodings:
        print("顔が検出されませんでした")
        return jsonify({'result': 'no_face_detected'})  # 顔が検出されなかった場合

    face_encoding = face_encodings[0]
    result = "unknown"

    # dangerフォルダの顔と比較
    for danger_encoding in danger_encodings:
        if compare_faces(danger_encoding, face_encoding):
            result = "danger"
            print("危険な人物が検出されました！")
            break

    # knownフォルダの顔と比較
    if result == "unknown":
        for known_encoding in known_encodings:
            if compare_faces(known_encoding, face_encoding):
                result = "known"
                print("既知の人物が検出されました")
                break

    # 結果に応じて画像を保存し、そのパスをフロントエンドに返す
    if result == "danger":
        save_path = os.path.join(static_danger_folder, f"danger_{len(danger_encodings) + 1}.jpg")
        image_file.seek(0)
        image_file.save(save_path)
        return jsonify({'result': 'danger', 'image_url': f"/static/images/danger/{os.path.basename(save_path)}"})
    
    elif result == "known":
        save_path = os.path.join(static_known_folder, f"known_{len(known_encodings) + 1}.jpg")
        image_file.seek(0)
        image_file.save(save_path)
        return jsonify({'result': 'known', 'image_url': f"/static/images/known/{os.path.basename(save_path)}"})
    
    return jsonify({'result': 'unknown'})

@app.route('/register', methods=['POST'])
def register_face():
    """未知の人物をknownまたはdangerとして登録"""
    person_type = request.form['person_type']  # 'known' か 'danger'
    image_file = request.files['image']
    
    # ファイルの保存先を設定
    if person_type == 'known':
        save_path = os.path.join(known_folder, f"new_known_{len(known_encodings) + 1}.jpg")
    elif person_type == 'danger':
        save_path = os.path.join(danger_folder, f"new_danger_{len(danger_encodings) + 1}.jpg")

    # 画像を保存
    image_file.save(save_path)
    
    # 保存した画像を再度読み込んでエンコードし、次回以降の認識に使用
    image = face_recognition.load_image_file(save_path)
    encoding = face_recognition.face_encodings(image)
    
    if encoding:
        if person_type == 'known':
            known_encodings.append(encoding[0])
        elif person_type == 'danger':
            danger_encodings.append(encoding[0])

    # ターミナルに登録完了のメッセージを表示
    print(f"{person_type}として登録され、次回の識別に使用されます: {save_path}")

    return jsonify({'message': f'{person_type}として登録されました'})

if __name__ == '__main__':
    app.run(debug=True)
