# 不審者の特徴リスト（例として仮の特徴をリストで保持）
suspicious_characteristics = [
    {
        'name': 'John Doe',
        'age': 30,
        'gender': 'male',
        'height': '180cm',
        'hair_color': 'black',
        'clothing': 'black hoodie',
        'reason': '近所での不審な行動が報告されています'
    },
    {
        'name': 'Jane Smith',
        'age': 25,
        'gender': 'female',
        'height': '160cm',
        'hair_color': 'blonde',
        'clothing': 'red jacket',
        'reason': '店舗周辺での万引きの疑い'
    },
    # 他の不審者の特徴を追加
]

def find_suspicious_info(characteristics):
    """
    渡された特徴と一致する不審者情報を検索し、文章を生成します。
    
    Args:
        characteristics (dict): 照合する特徴の辞書（例：{'height': '180cm', 'clothing': 'black hoodie'}）

    Returns:
        str: 一致する不審者情報の文章（見つからない場合はNone）
    """
    for suspicious in suspicious_characteristics:
        match = all(suspicious.get(key) == value for key, value in characteristics.items())
        if match:
            return (f"{suspicious['name']}（{suspicious['age']}歳, {suspicious['gender']}）は、"
                    f"{suspicious['reason']}。身長は{suspicious['height']}、髪の色は{suspicious['hair_color']}で、"
                    f"服装は{suspicious['clothing']}です。")

    return None  # 一致する情報がない場合
