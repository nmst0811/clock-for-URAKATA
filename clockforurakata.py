import sys
from PySide6.QtCore import QTimer, QTime, QDate, Qt
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import (QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton)

class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()

        # フォントの読み込み
        font_db = QFontDatabase()
        font_path = "./fonts/Let_s_go_Digital_Regular.ttf"  # フォントファイルのパス
        font_id = font_db.addApplicationFont(font_path)

        if font_id == -1:
            print("フォントの読み込みに失敗しました")
        else:
            print("フォントの読み込みに成功しました")

        # 読み込んだフォントを取得して設定
        font = QFont(font_db.applicationFontFamilies(
            font_id)[0], 40)  # 40ポイントのフォント
        self.setFont(font)

        # ウィンドウ設定
        self.setWindowTitle("デジタル時計")
        self.setGeometry(100, 100, 400, 150)  # 幅を400に変更

        self.setStyleSheet("background-color: black;")  # 背景色を黒に設定

        # メインレイアウト設定
        main_layout = QHBoxLayout(self)

        # 左側のストップウォッチ部分
        self.stopwatch_label = QLabel("00:00:00", self)
        self.stopwatch_label.setAlignment(Qt.AlignCenter)
        self.stopwatch_label.setStyleSheet("color: lime;")
        self.stopwatch_label.setFont(
            # フォントサイズを30に
            QFont(font_db.applicationFontFamilies(font_id)[0], 30))

        # 左側のレイアウト
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.stopwatch_label)

        # 右側のボタンを追加
        self.button_layout = QVBoxLayout()
        for _ in range(3):
            button = QPushButton(" ")  # 空のボタン
            button.setFixedSize(50, 50)  # ボタンのサイズを設定
            button.setStyleSheet(
                "border-radius: 25px; background-color: transparent; border: 2px solid black;")  # 丸いボタン
            self.button_layout.addWidget(button, alignment=Qt.AlignCenter)

        # レイアウトを追加
        main_layout.addLayout(left_layout)
        main_layout.addLayout(self.button_layout)

        # 時計の表示用ラベル
        layout = QVBoxLayout()
        self.date_label = QLabel(self)
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setStyleSheet("color: lime;")
        layout.addWidget(self.date_label)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: lime;")
        layout.addWidget(self.label)

        # メインレイアウトに日付と時刻を追加
        main_layout.addLayout(layout)

        # タイマーを作成して、毎秒更新
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)  # 1000ミリ秒 (1秒)

        # 初期の時刻と日付を表示
        self.update_time()

    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        current_date = QDate.currentDate().toString("yyyy/MM/dd ddd")

        self.label.setText(current_time)
        self.date_label.setText(current_date)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec())
