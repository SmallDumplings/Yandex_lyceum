import sys
import requests

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QPixmap
from geocoder import get_coordinate, search


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 500, 500, 500)

        self.map = QLabel(self)
        self.map.resize(400, 400)
        self.map.move(50, 50)

        self.lineedit = QLineEdit('Москва', self)
        self.lineedit.move(50, 10)
        self.lineedit.resize(340, 30)

        self.button = QPushButton('Search', self)
        self.button.move(400, 10)
        self.button.resize(50, 30)

        self.map_ll = [55.7031122, 37.5308796]
        self.z = 5
        self.map_l = "map"
        self.map_key = "40d1649f-0493-4b70-98ba-98533de7710b"

        self.refresh_map()

    def refresh_map(self):
        lon, lat = get_coordinate(self.lineedit.text())
        ll_spn = f'll={lat},{lon}&spn=0.005,0.005'
        address = search(f'{lat},{lon}', '0.005,0.005', 'https://static-maps.yandex.ru/1.x/')
        map_params = {
            "ll": ",".join(map(str, self.map_ll)),
            "l": self.map_l,
            "z": self.z,
            "ll_spn": ll_spn,
            "address": address
        }
        response = requests.get("https://static-maps.yandex.ru/1.x/", params=map_params)
        with open("tmp.png", mode="wb") as tmp:
            tmp.write(response.content)
        pixmap = QPixmap()
        pixmap.load("tmp.png")
        self.map.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec())
