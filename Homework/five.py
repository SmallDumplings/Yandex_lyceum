import sys
import requests

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QPixmap


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

        self.map_ll = '55.7031122,37.5308796'
        self.zoom = 5
        self.map_l = "map"
        self.api_key = "40d1649f-0493-4b70-98ba-98533de7710b"

        self.refresh_map()
        self.button.clicked.connect(lambda: self.get_coordinates(self.lineedit.text()))

    def refresh_map(self):
        request = 'https://static-maps.yandex.ru/1.x/'
        map_params = {
            'll': self.map_ll,
            'l': self.map_l,
            'z': 5,
            'size': '450,450',
            'apikey': self.api_key,
            'pt': f'{self.map_ll},vkbkm'
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
        self.map_ll = ','.join(toponym_coordinates.split())
        self.refresh_map()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec())
