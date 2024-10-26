import cv2
import os
import numpy as np
import mediapipe as mp

# 性別分類モデルの読み込み
gender_net = cv2.dnn.readNetFromCaffe("./gender_deploy.prototxt", "./gender_net.caffemodel")
GENDER_LIST = ['Male', 'Female']

# ファイルの存在確認
print("gender_deploy.prototxt exists:", os.path.exists("./gender_deploy.prototxt"))
print("gender_net.caffemodel exists:", os.path.exists("./gender_net.caffemodel"))

# Mediapipeのセットアップ
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

def predict_gender(face_img):
    """性別を予測する関数"""
    blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)
    gender_net.setInput(blob)
    gender_preds = gender_net.forward()
    gender = GENDER_LIST[gender_preds[0].argmax()]
    return gender

def is_sunglasses_region(roi, frame, eye_region_top_left):
    """サングラスかどうかを識別する関数"""
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    h, w = bw.shape
    white_pixel_ratio = np.sum(bw[h // 3:, 2 * w // 5: 3 * w // 5] == 255) / (bw[h // 3:, 2 * w // 5: 3 * w // 5].size)
    black_pixel_ratio = (np.sum(bw[:, :2 * w // 5] == 0) + np.sum(bw[:, 3 * w // 5:] == 0)) / (2 * (w * h // 5))
    return white_pixel_ratio > 0.3 and black_pixel_ratio > 0.7

def detect_accessories_and_gender_from_image(image_path):
    """画像から性別とサングラスの有無を判定する関数"""
    frame = cv2.imread(image_path)
    if frame is None:
        print("画像が読み込めませんでした。")
        return
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    gender = None
    has_sunglasses = False

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape
            # 顔全体の座標
            x_min = int(min([landmark.x for landmark in face_landmarks.landmark]) * w)
            y_min = int(min([landmark.y for landmark in face_landmarks.landmark]) * h)
            x_max = int(max([landmark.x for landmark in face_landmarks.landmark]) * w)
            y_max = int(max([landmark.y for landmark in face_landmarks.landmark]) * h)
            face_roi = frame[y_min:y_max, x_min:x_max]
            gender = predict_gender(face_roi)  # 性別を予測

            # 目の領域をサングラス検出のために抽出
            left_eye_coords = [(int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)) for i in [33, 133]]
            right_eye_coords = [(int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)) for i in [362, 263]]
            eye_top = min(left_eye_coords[0][1], right_eye_coords[1][1]) - 10
            eye_bottom = max(left_eye_coords[1][1], right_eye_coords[0][1]) + 10
            eye_region_top_left = (x_min, eye_top - (eye_bottom - eye_top) // 2)
            eye_region_bottom_right = (x_max, eye_bottom + (eye_bottom - eye_top) // 2)
            roi_eye = frame[eye_region_top_left[1]:eye_region_bottom_right[1], eye_region_top_left[0]:eye_region_bottom_right[0]]
            
            if roi_eye.size > 0 and is_sunglasses_region(roi_eye, frame, eye_region_top_left):
                has_sunglasses = True
    
    print(f"Predicted Gender: {gender}")
    print(f"Sunglasses detected: {'Yes' if has_sunglasses else 'No'}")

# 実行
detect_accessories_and_gender_from_image("face_1.jpg")
