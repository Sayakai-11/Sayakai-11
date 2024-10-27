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

        .gallery-item{
            display: flex;
            align-items: center;
            mergin-bottom: 20px;
        }

        .gallery-text{
            mergin-left: 20px;
        }
    </style>
</head>

<body>
    <!-- ヘッダー -->
    <header class="header">
        <div class="container">
            <a href="top_page.php"> <!-- トップページへのリンク -->
                <img src="../../logo3.png" alt="Logo" class="logo"> <!-- 一つ上の階層から画像を読み込む -->
            </a>
          <ul class="nav">
          <li class="header-hover-color"><a href="suspicious_page.php">不審者</a></li>
            <li class="header-hover-color"><a href="known_page.php">知人</a></li>
            <li class="header-hover-color"><a href="calender_page.php">カレンダー</a></li>
            <li class="header-hover-color"><a href="interphone_page.php">インターホン</a></li>
            <li class="header-hover-color active"><a href="target_danger_page.php">危険人物リスト</a></li>
          </ul>
        </div>
    </header>
    <h1>危険人物リスト</h1>

    <div id="gallery">
        <?php
        // 危険人物画像が保存されているフォルダのパス
        $image_folder = "../images/target_danger/";
        

        //画像が保存されているかのフラグ
        $has_image = false;

        // フォルダ内のファイルを取得
        if (is_dir($image_folder)) {
            if ($handle = opendir($image_folder)) {
                while (false !== ($file = readdir($handle))) {
                    // 画像ファイルの拡張子をチェック
                    if ($file != '.' && $file != '..' && preg_match('/\.(jpg|jpeg|png|gif)$/i', $file)) {
                        $has_image = true;

                        //画像ファイル名から拡張子を除いたファイル名を取得
                        $base_name = pathinfo($file, PATHINFO_FILENAME);
                        //対応するテキストファイルのパス
                        $text_file_path = $image_folder . $base_name . '.txt';

                        //テキストファイルの内容を取得
                        $text_content = '';
                        if(file_exists($text_file_path)){
                            $text_content = file_get_contents($text_file_path);
                        }else {
                            $text_content = '説明文が見つかりません。'; //ファイルが見つからない場合
                        }

                        echo '<div class="gallery-item">';
                        echo '<img src="' . $image_folder . $file . '" alt="' . $file . '">';
                        echo '<div class="gallery-text">'.htmlspecialchars($text_content) . '</div>';
                        echo '</div>';
                    }
                }
                closedir($handle);
            }
        }

        //画像が保存されていなかったら「危険人物が保存されていません」と表示
        if(!$has_image){
            echo '<div class="gallery-text">危険人物が保存されていません。</div>';
        }
        ?>
        
    </div>
</body>
</html>