<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Known Persons</title>
    <link rel="stylesheet" href="../css/known_page_index.css">
    <style>
        img {
            width: 150px;
            height: auto;
            margin: 10px;
        }
        .image-container {
            display: inline-block;
            text-align: center;
            margin: 10px;
        }
        .image-container img {
            cursor: pointer;
        }
    </style>
    <script>
        function editFileName(fileName, element) {
            let newFileName = prompt("新しいファイル名を入力してください", fileName);
            if (newFileName) {
                // AJAXリクエストでPHPに新しいファイル名を送信してリネーム
                const xhr = new XMLHttpRequest();
                xhr.open("POST", "rename_image.php", true);
                xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                xhr.onload = function () {
                    if (xhr.status === 200) {
                        // 成功したら表示名を変更
                        element.innerText = newFileName;
                    } else {
                        alert("ファイル名の変更に失敗しました。");
                    }
                };
                xhr.send("oldName=" + encodeURIComponent(fileName) + "&newName=" + encodeURIComponent(newFileName));
            }
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
            <li class="header-hover-color"><a href="suspicious_page.php">危険人物</a></li>
            <li class="header-hover-color"><a href="known_page.php">知人</a></li>
            <li class="header-hover-color"><a href="calender_page.php">カレンダー</a></li>
            <li class="header-hover-color"><a href="interphone_page.php">インターホン</a></li>
          </ul>
        </div>
    </header>
    <h1>既知人物リスト</h1>
    <div id="gallery">
        <?php
        $image_folder = "../images/known/";
        if (is_dir($image_folder)) {
            if ($handle = opendir($image_folder)) {
                while (false !== ($file = readdir($handle))) {
                    if ($file != '.' && $file != '..' && preg_match('/\.(jpg|jpeg|png|gif)$/i', $file)) {
                        // ファイル名から拡張子を除去
                        $fileNameWithoutExt = pathinfo($file, PATHINFO_FILENAME);
                        echo '<div class="image-container">';
                        echo '<img src="' . $image_folder . $file . '" alt="' . $file . '" onclick="editFileName(\'' . $file . '\', this.nextElementSibling)">';
                        echo '<p class="name_style">' . $fileNameWithoutExt . '</p>';
                        echo '</div>';
                    }
                }
                closedir($handle);
            }
        }
        ?>
    </div>
</body>
</html>