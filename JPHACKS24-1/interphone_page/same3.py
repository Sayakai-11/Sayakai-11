import cv2
import face_recognition
import os

def load_and_encode_image(image_path):
    """画像を読み込み、顔の特徴をエンコードします。"""
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)
    return encoding[0] if encoding else None  # エンコーディングがなければNoneを返す

def compare_faces(face_encoding1, face_encoding2):
    """2つの顔の特徴を比較し、同一人物かどうかを判断します。"""
    results = face_recognition.compare_faces([face_encoding1], face_encoding2)
    return results[0]

# knownフォルダとdangerフォルダのパス
known_folder = r'C:\Users\hyeji\Desktop\JPHACKS24\known'
danger_folder = r'C:\Users\hyeji\Desktop\JPHACKS24\danger'

# knownの画像をエンコード
known_encodings = []
for filename in os.listdir(known_folder):
    if filename.endswith('.jpg'):
        known_image_path = os.path.join(known_folder, filename)
        encoding = load_and_encode_image(known_image_path)
        if encoding is not None:
            known_encodings.append(encoding)  # エンコーディングを保存

# dangerの画像をエンコード
danger_encodings = []
for filename in os.listdir(danger_folder):
    if filename.endswith('.jpg'):
        danger_image_path = os.path.join(danger_folder, filename)
        encoding = load_and_encode_image(danger_image_path)
        if encoding is not None:
            danger_encodings.append(encoding)  # エンコーディングを保存      

# カメラを起動
video_capture = cv2.VideoCapture(1)

while True:
    # カメラからのフレームを取得
    ret, frame = video_capture.read()
    if not ret:
        break

    # フレームから顔の特徴をエンコード
    unknown_face_encodings = face_recognition.face_encodings(frame)

    # すべての顔を比較
    for unknown_face_encoding in unknown_face_encodings:
        found_match = False
        display_warning = False
        result_text = ""

        # 既知の顔と比較
        for known_face_encoding in known_encodings:
            if compare_faces(known_face_encoding, unknown_face_encoding):
                result_text = "Known"
                found_match = True
                break  # 一致したら比較を終了

        # 危険な顔の場合
        for danger_face_encoding in danger_encodings:
            if compare_faces(danger_face_encoding, unknown_face_encoding):
                result_text = "Danger"
                display_warning = True
                found_match = True
                break  # 一致したら比較を終了

        # 警告メッセージを表示
        if display_warning:
            height, width, _ = frame.shape
            warning_text = "!WARNING!"
            text_size = cv2.getTextSize(warning_text, cv2.FONT_HERSHEY_SIMPLEX, 2, 3)[0]
            text_x = (width - text_size[0]) // 2
            text_y = (height + text_size[1]) // 2
            cv2.putText(frame, warning_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        # どちらにも一致しない場合
        if not found_match:
            result_text = "Unknown face detected! Press 'k' for True (known), 'd' for False (danger)"
            cv2.putText(frame, result_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "Press 'k' for True (known)", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "Press 'd' for False (danger)", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # キー入力の処理
            key = cv2.waitKey(1) & 0xFF
            if key == ord('k'):  # knownフォルダに追加
                save_path = os.path.join(known_folder, f"new_known_{len(known_encodings) + 1}.jpg")
                cv2.imwrite(save_path, frame)  # 現在のフレームを保存
                print(f"顔がknownフォルダに追加されました: {save_path}")
            elif key == ord('d'):  # dangerフォルダに追加
                save_path = os.path.join(danger_folder, f"new_danger_{len(danger_encodings) + 1}.jpg")
                cv2.imwrite(save_path, frame)  # 現在のフレームを保存
                print(f"顔がdangerフォルダに追加されました: {save_path}")
            elif key == ord('q'):  # 'q'キーで終了
                video_capture.release()
                cv2.destroyAllWindows()
                exit()  # プログラムを終了

        # 結果を表示
        if result_text:
            cv2.putText(frame, result_text, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # フレームを表示
    cv2.imshow('Video', frame)

    # 'q'キーを押すとループを終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# リソースの解放
video_capture.release()
cv2.destroyAllWindows()
