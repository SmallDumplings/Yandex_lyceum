import requests

API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def geocode(address):
    geocoder_req = f'http://geocode-maps.yandex.ru/1.x/'
    geocoder_params = {
        'apikey': API_KEY,
        'geocode': address,
        'format': 'json'
    }
    response = requests.get(geocoder_req, params=geocoder_params)
    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            f'''Ошибка выполнения запроса: {geocoder_req} \n
            http статус {response.status_code} ({response.reason})'''
        )

    features = json_response['response']['GeoObjectCollection']['featureMember']

    return features[0]['GeoObject'] if features else None


def get_coordinate(address):
    toponym = geocode(address)
    if not toponym:
        return None, None

    toponym_coordinates = toponym['Point']['pos']
    toponym_long, toponym_lat = toponym_coordinates.split()
    return float(toponym_long), float(toponym_lat)


def get_ll_span(address):
    toponym = geocode(address)
    if not toponym:
        return None, None

    toponym_coordinates = toponym['Point']['pos']
    toponym_long, toponym_lat = toponym_coordinates.split()
    ll = ','.join([toponym_long, toponym_lat])
    envelope = toponym['boundedBy']['Envelope']
    l, b = envelope['lowerCorner'].split()
    r, t = envelope['upperCorner'].split()
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0
    span = f'{dx},{dy}'
    return ll, span


def search(ll, spn, request, locale='ru_RU'):
    search_api_server = 'https://search-maps.yandex.ru/v1/'
    api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
    search_params = {
        'apikey': api_key,
        'text': request,
        'lang': locale,
        'll': ll,
        'spn': spn,
        'type': 'biz'
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        raise RuntimeError(f'''Ошибка выполнения запроса {search_api_server} \nhttp статус {response.status_code} 
        ({response.reason})''')
    json_response = response.json()
    organizations = json_response['features']
    return organizations
