import cv2
import mediapipe as mp
import numpy as np

# Mediapipeのセットアップ
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

def is_sunglasses_region(roi, frame, eye_region_top_left):
    """検出領域がサングラスかどうかを識別し、指定された領域を四角で囲む"""
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # 二値化した画像を保存
    cv2.imwrite("binary_image.jpg", bw)

    # 目の領域を横方向に5分割し、中央の白ピクセル割合と外側の黒ピクセル割合を計算
    h, w = bw.shape
    segment_1 = bw[:, :2 * w // 5]         # 左端の領域
    segment_3_1 = bw[:, 2 * w // 5: 3 * w // 5]  # 真ん中の領域
    segment_3 = segment_3_1[h // 3:, :]  # 下2/3を取得
    segment_5 = bw[:, 3 * w // 5:]     # 右端の領域

    # 真ん中領域の白ピクセル割合（下2/3の部分を含む）
    white_pixel_count_segment_3 = np.sum(segment_3 == 255)  # 真ん中領域の白ピクセル数
    total_pixel_count_segment_3 = segment_3.size  # 真ん中領域の総ピクセル数
    white_pixel_ratio = white_pixel_count_segment_3 / total_pixel_count_segment_3 if total_pixel_count_segment_3 > 0 else 0

    # 左端の黒ピクセル割合
    black_pixel_count_segment_1 = np.sum(segment_1 == 0)  # 左端の黒ピクセル数
    total_pixel_count_segment_1 = segment_1.size  # 左端の総ピクセル数
    black_pixel_ratio_1 = black_pixel_count_segment_1 / total_pixel_count_segment_1 if total_pixel_count_segment_1 > 0 else 0

    # 右端の黒ピクセル割合
    black_pixel_count_segment_5 = np.sum(segment_5 == 0)  # 右端の黒ピクセル数
    total_pixel_count_segment_5 = segment_5.size  # 右端の総ピクセル数
    black_pixel_ratio_5 = black_pixel_count_segment_5 / total_pixel_count_segment_5 if total_pixel_count_segment_5 > 0 else 0

    # 外側の黒ピクセル割合の平均
    black_pixel_ratio = (black_pixel_ratio_1 + black_pixel_ratio_5) / 2 if black_pixel_ratio_1 > 0 and black_pixel_ratio_5 > 0 else 0

    # 結果の表示（デバッグ用）
    print(f"真ん中の白ピクセル割合: {white_pixel_ratio:.2f}")
    print(f"左端の黒ピクセル割合: {black_pixel_ratio_1:.2f}")
    print(f"右端の黒ピクセル割合: {black_pixel_ratio_5:.2f}")
    print(f"外側の黒ピクセル割合の平均: {black_pixel_ratio:.2f}")

    # 左から2つ分の領域の左上と右下の座標を設定
    segment_1_2_top_left = (eye_region_top_left[0], eye_region_top_left[1])
    segment_1_2_bottom_right = (eye_region_top_left[0] + 2 * w // 5, eye_region_top_left[1] + h)
    cv2.rectangle(frame, segment_1_2_top_left, segment_1_2_bottom_right, (255, 255, 0), 2)  # 黄色で描画

    # 下2/3部分の左上と右下の座標を計算
    segment_3_top_left = (eye_region_top_left[0] + 2 * w // 5, eye_region_top_left[1] + h // 3)
    segment_3_bottom_right = (eye_region_top_left[0] + 3 * w // 5, eye_region_top_left[1] + h)
    cv2.rectangle(frame, segment_3_top_left, segment_3_bottom_right, (255, 255, 255), 2)  # 白色で描画
     
    # 右から2つ分の領域の左上と右下の座標を設定
    segment_4_5_top_left = (eye_region_top_left[0] + 3 * w // 5, eye_region_top_left[1])
    segment_4_5_bottom_right = (eye_region_top_left[0] + 5 * w // 5, eye_region_top_left[1] + h)
    cv2.rectangle(frame, segment_4_5_top_left, segment_4_5_bottom_right, (255, 255, 0), 2)  # 黄色で描画

    # 黒と白のピクセル割合を表示
    print(f"白ピクセル割合: {white_pixel_ratio:.2f}")
    print(f"黒ピクセル割合: {black_pixel_ratio:.2f}")
          
    # 白ピクセル割合と黒ピクセル割合が一定以上であればサングラスがあると判定
    if white_pixel_ratio > 0.3 and black_pixel_ratio > 0.7:  # 白ピクセル割合と黒ピクセル割合の条件
        return True
    return False

def detect_accessories_from_frame(frame):
    """フレームから顔を検出し、目の領域にサングラスがあるかを判定する"""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    has_sunglasses = False

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape
            # 顔全体の境界を取得
            x_min = int(min([landmark.x for landmark in face_landmarks.landmark]) * w)
            y_min = int(min([landmark.y for landmark in face_landmarks.landmark]) * h)
            x_max = int(max([landmark.x for landmark in face_landmarks.landmark]) * w)
            y_max = int(max([landmark.y for landmark in face_landmarks.landmark]) * h)
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)  # 顔全体の四角を青で描画

            # 左目と右目のランドマークID
            left_eye_landmarks = [33, 133, 173, 155, 145, 246, 7, 163, 161, 160, 159, 158, 157, 154, 153]
            right_eye_landmarks = [362, 263, 384, 373, 380, 466, 249, 398, 390, 373, 374, 385, 386, 387, 388]

            try:
                left_eye_coords = [(int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)) for i in left_eye_landmarks]
                right_eye_coords = [(int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)) for i in right_eye_landmarks]
            except IndexError:
                print("ランドマークの座標が取得できませんでした。")
                continue

            # 目の領域の上端と下端はランドマークに基づき、横幅を顔全体に拡大し、縦の幅を2倍に拡張
            eye_top = min(left_eye_coords[0][1], right_eye_coords[1][1]) - 10  # 目の上端
            eye_bottom = max(left_eye_coords[1][1], right_eye_coords[0][1]) + 10  # 目の下端
            eye_height = eye_bottom - eye_top
            eye_region_top_left = (x_min, eye_top - eye_height // 2)  # 縦の幅を2倍に拡張
            eye_region_bottom_right = (x_max, eye_bottom + eye_height // 2)  # 縦の幅を2倍に拡張

            # 目の領域を描画し、ROIを拡大した目の領域で設定
            cv2.rectangle(frame, eye_region_top_left, eye_region_bottom_right, (0, 255, 0), 2)
            roi_eye = frame[eye_region_top_left[1]:eye_region_bottom_right[1], eye_region_top_left[0]:eye_region_bottom_right[0]]

            if roi_eye.size > 0 and is_sunglasses_region(roi_eye, frame, eye_region_top_left):
                has_sunglasses = True
                cv2.rectangle(frame, eye_region_top_left, eye_region_bottom_right, (0, 255, 0), 2)  # サングラス領域の四角を緑で描画

    return has_sunglasses, frame

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("カメラが起動できませんでした。")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        has_sunglasses, frame_with_detections = detect_accessories_from_frame(frame)
        
        print(f"Sunglasses detected: {'Yes' if has_sunglasses else 'No'}")

        if has_sunglasses:
            cv2.imwrite("sunglasses_detected.jpg", frame_with_detections)
            print("サングラスの検出領域を保存しました: sunglasses_detected.jpg")
        else:
            cv2.imwrite("sunglasses_detected.jpg", frame_with_detections)

        if input("Press 'q' and Enter to quit, or just Enter to continue: ") == 'q':
            break

    cap.release()
