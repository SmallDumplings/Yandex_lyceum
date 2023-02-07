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

        self.map_ll = [55.7031122, 37.5308796]
        self.zoom = 5
        self.map_l = "map"
        self.map_key = "40d1649f-0493-4b70-98ba-98533de7710b"

        self.refresh_map()

    def refresh_map(self):
        geocode_request = 'http://geocode-maps.yandex.ru/1.x/'
        geocode_params = {'apikey': self.map_key,
                          'geocode': self.lineedit.text(),
                          'format': 'json'}
        geocode_response = requests.get(geocode_request, params=geocode_params)
        feature = geocode_response.json()['response']['GeoObjectCollection']['featureMember']
        toponym = feature[0]['GeoObject']
        coordinates = toponym['Point']['pos']
        ll = ','.join(coordinates.split())

        map_params = {'l': self.map_l,
                      'll': ll,
                      'apikey': self.map_key,
                      'zoom': self.zoom}
        request = 'http://static-map.yandex.ru/1.x/'
        response = requests.get(request, params=map_params)
        with open('../Image/tmp.png', mode='wb') as tmp:
            tmp.write(response.content)
        pixmap = QPixmap()
        pixmap.load('tmp.png')
        self.map.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec())
