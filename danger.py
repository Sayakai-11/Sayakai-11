import http.client
import urllib.parse
import json
import os

headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'BbOmcJHqNtpHjSRV39IRAjKr58o3o01wSPMivEfH6C1loAOUe8W9JQQJ99AJACi0881XJ3w3AAAFACOGObMK',  # 実際のキーに置き換えてください
}

params = urllib.parse.urlencode({
    'visualFeatures': 'Description',
    'language': 'ja',
})

conn = http.client.HTTPSConnection('jphacks24-chocopa.cognitiveservices.azure.com')
image_folder = 'C:\MAMP\htdocs\JPHACKS24-2\static\images\danger_target'
output_data = []

print("開始")

for file_name in os.listdir(image_folder):
    #print(f"処理中のファイル: {file_name}")
    file_path = os.path.join(image_folder, file_name)

    if os.path.isfile(file_path) and file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        base_name = os.path.splitext(file_name)[0]
        text_file_path = os.path.join(image_folder, f"{base_name}.txt")

        if os.path.exists(text_file_path):
            try:
                with open(text_file_path, "r", encoding="utf-8") as file:
                    description = file.read()
                #print(f"{file_name} の説明を読み込みました")
            except Exception as e:
                print(f"エラー: {file_name} の説明を読み込めませんでした: {e}")
        else:
            try:
                with open(file_path, 'rb') as img:
                    #print(f"{file_name} の画像データをAPIに送信中")
                    conn.request("POST", "/vision/v3.1/analyze?%s" % params, img.read(), headers)
                    response = conn.getresponse()
                    
                    if response.status != 200:
                        print(f"APIリクエストエラー: ステータスコード {response.status}")
                        continue
                    
                    caption_data = response.read()
                    data = json.loads(caption_data)
                    description = data.get('description', {}).get('captions', [{}])[0].get('text', 'No description available')
                    #print(f"{file_name} の説明: {description}")
                    
                    with open(text_file_path, "w", encoding="utf-8") as output_file:
                        output_file.write(description)
                    #print(f"{file_name} の説明をテキストファイルに保存しました")
            except Exception as e:
                print(f"{file_name} の処理エラー: {e}")

#print("処理完了")

conn.close()
