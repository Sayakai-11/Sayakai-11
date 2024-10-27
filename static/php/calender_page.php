<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>カレンダーページ</title>
    <!-- FullCalendar CSS -->
    <link href="https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.min.css" rel="stylesheet">
    <link rel="stylesheet" href="../css/calender_page_index.css">
    <style>
        .calendar-container {
            margin: 0 auto; /* 左右の余白を自動的に設定 */
            max-width: 1200px; /* 最大幅を設定（必要に応じて調整） */
            padding: 20px; /* 上下の余白を追加（必要に応じて調整） */
        }
        .selected-date {
            margin-top: 20px; /* カレンダーとの間隔を設定 */
            font-size: 1.5em; /* フォントサイズを調整 */
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <a href="top_page.php">
                <img src="../../logo3.png" alt="Logo" class="logo">
            </a>
            <ul class="nav">
                <li class="header-hover-color"><a href="suspicious_page.php">不審者</a></li>
                <li class="header-hover-color"><a href="known_page.php">知人</a></li>
                <li class="header-hover-color active"><a href="calender_page.php">カレンダー</a></li>
                <li class="header-hover-color"><a href="interphone_page.php">インターホン</a></li>
                <li class="header-hover-color"><a href="target_danger_page.php">危険人物リスト</a></li>
            </ul>
        </div>
    </header>
    <h1 class="calendar-title">カレンダー</h1>
    <div class="calendar-container">
        <div id="calendar"></div>
        <div id="selected-date" class="selected-date">選択された日付: なし</div> <!-- ここに選択された日付が表示される -->
    </div>

    <h2 class="picture-title">選択された日付に来た人たちの写真</h2>
    <div id="photo-list">
        <!-- 写真一覧がここに表示されます -->
    </div>

    <!-- FullCalendar JavaScript -->
    <script src="https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.min.js"></script>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            var calendarEl = document.getElementById('calendar');

            // カレンダーの表示
            var calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'dayGridMonth',  // 月表示
                dateClick: function(info) {
                    var date = info.dateStr;  // クリックされた日付
                    document.getElementById('selected-date').innerText = "選択された日付: " + date; // 選択された日付を表示
                    fetchPhotosForDate(date);
                }
            });

            calendar.render();

            // 特定の日付の写真を取得する関数
            function fetchPhotosForDate(date) {
                var year = date.split('-')[0];
                var month = date.split('-')[1];
                var day = date.split('-')[2];

                var fileName = `danger_${year}${month}${day}_154801.jpg`; // 必要に応じて変更。

                var imageUrl = `../images/danger/${fileName}`;

                displayPhotos([imageUrl]); 
            }

            // 写真を表示する関数
            function displayPhotos(photos) {
                const photoList = document.getElementById('photo-list');
                photoList.innerHTML = '';

                photos.forEach(photo => {
                    const img = document.createElement('img');
                    img.src = photo;
                    img.alt = "人物の写真";
                    img.style.maxWidth = "150px"; 
                    img.style.margin = "10px";
                    photoList.appendChild(img);
                });
            }
        });
    </script>
</body>
</html>

