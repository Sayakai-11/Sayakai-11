<?php
// 元の画像フォルダとコピー先フォルダのパスを指定
$image_folder = "../images/danger/";
$destination_folder = "../images/danger_target/";

if (isset($_POST['fileName'])) {
    $fileName = basename($_POST['fileName']); // ファイル名をサニタイズ

    // 元の画像パスとコピー先パスを設定
    $originalPath = $image_folder . $fileName;
    $destinationPath = $destination_folder . $fileName;

    // ファイルが存在する場合のみ移動
    if (file_exists($originalPath)) {
        if (rename($originalPath, $destinationPath)) { // ファイルを移動
            echo "ファイルが正常に移動されました。";
        } else {
            http_response_code(500);
            echo "ファイルの移動に失敗しました。";
        }
    } else {
        http_response_code(400);
        echo "ファイルが見つかりません。";
    }
} else {
    http_response_code(400);
    echo "リクエストが不正です。";
}
?>