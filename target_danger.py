import http.client
import urllib.parse
import json
import os

headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'BbOmcJHqNtpHjSRV39IRAjKr58o3o01wSPMivEfH6C1loAOUe8W9JQQJ99AJACi0881XJ3w3AAAFACOGObMK',  # ここに実際のサブスクリプションキーを入力
}

params = urllib.parse.urlencode({
    'visualFeatures': 'Description',
    'language': 'ja',  # 日本語で説明を取得
})

# ホスト名のみ指定
conn = http.client.HTTPSConnection('jphacks24-chocopa.cognitiveservices.azure.com')
image_folder = './static/images/target_danger'

# 画像フォルダ内のすべての画像を処理
for file_name in os.listdir(image_folder):
    file_path = os.path.join(image_folder, file_name)

    # 画像ファイルのみ処理する
    if os.path.isfile(file_path) and file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        base_name = os.path.splitext(file_name)[0]
        text_file_path = os.path.join(image_folder, f"{base_name}.txt")

        # 既に説明文がある場合はスキップ
        if os.path.exists(text_file_path):
            print(f"{file_name} の説明は既に存在します。スキップします。")
            continue

        try:
            with open(file_path, 'rb') as img:
                # 最新バージョンのv3.1を使用
                conn.request("POST", "/vision/v3.1/analyze?%s" % params, img.read(), headers)
                response = conn.getresponse()
                caption_data = response.read()
                
                # JSONレスポンスからdescription部分を抽出
                data = json.loads(caption_data)
                description = data.get('description', {}).get('captions', [{}])[0].get('text', 'No description available')
                
                # descriptionをテキストファイルに書き込む
                with open(text_file_path, "w", encoding="utf-8") as output_file:
                    output_file.write(description)
                
                print(f"Description saved to {text_file_path}")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

# 接続を閉じる
conn.close()

