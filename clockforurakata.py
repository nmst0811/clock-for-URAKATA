import sys
from PySide6.QtCore import QTimer, QTime, QDate, Qt
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import (QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSpacerItem, QSizePolicy)

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

        # ウィンドウ設定
        self.setWindowTitle("Clock for URAKATA")
        self.setGeometry(20, 20, 1200, 540)  # 幅を1200に変更
        self.setStyleSheet("background-color: black;")  # 背景色を黒に設定

        # ストップウォッチ用変数
        self.stopwatch_time = 0  # ミリ秒単位で計測
        self.is_running = False  # ストップウォッチが動作しているかどうか
        self.timer = QTimer(self)  # タイマーを作成
        self.timer.timeout.connect(self.update_stopwatch)  # タイマーが10ミリ秒ごとに更新
        self.clock_timer = QTimer(self)  # 時計用タイマーを作成
        self.clock_timer.timeout.connect(self.update_time)  # 時計を毎秒更新

        # メインレイアウト設定
        main_layout = QHBoxLayout(self)

        # 左側のストップウォッチ部分
        left_layout = QVBoxLayout()

        # ストップウォッチ部分にスペーサーを追加して上下中央に配置
        left_layout.addItem(QSpacerItem(
            200, 150, QSizePolicy.Minimum, QSizePolicy.Expanding))  # type: ignore # 上部にスペーサー

        # ストップウォッチのラベル
        self.stopwatch_label = QLabel("00:00:00.00", self)
        self.stopwatch_label.setAlignment(Qt.AlignCenter) # type: ignore
        self.stopwatch_label.setStyleSheet("color: lime;")
        self.stopwatch_label.setFont(
            QFont(font_db.applicationFontFamilies(font_id)[0], 30))

        left_layout.addWidget(self.stopwatch_label)

        # ストップウォッチ部分にスペーサーを追加して下部に配置
        left_layout.addItem(QSpacerItem(
            200, 150, QSizePolicy.Minimum, QSizePolicy.Expanding))  # type: ignore # 下部にスペーサー

        # 時計の表示用ラベル
        layout = QVBoxLayout()
        self.date_label = QLabel(self)
        self.date_label.setAlignment(Qt.AlignCenter) # type: ignore
        self.date_label.setStyleSheet("color: lime;")
        self.date_label.setFont(
            # 日付フォントサイズを小さく設定
            QFont(font_db.applicationFontFamilies(font_id)[0], 70))
        layout.addWidget(self.date_label)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter) # type: ignore
        self.label.setStyleSheet("color: lime;")
        self.label.setFont(QFont(font_db.applicationFontFamilies(
            font_id)[0], 150))  # 時計のフォントサイズを大きく設定
        layout.addWidget(self.label)

        # 中央のレイアウトにスペーサーを追加して上下中央に配置
        central_layout = QVBoxLayout()
        central_layout.addItem(QSpacerItem(
            200, 150, QSizePolicy.Expanding, QSizePolicy.Minimum))  # type: ignore # 上側のスペーサー

        central_layout.addLayout(layout)  # 時計と日付のレイアウト

        central_layout.addItem(QSpacerItem(
            200, 150, QSizePolicy.Expanding, QSizePolicy.Minimum))  # type: ignore # 下側のスペーサー

        # メインレイアウトに追加
        main_layout.addLayout(left_layout)  # 左側のストップウォッチ
        main_layout.addLayout(central_layout)  # 中央の時計と日時
        main_layout.addLayout(self.create_button_layout())  # 右側のボタン

        # タイマーを作成して、毎秒更新
        self.update_time()  # 初期の時刻と日付を表示
        self.clock_timer.start(1000)  # 1秒ごとに更新

    def create_button_layout(self):
        # ボタンを追加
        button_layout = QVBoxLayout()

        # リセットボタン
        self.reset_button = QPushButton("リセット")  # リセットボタン
        self.reset_button.setFixedSize(100, 100)
        self.reset_button.setStyleSheet(
            "border-radius: 50px; background-color: transparent; border: 2px solid lime; color: lime; font-weight: bold;")
        self.reset_button.clicked.connect(self.reset_stopwatch)  # クリック時にリセット
        button_layout.addWidget(self.reset_button, alignment=Qt.AlignCenter) # type: ignore

        # スタート/ストップボタン
        self.start_stop_button = QPushButton("スタート")  # スタート/ストップボタン
        self.start_stop_button.setFixedSize(100, 100)
        self.start_stop_button.setStyleSheet(
            "border-radius: 50px; background-color: transparent; border: 2px solid lime; color: lime; font-weight: bold;")
        self.start_stop_button.clicked.connect(
            self.toggle_stopwatch)  # クリック時にスタートまたはストップ
        button_layout.addWidget(self.start_stop_button,
                                alignment=Qt.AlignCenter) # type: ignore

        # 設定ボタン
        for _ in range(1):
            button = QPushButton("設定") 
            button.setFixedSize(100, 100)
            button.setStyleSheet(
                "border-radius: 50px; background-color: transparent; border: 2px solid lime; color: lime; font-weight: bold;")
            button_layout.addWidget(button, alignment=Qt.AlignCenter) # type: ignore

        return button_layout  # 作成したボタンレイアウトを返す

    def toggle_stopwatch(self):
        """スタート/ストップボタンの機能"""
        if self.is_running:
            self.timer.stop()  # ストップウォッチを停止
            self.start_stop_button.setText("スタート")  # ボタンテキストを変更
        else:
            self.timer.start(10)  # 10ミリ秒ごとに更新
            self.start_stop_button.setText("ストップ")  # ボタンテキストを変更
        self.is_running = not self.is_running  # ストップウォッチの状態を切り替え

    def reset_stopwatch(self):
        """リセットボタンの機能"""
        self.stopwatch_time = 0  # ミリ秒をリセット
        self.stopwatch_label.setText("00:00:00.00")  # ラベルに表示
        if self.is_running:
            self.timer.stop()  # ストップウォッチが動いている場合は停止
            self.is_running = False
            self.start_stop_button.setText("スタート")  # ボタンテキストをスタートに変更

    def update_stopwatch(self):
        """ストップウォッチの時間を更新"""
        self.stopwatch_time += 10  # 10ミリ秒加算
        seconds = (self.stopwatch_time // 1000) % 60
        minutes = (self.stopwatch_time // 60000) % 60
        hours = (self.stopwatch_time // 3600000) % 24
        milliseconds = self.stopwatch_time % 1000
        self.stopwatch_label.setText(f"{hours:02}:{minutes:02}:{seconds:02}.{
                                     milliseconds // 10:02}")  # ラベルに表示

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
