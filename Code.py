import sys
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    if request.method == "POST":
        city = request.form["city"]
        api_key = "your_api_key_here"  # Replace with your actual API key
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&lang=fr&appid={api_key}"
            
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = {
                'location': city,
                'forecasts': []
            }
            daily_forecasts = {}
            
            for item in data['list']:
                date = item['dt_txt'].split(" ")[0]
                max_temp = item['main']['temp_max']
                min_temp = item['main']['temp_min']
                sky_condition = item['weather'][0]['description'] 

                if date not in daily_forecasts:
                    daily_forecasts[date] = {
                        'max': max_temp,
                        'min': min_temp,
                        'sky_condition': sky_condition,
                        'count': 1,
                        'total_max': max_temp,
                        'total_min': min_temp,
                    }
                else:
                    daily_forecasts[date]['count'] += 1
                    daily_forecasts[date]['total_max'] += max_temp
                    daily_forecasts[date]['total_min'] += min_temp
                    daily_forecasts[date]['max'] = max(daily_forecasts[date]['max'], max_temp)
                    daily_forecasts[date]['min'] = min(daily_forecasts[date]['min'], min_temp)
                    daily_forecasts[date]['sky_condition'] = sky_condition

            for date, temps in daily_forecasts.items():
                average_temp = (temps['total_max'] / temps['count'] + temps['total_min'] / temps['count']) / 2
                weather['forecasts'].append({
                    'date': date,
                    'max': temps['max'],
                    'min': temps['min'],
                    'average': average_temp,
                    'sky_condition': temps['sky_condition']  
                })
        else:
            weather = {'error': "Zone géographique non trouvée."}

    return render_template("index.html", weather=weather)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
