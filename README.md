## 留守るちゃん
このプロジェクトは、顔認識技術を利用した不審者対策システムです。

## 使用技術一覧

![Python](https://img.shields.io/badge/Python-v3.8.0-blue?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-v3.0.3-lightgrey?style=for-the-badge)
![Flask-CORS](https://img.shields.io/badge/Flask-CORS-v5.0.0-lightgrey?style=for-the-badge)
![face_recognition](https://img.shields.io/badge/face__recognition-v1.3.0-blue?style=for-the-badge)

- **Python**：プログラミング言語
- **Flask**：Pythonの軽量なWebフレームワーク
- **face_recognition**：顔認識ライブラリ
- **HTML / CSS / JavaScript**：フロントエンドの構築

## プロジェクトの概要

本プロジェクトは以下の3つの機能を備えています：

1. **不審者検知**：アップロードされた画像から顔認識を行い、不審者・知人の判定を行います。結果に応じて、画像をフロントエンドに表示します。
2. **登録機能**：判定された未知の人物を、手動で知人または不審者として登録します。
3. **履歴表示**：日付に基づいて、過去の訪問者の画像一覧を表示します。

## 依存パッケージのインストール

以下のコマンドを実行し、依存パッケージをインストールします。

```bash
pip
install -r requirements.txt

```

## ディレクリ構成
project/
├── same3_2.py                          # メインのFlaskアプリケーション
├── static/                             # 静的ファイル（CSS, JS）
│   ├── images/                         # 画像の保存フォルダ
│   │   ├── known/                      # 知人の画像を保存
│   │   └── danger/                     # 不審者の画像を保存
│   ├── css/                            # CSSファイル
|   |   ├── top_page_index.css          # toppageのcss
|   |   ├── suspicious_page_index.css   #不審者ページのcss
|   |   ├── known_page_index.css        #知人ページのcss
|   |   ├── interphone_page_index.css   #インターフォンページのcss
|   |   └── calender_page_index.css     #カレンダーページのcss
|   └── php/                            # フロントエイドのトップページ
│       ├── top_page_index.php          # トップページのhtml
|       ├── suspicious_page.php         #不審者ページのhtml
|       ├── known_page.php              #知人ページのhtml
|       ├── interphone_page.php         #インターフォンページのhtml
|       └── calender_page.php           #カレンダーページのhtml 
├── known/                              # 既知の人物の画像
├── danger/                             # 危険人物の画像
├── requirements.txt                    # 依存パッケージのリスト
└── README.md                           # README

## 開発環境の構築方法
#リポジトリのクローン
```bash
コードをコピーする
git clone https://github.com/username/repository.git
cd repository
```

#仮想環境の作成
```bash
コードをコピーする
python -m venv venv
source venv/bin/activate  # Windowsの場合は venv\Scripts\activate
```

#依存関係のインストール
```bash
コードをコピーする
pip install -r requirements.txt
```

#サーバーの起動
```bash
コードをコピーする
python app.py
```

デフォルトでは、http://127.0.0.1:5000 でアプリケーションが起動します。

##トラブルシューティング
顔が検出されない場合：
画像が明るすぎたり暗すぎたりすると、face_recognitionライブラリが顔を検出できないことがあります。照明や画像の品質を確認してください。
CORSの問題：
フロントエンドとバックエンドが異なるオリジンにある場合、flask_corsの設定が必要です。コード内のCORS(app)の行を確認し、必要に応じて設定を追加してください。
画像保存ディレクトリのパスエラー：
画像保存用のディレクトリが存在しない場合、static/images/knownとstatic/images/dangerディレクトリを手動で作成してください。また、known/とdanger/ディレクトリも同様に作成が必要です。