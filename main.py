from flask import Flask, jsonify, request
from flask_cors import CORS
import face_recognition_service as frs

app = Flask(__name__)
CORS(app)
frs.load_encodings()  # サーバー起動時にエンコードを読み込む

@app.route('/detect', methods=['POST'])
def detect_face():
    """画像を受け取り、既知の人物、危険人物、未知の人物かを判定し、画像を保存"""
    image_file = request.files['image']
    result, image_url = frs.detect_face(image_file)

    if result == 'no_face_detected':
        return jsonify({'result': 'no_face_detected'})
    elif result == 'unknown':
        return jsonify({'result': 'unknown'})
    else:
        return jsonify({'result': result, 'image_url': image_url})

@app.route('/register', methods=['POST'])
def register_face():
    """未知の人物をknownまたはdangerとして登録"""
    person_type = request.form['person_type']
    image_file = request.files['image']
    image_url = frs.register_face(image_file, person_type)

    return jsonify({'message': f'{person_type}として登録されました', 'image_url': image_url})

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
