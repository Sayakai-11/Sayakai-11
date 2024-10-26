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
    </style>
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
    <h1>危険人物リスト</h1>

    <div id="gallery">
        <?php
        // 危険人物画像が保存されているフォルダのパス
        $image_folder = "../images/target_danger/";

        // フォルダ内のファイルを取得
        if (is_dir($image_folder)) {
            if ($handle = opendir($image_folder)) {
                while (false !== ($file = readdir($handle))) {
                    // 画像ファイルの拡張子をチェック
                    if ($file != '.' && $file != '..' && preg_match('/\.(jpg|jpeg|png|gif)$/i', $file)) {
                        echo '<img src="' . $image_folder . $file . '" alt="' . $file . '">';
                    }
                }
                closedir($handle);
            }
        }
        ?>
        
    </div>
</body>
</html>