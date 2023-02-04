import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
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

        self.map_ll = [55.7031122, 37.5308796]
        self.z = 5
        self.map_l = "map"
        self.map_key = "40d1649f-0493-4b70-98ba-98533de7710b"
        self.refresh_map()

    def refresh_map(self):
        map_params = {
            "ll": ",".join(map(str, self.map_ll)),
            "l": self.map_l,
            "z": self.z
        }
        seasion = requests.Session()
        retry = Retry(total=10, connect=5)
        adapter = HTTPAdapter(max_retries=retry)
        seasion.mount('http://', adapter)
        seasion.mount('https://', adapter)
        responce = seasion.get("https://static-maps.yandex.ru/1.x/", params=map_params)
        with open("tmp.png", mode="wb") as tmp:
            tmp.write(responce.content)
        pixmap = QPixmap()
        pixmap.load("tmp.png")
        self.map.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec())
