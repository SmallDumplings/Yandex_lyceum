import sys
import requests

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 500, 500, 500)

        self.map = QLabel(self)
        self.map.resize(400, 400)
        self.map.move(50, 50)
        self.map.setFocusPolicy(Qt.ClickFocus)

        self.lineedit = QLineEdit('Москва', self)
        self.lineedit.move(50, 10)
        self.lineedit.resize(340, 30)
        self.lineedit.setFocusPolicy(Qt.ClickFocus)

        self.button = QPushButton('Search', self)
        self.button.move(400, 10)
        self.button.resize(50, 30)
        self.button.setFocusPolicy(Qt.NoFocus)

        self.mark_coordinates = [0, 0]

        self.map_ll = [0, 0]
        self.zoom = 5
        self.map_l = "map"
        self.api_key = "40d1649f-0493-4b70-98ba-98533de7710b"

        self.delta = 0.5

        self.refresh_map()
        self.button.clicked.connect(lambda: self.get_coordinates(self.lineedit.text()))

    def refresh_map(self):
        request = 'https://static-maps.yandex.ru/1.x/'
        map_params = {
            'll': ','.join(map(str, self.map_ll)),
            'l': self.map_l,
            'z': self.zoom,
            'size': '450,450',
            'apikey': self.api_key,
            'pt': f'{",".join(map(str, self.mark_coordinates))},vkbkm'
        }
        response = requests.get(request, params=map_params)
        with open('../Image/tmp.png', mode='wb') as tmp:
            tmp.write(response.content)
        pixmap = QPixmap()
        pixmap.load('../Image/tmp.png')
        self.map.setPixmap(pixmap)

    def get_coordinates(self, address):
        geocode_request = f'http://geocode-maps.yandex.ru/1.x/'
        geocode_params = {
            'apikey': self.api_key,
            'geocode': address,
            'format': 'json'
        }
        response = requests.get(geocode_request, params=geocode_params)
        json_response = response.json()
        features = json_response['response']['GeoObjectCollection']['featureMember']
        toponym = features[0]['GeoObject']
        toponym_coordinates = toponym['Point']['pos']
        self.mark_coordinates = list(map(float, toponym_coordinates.split()))
        self.map_ll = list(map(float, toponym_coordinates.split()))
        self.refresh_map()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec())
