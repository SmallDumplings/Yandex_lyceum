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
        self.lineedit.move(30, 10)
        self.lineedit.resize(340, 30)
        self.lineedit.setFocusPolicy(Qt.ClickFocus)

        self.but1 = QPushButton("Схема", self)
        self.but1.move(50, 450)
        self.but1.resize(100, 50)
        self.but1.clicked.connect(self.set_type_map)
        self.but1.setFocusPolicy(Qt.NoFocus)

        self.but2 = QPushButton("Спутник", self)
        self.but2.move(190, 450)
        self.but2.resize(100, 50)
        self.but2.clicked.connect(self.set_type_map)
        self.but2.setFocusPolicy(Qt.NoFocus)

        self.but3 = QPushButton("Гибрид", self)
        self.but3.move(340, 450)
        self.but3.resize(100, 50)
        self.but3.clicked.connect(self.set_type_map)
        self.but3.setFocusPolicy(Qt.NoFocus)

        self.button = QPushButton('Search', self)
        self.button.move(370, 10)
        self.button.resize(50, 30)
        self.button.setFocusPolicy(Qt.NoFocus)

        self.but_rest = QPushButton("Restart", self)
        self.but_rest.move(420, 10)
        self.but_rest.resize(50, 30)
        self.but_rest.clicked.connect(self.restart)
        self.but_rest.setFocusPolicy(Qt.NoFocus)

        self.mark_coordinates = [37.617698, 55.755864]

        self.map_ll = [37.617698, 55.755864]
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

    def set_type_map(self):
        sender = self.sender()
        if sender.text() == "Схема":
            self.map_l = "map"
        elif sender.text() == "Спутник":
            self.map_l = "sat"
        elif sender.text() == "Гибрид":
            self.map_l = "skl"
        self.refresh_map()

    def restart(self):
        self.map_ll = [37.617698, 55.755864]
        self.lineedit.setText("Москва")
        self.refresh_map()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec())
