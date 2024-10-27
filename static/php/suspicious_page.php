<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Danger Persons</title>
    <link rel="stylesheet" href="../css/suspicious_page_index.css">
    <style>
        img {
            width: 150px;
            height: auto;
            margin: 10px;
            cursor: pointer;
        }
        #confirmation {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: white;
            padding: 20px;
            border: 2px solid black;
            text-align: center;
        }
        #confirmation button {
            margin: 5px;
        }
    </style>
    <script>
        function showConfirmation(fileName) {
            const confirmation = document.getElementById('confirmation');
            confirmation.style.display = 'block';
            confirmation.setAttribute('data-file', fileName);
        }

        function addToDangerList() {
            const confirmation = document.getElementById('confirmation');
            const fileName = confirmation.getAttribute('data-file');

            // AJAXリクエストでPHPにファイル名を送信してコピーを作成
            const xhr = new XMLHttpRequest();
            xhr.open("POST", "add_to_danger.php", true);
            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xhr.onload = function () {
                if (xhr.status === 200) {
                    alert("危険人物に追加されました。");
                } else {
                    alert("追加に失敗しました。");
                }
                confirmation.style.display = 'none';
            };
            xhr.send("fileName=" + encodeURIComponent(fileName));
        }

        function closeConfirmation() {
            document.getElementById('confirmation').style.display = 'none';
        }
    </script>
</head>
<body>
    <header class="header">
        <div class="container">
            <a href="top_page.php"> <!-- トップページへのリンク -->
                <img src="../../logo3.png" alt="Logo" class="logo"> <!-- 一つ上の階層から画像を読み込む -->
            </a>
          <ul class="nav">
          <li class="header-hover-color active"><a href="suspicious_page.php">不審者</a></li>
            <li class="header-hover-color"><a href="known_page.php">知人</a></li>
            <li class="header-hover-color"><a href="calender_page.php">カレンダー</a></li>
            <li class="header-hover-color"><a href="interphone_page.php">インターホン</a></li>
            <li class="header-hover-color"><a href="danger_target_page.php">危険人物リスト</a></li>          </ul>
        </div>
    </header>
    <h1>危険人物リスト</h1>

    <div id="gallery">
        <?php
        $image_folder = "../images/danger/";
        if (is_dir($image_folder)) {
            if ($handle = opendir($image_folder)) {
                while (false !== ($file = readdir($handle))) {
                    if ($file != '.' && $file != '..' && preg_match('/\.(jpg|jpeg|png|gif)$/i', $file)) {
                        echo '<img src="' . $image_folder . $file . '" alt="' . $file . '" onclick="showConfirmation(\'' . $file . '\')">';
                    }
                }
                closedir($handle);
            }
        }
        ?>
    </div>

    <!-- 確認タブ -->
    <div id="confirmation">
        <p>この人物を危険人物に追加しますか？</p>
        <button onclick="addToDangerList()">追加</button>
        <button onclick="closeConfirmation()">キャンセル</button>
    </div>
</body>
</html>
