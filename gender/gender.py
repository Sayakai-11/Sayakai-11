import cv2
import numpy as np

# 事前に学習済みの性別分類モデル（例えば、OpenCVの性別分類モデルなど）を読み込む
gender_net = cv2.dnn.readNetFromCaffe("./gender_deploy.prototxt", "./gender_net.caffemodel")

# 性別ラベル
GENDER_LIST = ['Male', 'Female']

# 性別を判定する関数
def predict_gender(face_img):
    # 画像をモデルに適したフォーマットに変換
    blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)
    gender_net.setInput(blob)
    gender_preds = gender_net.forward()
    gender = GENDER_LIST[gender_preds[0].argmax()]
    return gender

# 顔画像を読み込む（例：face.jpg）
face_img = cv2.imread('face_1.jpg')
if face_img is not None:
    # 性別を判定して出力
    gender = predict_gender(face_img)
    print(f"Predicted Gender: {gender}")
else:
    print("画像が読み込めませんでした。")
