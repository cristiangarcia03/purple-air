import json
import urllib.request
import urllib.parse
import math

def center_split(text: str) -> list:

    text = text.split(' ', 2)
    text.remove('CENTER')

    return text

def center_direct(center: list) -> list:

    if center[0] == 'NOMINATIM':
        center = Center_Nominatim(center[1])
        print(center.display_cords())
        return center.cords()
        
    elif center[0] == 'FILE':
        center = Center_File(center[1])
        print(center.display_cords())
        return center.cords()


def nums_split(text: str) -> int:

    text = text.split(' ')

    return int(text[1])


def aqi_split(text: str) -> int or str:

    if text != 'AQI PURPLEAIR':
        text = text.split(' ')
        return text[2]
    
    else:
        return text

def aqi_direct(text: list or str) -> None:

    if text == "AQI PURPLEAIR":
        data = Aqi_Purpleair()
        return data.data()

    else:
        data = Aqi_File(text)
        return data.data()


def reverse_split(text: str) -> list or str:

    if text != 'REVERSE NOMINATIM':

        text = text.split(' ')
        text.remove('REVERSE')
        text.remove('FILES')

    return text


########################################################################################
########################################################################################
########################################################################################



def get_cords(location: str) -> list:

    text = download_data(_build_a_foward(location))
    text = text[0]
    long = float(text['lon'])
    lat = float(text['lat'])

    return [lat, long]


def get_cords_file(file_name: str) -> str:

    try:
        f = open(file_name, 'r', encoding = 'utf8')
        f = f.read()
        f = json.loads(f)
        
        text = f[0]
        long = float(text['lon'])
        lat = float(text['lat'])

        return [lat, long]
    except:
        print('FAILDED')
        print(file_name)
        print('Missing')
              


def print_cords(lat: float, long: float) -> None:

    d1 = 'N'
    d2 = 'E'

    if lat < 0:
        d1 = 'S'
        lat *= -1
    if long < 0:
        d2 = 'W'
        long *= -1

    return (f'{lat}/{d1} {long}/{d2}')


def download_data(url: str) -> None:
    
    request = urllib.request.Request(url, headers = {"Referer": "https://www.ics.uci.edu/~thornton/ics32/ProjectGuide/Project3/crisag12"})
        
    try:
        response = urllib.request.urlopen(request)
        json_text = response.read().decode(encoding = 'utf-8')
        return json.loads(json_text)

    except IndexError:
        pass
    
    except KeyError:
        pass 
    except urllib.error.HTTPError as e:
        print('FAILDED')
        print(f'{e.code} {url}')
        print('NOT 200')

    finally:
        response.close()


def _build_a_foward(location: str) -> str:

    url = 'https://nominatim.openstreetmap.org/search?'

    parameters = urllib.parse.urlencode([('q', location), ('format', 'json')])

    return url + parameters


def _build_a_reverse(lat: int, long: int) -> str:

    url = 'https://nominatim.openstreetmap.org/reverse?'

    parameters = urllib.parse.urlencode([('lat', lat), ('lon', long), ('format', 'json')])

    return url + parameters


def convert(pm25: float) -> float:

    if pm25 < 12.1:
        x1 = 0
        y1 = 0
        x2 = 12
        y2 = 50
        AQI = y1 + ((y2 - y1)/(x2 - x1)) * (pm25 - x1)
        return _round(AQI)

    elif pm25 < 35.5:
        x1 = 12.1
        y1 = 51
        x2 = 35.4
        y2 = 100
        AQI = y1 + ((y2 - y1)/(x2 - x1)) * (pm25 - x1)
        return _round(AQI)

    elif pm25 < 55.5:
        x1 = 35.5
        y1 = 101
        x2 = 55.4
        y2 = 150
        AQI = y1 + ((y2 - y1)/(x2 - x1)) * (pm25 - x1)
        return _round(AQI)

    elif pm25 < 150.5:
        x1 = 55.5
        y1 = 151
        x2 = 150.4
        y2 = 200
        AQI = y1 + ((y2 - y1)/(x2 - x1)) * (pm25 - x1)
        return _round(AQI)

    elif pm25 < 250.5:
        x1 = 150.5
        y1 = 201
        x2 = 250.4
        y2 = 300
        AQI = y1 + ((y2 - y1)/(x2 - x1)) * (pm25 - x1)
        return _round(AQI)

    elif pm25 < 350.5:
        x1 = 250.5
        y1 = 301
        x2 = 350.4
        y2 = 400
        AQI = y1 + ((y2 - y1)/(x2 - x1)) * (pm25 - x1)
        return _round(AQI)

    elif pm25 < 500.5:
        x1 = 350.5
        y1 = 401
        x2 = 500.5
        y2 = 500
        AQI = y1 + ((y2 - y1)/(x2 - x1)) * (pm25 - x1)
        return _round(AQI)


def distance(lat1, long1, lat2, long2) -> int:

    dlat = (lat1 - lat2) * (math.pi/180)
    dlon = (long1 - long2) * (math.pi/180)
    alat = ((lat1 + lat2) / 2) * (math.pi/180)
    radius = 3958.8

    x = dlon * math.cos(alat)
    d = math.sqrt((x ** 2) + (dlat ** 2)) * radius

    return d


def _round(num: float) -> int:
    
    num = str(num).split('.')
    
    if int(num[1][0]) >= 5:
        num = int(num[0])
        num += 1
    else:
        num = int(num[0])
    
    return num


########################################################################################
########################################################################################
########################################################################################

class Center_Nominatim:
    def __init__(self, location: str):
        self._cords = get_cords(location)
        
    def cords(self):
        return self._cords

    def display_cords(self):
        return f'CENTER {print_cords(self._cords[0], self._cords[1])}'
        

class Center_File:
    def __init__(self, file):
        try:
            self._cords = get_cords_file(file)
        except:
            pass
            
    def cords(self):
        return self._cords

    def display_cords(self):
        return f'CENTER {print_cords(self._cords[0], self._cords[1])}'


class Aqi_Purpleair:
    def __init__(self):
        self._data = download_data('https://www.purpleair.com/data.json')

    def data(self):
        return self._data

class Aqi_File:
    def __init__(self, file):
        try:
            f = open(file, 'r', encoding = 'utf8')
            f = f.read()
            self._data = json.loads(f)
        except:
            print('FAILDED')
            print(file)
            print('MISSING')
            
    def data(self):
        return self._data



class Reverse_Nominatim:
    def __init__(self, cords: list, radius: int, threshold: int, num_of_places: int, data: dict):
        data = data['data']
        moon = []

        for i in data:
            if i[27] != None and i[28] != None:
                if distance(cords[0], cords[1], i[27], i[28]) <= radius:
                    moon.append(i)

        mars = []
        num = 0
        for i in moon:
            if num != num_of_places:
                if type(i[1]) == float:
                    if type(convert(i[1])) == int:
                        if convert(i[1]) > threshold:
                            if i[4] < 36000:
                                if i[25] == 0:
                                    mars.append(i)
                                    num += 1
            else:
                break

        self._locations = mars

    def display(self):

        for i in self._locations:
            print(f'AQI {convert(i[1])}')
            print(print_cords(i[27], i[28]))
            w = download_data(_build_a_reverse(i[27], i[28]))
            print(w['display_name'])

class Reverse_Files:
    def __init__(self, cords: list, files: list, radius: int, threshold: int, num_of_places: int, data: dict):
        
        data = data['data']
        names = []
        moon = []
        for i in files:
            try:
                i = open(i, 'r', encoding = 'utf8')
                i = i.read()
                i = json.loads(i)
                names.append(i['display_name'])
            except:
                print('FAILDED')
                print(i)
                print('MISSING')
        for i in data:
            if type(i[1]) == float:
                if i[27] != None and i[28] != None:
                    if distance(cords[0], cords[1], i[27], i[28]) <= radius:
                        if convert(i[1]) > 10:
                            if i[4] < 36000:
                                if i[25] == 0:
                                    moon.append(i)
        aqi_list = []
        sensor_list = []

        for i in moon:
            sensor_list.append([convert(i[1]), i[27], i[28]])
            aqi_list.append(convert(i[1]))

        aqi_list.sort(reverse = True)
        final = []

        num = num_of_places
        check = True

        while check:
            for i in sensor_list[:]:
                if num == 0:
                    check = False
                if aqi_list[0] == i[0]:
                    final.append(i)
                    aqi_list.remove(aqi_list[0])
                    num -= 1

        self._names = names
        self._info = final

    def display(self):

        for i in range(len(self._names)):
            print(self._info[i][0])
            print(print_cords(self._info[i][1], self._info[i][2]))
            print(self._names[i])
            
            
            

        
