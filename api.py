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
})

# ホスト名のみ指定
conn = http.client.HTTPSConnection('jphacks24-chocopa.cognitiveservices.azure.com')
file_name = './image.jpeg'

try:
    # 画像ファイル名から拡張子を除いたファイル名を取得
    base_name = os.path.splitext(os.path.basename(file_name))[0]
    text_file_path = f"{base_name}.txt"

    with open(file_name, 'rb') as img:
        # 最新バージョンのv3.1を使用
        conn.request("POST", "/vision/v3.1/analyze?%s" % params, img.read(), headers)
        response = conn.getresponse()
        caption_data = response.read()
        
        # JSONレスポンスからdescription部分を抽出
        data = json.loads(caption_data)
        description = data.get('description', {}).get('captions', [{}])[0].get('text', 'No description available')
        
        # 抽出したdescriptionをテキストファイルに書き込む
        with open(text_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(description)
        
        print(f"Description saved to {text_file_path}")
finally:
    conn.close()



