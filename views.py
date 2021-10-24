from flask import Blueprint, render_template, request
import requests
from datetime import datetime

from werkzeug.utils import redirect


views = Blueprint(__name__, "views")

@views.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
    
        city = request.form.get('city')
        # print(city)
        if city == "":
            return redirect("/")

        api_key = 'c46d92ceb9e9b915470ab45fc26226b8'

        city_name = city

        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'

        re = requests.get(url)

        row_data = re.json()
        print(row_data)

        if row_data == {'cod': '404', 'message': 'city not found'}:
            return redirect('/')

        # kelvin to celsius
        temp = row_data['main']['temp'] - 273.15
        
        data = {
                    "country_code": row_data['sys']['country'],
                    "city": str(row_data['name']),
                    # "time":str(datetime.now())[0:19],
                    "temp": str(temp)[0:4] + ' °C',
                    "pressure": str(row_data['main']['pressure']),
                    "humidity": str(row_data['main']['humidity']) + ' %',
                    'main': str(row_data['weather'][0]['main']),
                    'description': str(row_data['weather'][0]['description']),
                    'icon': row_data['weather'][0]['icon'],
                }
    else:
        data = {

             }

    return render_template("index.html", data=data)