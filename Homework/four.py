import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 500, 500, 500)

        self.map = QLabel(self)
        self.map.resize(400, 400)
        self.map.move(50, 50)

        self.but1 = QPushButton("Схема", self)
        self.but1.move(50, 450)
        self.but1.resize(100, 50)
        self.but1.clicked.connect(self.set_type_map)

        self.but2 = QPushButton("Спутник", self)
        self.but2.move(190, 450)
        self.but2.resize(100, 50)
        self.but2.clicked.connect(self.set_type_map)

        self.but3 = QPushButton("Гибрид", self)
        self.but3.move(340, 450)
        self.but3.resize(100, 50)
        self.but3.clicked.connect(self.set_type_map)

        self.map_ll = [55.7031122, 37.5308796]
        self.zoom = 5
        self.map_l = "map"
        self.delta = 0.5
        self.map_key = "40d1649f-0493-4b70-98ba-98533de7710b"
        self.refresh_map()

    def refresh_map(self):
        map_params = {
            "ll": ",".join(map(str, self.map_ll)),
            "l": self.map_l,
            "z": self.zoom
        }
        seasion = requests.Session()
        retry = Retry(total=10, connect=5)
        adapter = HTTPAdapter(max_retries=retry)
        seasion.mount('http://', adapter)
        seasion.mount('https://', adapter)
        responce = seasion.get("https://static-maps.yandex.ru/1.x/", params=map_params)
        with open("../image/tmp.png", mode="wb") as tmp:
            tmp.write(responce.content)
        pixmap = QPixmap()
        pixmap.load("tmp.png")
        self.map.setPixmap(pixmap)

    def keyPressEvent(self, event):
        key = event.key()
        if event.key() == Qt.Key_PageUp and self.zoom < 17:
            self.zoom += 1
        if event.key() == Qt.Key_PageDown and self.zoom > 0:
            self.zoom -= 1
        if key == Qt.Key_Left:
            self.map_ll[0] -= self.delta
        if key == Qt.Key_Right:
            self.map_ll[0] += self.delta
        if key == Qt.Key_Up:
            self.map_ll[1] += self.delta
        if key == Qt.Key_Down:
            self.map_ll[1] -= self.delta
        self.refresh_map()

    def set_type_map(self):
        sender = self.sender()
        if sender.text() == "Схема":
            self.map_l = "map"
        elif sender.text() == "Спутник":
            self.map_l = "sat"
        elif sender.text() == "Гибрид":
            self.map_l = "skl"
        self.refresh_map()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec())