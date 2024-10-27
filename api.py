import http.client
import urllib.parse
import json

headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'Your key',  # ここに実際のサブスクリプションキーを入力
}

params = urllib.parse.urlencode({
    'visualFeatures': 'Description',
})

# ホスト名のみ指定
conn = http.client.HTTPSConnection('jphacks24-chocopa.cognitiveservices.azure.com')
file_name = './image.jpeg'

try:
    with open(file_name, 'rb') as img:
        # 最新バージョンのv3.1を使用
        conn.request("POST", "/vision/v3.1/analyze?%s" % params, img.read(), headers)
        response = conn.getresponse()
        caption_data = response.read()
        
        # JSONレスポンスからdescription部分を抽出
        data = json.loads(caption_data)
        description = data.get('description', {}).get('captions', [{}])[0].get('text', 'No description available')
        
        # descriptionをテキストファイルに書き込む
        with open("output.txt", "w", encoding="utf-8") as output_file:
            output_file.write(description)
        
        print("Description saved to output.txt")
finally:
    conn.close()


