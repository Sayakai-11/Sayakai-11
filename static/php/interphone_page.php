
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>インターフォン</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        #message {
            margin-top: 10px;
            font-size: 24px;
            font-weight: bold;
            position: absolute;
            top: 80%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            padding: 10px 20px;
            border-radius: 10px;
        }
        /* メッセージのクラスによる文字色の設定 */
        .danger {
            color: rgb(255, 0, 0);
        }
        .known {
            color: green;
        }
        .unknown {
            color: black;
        }
        #action-buttons {
            margin-top: 10px; /* メッセージとのスペースを追加 */
            text-align: center; /* ボタンを中央に配置 */
        }
        #audio-choice {
            position: absolute;
            bottom: 10%;
            left: 50%;
            transform: translateX(-50%);
            text-align: center;
        }
        .hidden {
            display: none;
        }

        /* 不在ボタンの設定 */
        .state_wrap{
            margin-top: 20px;
            text-align: right; /* ボタンを右側に配置 */        
        }
        .state_wrap .button{
            color:  #606060; /* 文字色 */
            font-size: 30px; /* フォントサイズ */
            padding: 5px 20px; /* パディングを増やしてボタンを大きくする */
            border: none;
            border-radius: 8px; /* ボタンの角を丸める */
            text-decoration: none; /* リンクの下線を削除 */
        }
        .state_wrap .button:hover {
            background-color: #f09c8a; /* ホバー時の色 */
        }    

    </style>
    <link rel="stylesheet" href="../css/interphone_page_index.css">
</head>

<body class="interphone_style">
    <header class="header">
        <div class="container">
            <a href="top_page.php"> <!-- トップページへのリンク -->
                <img src="../../logo3.png" alt="Logo" class="logo"> <!-- 一つ上の階層から画像を読み込む -->
            </a>
          <ul class="nav">
          <li class="header-hover-color"><a href="suspicious_page.php">不審者</a></li>
            <li class="header-hover-color"><a href="known_page.php">知人</a></li>
            <li class="header-hover-color active"><a href="calender_page.php">カレンダー</a></li>
            <li class="header-hover-color"><a href="interphone_page.php">インターホン</a></li>
            <li class="header-hover-color"><a href="target_danger_page.php">危険人物リスト</a></li>          </ul>
        </div>
    </header>
    <h1 class="title">INTERPHONE</h1>
    <div class="interphone_frame">
        <div class="interphone_camera">
            <video class="img_camera" id="video" autoplay></video><br>
        </div>
        
        <div class="interphone_button_wrap">
        </div>

        <div class="state_wrap">
            <a href="nonstate_interphone_page.php" class="button">在宅</a>
        </div>
    </div>
    <div id="message" class="hidden"></div>
    <div id="action-buttons" class="hidden">
        <button id="known">knownとして登録</button>
        <button id="danger">dangerとして登録</button>
    </div>
    <div id="audio-choice" class="hidden">
        <button id="play-audio">音声を再生</button>
    </div>

    <audio id="absentAudio" src="../audio/rusu.mp3"></audio>
    <audio id="pleaseWaitAudio" src="../audio/please_wait.mp3"></audio> <!--手が離せないときに流す音声-->

    
    <script>
        const video = document.getElementById('video');
        const message = document.getElementById('message');
        const actionButtons = document.getElementById('action-buttons');
        const knownButton = document.getElementById('known');
        const dangerButton = document.getElementById('danger');
        const audioChoice = document.getElementById('audio-choice');
        const playAudioButton = document.getElementById('play-audio');
        const skipAudioButton = document.getElementById('skip-audio');
        const absentAudio = document.getElementById('absentAudio');

        // カメラの映像を取得して表示
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => { video.srcObject = stream; })
            .catch(error => { console.error("カメラの取得に失敗しました:", error); });

        // 音声再生の関数
        function playAbsentAudio() {
            absentAudio.play();
        }

        // 音声が再生中かどうかを示すフラグ
        let isPlayingPleaseWaitAudio = false;

            // フレームを定期的にAPIに送信して結果を取得
        setInterval(async () => {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);

            const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg'));
            const formData = new FormData();
            formData.append('image', blob);

                // /detect APIに画像を送信して結果を受け取る
            const response = await fetch('http://localhost:5000/detect', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            message.classList.remove('hidden');

            // クラスをリセット
            message.classList.remove('danger', 'known', 'unknown'); 

            if (data.result === 'danger') {
                message.textContent = '危険です！';
                message.classList.add('danger'); // 危険な場合は赤色
                actionButtons.classList.add('hidden'); // アクションボタンを非表示
                audioChoice.classList.remove('hidden'); // 音声選択ボタンを表示
                isPlayingPleaseWaitAudio = false; //音声が流れたかを記録するフラグ
            } else if (data.result === 'known') {
                message.textContent = '既知の人物です';
                message.classList.add('known'); // 既知の人物は緑色
                actionButtons.classList.add('hidden'); // アクションボタンを非表示
                audioChoice.classList.add('hidden'); // 音声選択ボタンを非表示

                 // 15秒後に音声を再生
                if(!isPlayingPleaseWaitAudio) {
                    setTimeout(() => {
                        const pleaseWaitAudio = document.getElementById('pleaseWaitAudio');
                        pleaseWaitAudio.play();
                    }, 10000); // 15秒 (15000ミリ秒) 後に再生
                    isPlayingPleaseWaitAudio = true;
                }
            } else if (data.result === 'unknown') {
                message.innerHTML = '未知の人物が検出されました。<br>登録してください。';
                message.classList.add('unknown'); // 未知の人物は黒色
                actionButtons.classList.remove('hidden'); // アクションボタンを表示
                audioChoice.classList.add('hidden'); // 音声選択ボタンを非表示
                isPlayingPleaseWaitAudio = false; 

                knownButton.onclick = () => registerPerson(blob, 'known');
                dangerButton.onclick = () => registerPerson(blob, 'danger');
            } else {
                message.textContent = '顔を映してください。'; // 顔が認識できない場合のメッセージ
                message.classList.add('unknown'); // 未知の人物は黒色
                actionButtons.classList.add('hidden'); // アクションボタンを非表示
                audioChoice.classList.add('hidden'); // 音声選択ボタンを非表示
                isPlayingPleaseWaitAudio = false;
            }
            
        }, 3000); // 3秒ごとにフレームを送信

        // 未知の人物を登録するAPIリクエスト
        async function registerPerson(imageBlob, personType) {
            const formData = new FormData();
            formData.append('image', imageBlob);
            formData.append('person_type', personType);

            const response = await fetch('http://localhost:5000/register', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            alert(data.message);
            actionButtons.classList.add('hidden'); // アクションボタンを非表示
            message.textContent = ''; // メッセージをクリア
        }
        
        // 音声再生ボタンの動作
        playAudioButton.addEventListener('click', () => {
            playAbsentAudio();
            audioChoice.classList.add('hidden'); // 音声選択ボタンを非表示
        });

        // 音声スキップボタンの動作
        skipAudioButton.addEventListener('click', () => {
            audioChoice.classList.add('hidden'); // 音声選択ボタンを非表示
        });

    </script>
</body>
</html>