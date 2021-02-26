appid = "4f808e5799b99bd7746b1c9d8eba6898"
import requests

def get_wind_direction(deg):
    l = ['С ','СВ',' В','ЮВ','Ю ','ЮЗ',' З','СЗ']
    for i in range(0,8):
        step = 45.
        min = i*step - 45/2.
        max = i*step + 45/2.
        if i == 0 and deg > 360-45/2.:
            deg = deg - 360
        if deg >= min and deg <= max:
            res = l[i]
            break
    return res

# Проверка наличия в базе информации о нужном населенном пункте
def get_city_id(s_city_name):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                     params={'q': s_city_name, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        #cities = ["{} ({})".format(d['name'], d['sys']['country'])
        #         for d in data['list']]
        #print("city:", cities)
        city_id = data['list'][0]['id']
        #print('city_id=', city_id)
    except Exception as e:
        print("Exception (find):", e)
    assert isinstance(city_id, int)
    return city_id


# Запрос текущей погоды
def request_current_weather(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        print("conditions:", data['weather'][0]['description'])
        print("temp:", data['main']['temp'])
        print("temp_min:", data['main']['temp_min'])
        print("temp_max:", data['main']['temp_max'])
        print("pressure:", data['main']['pressure'])
        print("humidity:", data['main']['humidity'])
        #print("data:", data)
    except Exception as e:
        print("Exception (weather):", e)


# Прогноз
def request_week_forecast(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        print('city:', data['city']['name'], data['city']['country'])
        for i in data['list']:
            print( (i['dt_txt'])[:16], '{0:+3.0f}'.format(i['main']['temp']),
                   '{0:2.0f}'.format(i['wind']['speed']) + " м/с", 
                   get_wind_direction(i['wind']['deg']),
                   i['weather'][0]['description'] )
    except Exception as e:
        print("Exception (forecast):", e)

#city_id for Minsk
#city_id= 625144
import sys
if len(sys.argv) == 3:
    s_city_name = sys.argv[1]
    print("city:", s_city_name)
    city_id = get_city_id(s_city_name)
    print('city_id=', city_id)
    if sys.argv[2] == "now":
        request_current_weather(city_id)
    elif sys.argv[2] == "week":
        request_week_forecast(city_id)
    else:
        print("fuck u")
elif len(sys.argv) > 3:
    print('Enter name of city and type of prediction as one(two) argument(s). For example: Minsk,BY  now(week)')