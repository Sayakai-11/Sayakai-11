<?php
// 元の画像フォルダとコピー先フォルダのパスを指定
$image_folder = "../images/danger/";
$destination_folder = "../images/target_danger/";

if (isset($_POST['fileName'])) {
    $fileName = basename($_POST['fileName']); // ファイル名をサニタイズ

    // 元の画像パスとコピー先パスを設定
    $originalPath = $image_folder . $fileName;
    $destinationPath = $destination_folder . $fileName;

    // ファイルが存在する場合のみコピー
    if (file_exists($originalPath)) {
        if (copy($originalPath, $destinationPath)) {
            echo "コピーが成功しました。";
        } else {
            http_response_code(500);
            echo "コピーに失敗しました。";
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