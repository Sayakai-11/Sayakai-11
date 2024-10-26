<?php
$image_folder = "../images/known/";

if (isset($_POST['oldName']) && isset($_POST['newName'])) {
    $oldName = basename($_POST['oldName']);
    $newName = basename($_POST['newName']);

    $oldPath = $image_folder . $oldName;
    $newPath = $image_folder . $newName;

    // ファイルが存在し、新しいファイル名が使用されていない場合のみ名前を変更
    if (file_exists($oldPath) && !file_exists($newPath)) {
        if (rename($oldPath, $newPath)) {
            echo "ファイル名が変更されました。";
        } else {
            http_response_code(500);
            echo "ファイル名の変更に失敗しました。";
        }
    } else {
        http_response_code(400);
        echo "ファイルが見つからないか、新しい名前が既に使用されています。";
    }
} else {
    http_response_code(400);
    echo "リクエストが不正です。";
}
?>
