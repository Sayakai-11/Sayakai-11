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
    // ファイル名から拡張子を除いたベース部分と拡張子を取得
    const baseName = fileName.substring(0, fileName.lastIndexOf('.'));
    const extension = fileName.substring(fileName.lastIndexOf('.'));

    // ベース部分を「danger_20241026_121755」までと、それ以降に分ける
    const match = baseName.match(/^(danger_\d{8}_\d{6})(-.*)?$/);
    const mainPart = match ? match[1] : baseName;  // "danger_20241026_121755" の部分
    let suffix = match && match[2] ? match[2].substring(1) : ""; // "-"以降の追加部分、なければ空文字

    // 入力フィールドに、既存の追加部分を表示または空欄で入力
    suffix = prompt("ファイル名の後ろに追加する名前を入力してください", suffix);
    if (suffix !== null) {
        // 新しいファイル名を生成、ベース名に "-" を追加
        const newFileName = mainPart + (suffix ? '-' : '') + suffix + extension;

        // AJAXリクエストでPHPに新しいファイル名を送信してリネーム
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "rename_image.php", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.onload = function () {
            if (xhr.status === 200) {
                // 成功したら表示名を新しい追加部分で更新
                element.innerText = suffix;
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
          <li class="header-hover-color"><a href="suspicious_page.php">不審者</a></li>
            <li class="header-hover-color active"><a href="known_page.php">知人</a></li>
            <li class="header-hover-color"><a href="calender_page.php">カレンダー</a></li>
            <li class="header-hover-color"><a href="interphone_page.php">インターホン</a></li>
            <li class="header-hover-color"><a href="target_danger_page.php">危険人物リスト</a></li>          </ul>
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