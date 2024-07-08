from flask import Flask, request, jsonify
import requests
import logging
from charts import * 
import datetime

app = Flask(__name__)

instruction_msg = "In this astrological data: SR = Solar Return, LR = Lunar Returns, h = house, z = zodiac sign, d = degrees in sign. All degree values are rounded to one decimal place."

def get_timezone(lat, lng):
    api_key = 'YOUR_OPEN_CAGE_API_KEY'
    url = f'https://api.opencagedata.com/geocode/v1/json?q={lat}+{lng}&key=1e660713cb444c40ae916eaa55feaf58'
    response = requests.get(url)
    data = response.json()

    # Assuming the request is successful and data is returned
    if data['results']:
        # Extract timezone information from the first result
        timezone = data['results'][0]['annotations']['timezone']['name']
        return timezone
    else:
        return "Timezone information not available."

@app.route('/birth_chart', methods=['POST'])
def birth_chart():
    data = request.json
    birth_date = data.get('date')
    birth_time = data.get('time')
    lat = data.get('lat')
    lng = data.get('lng')
    print("data received")
    tz = get_timezone(lat, lng)
    print("get tz")
    if tz == "Timezone information not available.":
        return jsonify({'status': 'error', 'message': 'Invalid timezone information'}), 400
    
    try:
        print("trying")
        # natal houses
        natal_info, natal_ascmc = astro_charts(to_jd_ut(birth_date, birth_time, tz), float(lat), float(lng))
        print("trying second")
        # yearly info
        years_dict = get_yearly_info(datetime.date.today().year, tz, float(lat), float(lng), natal_info, birth_date, birth_time)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    
    result = {
        "": instruction_msg,
        "natal_chart": natal_info,
        "natal_ascmc": natal_ascmc,
        "yearly_info": years_dict
    }
    return jsonify(result)

@app.route('/birth_chart_enriched', methods=['POST'])
def birth_chart_enriched():
    try:
        data = request.json
        birth_date = data.get('date')
        birth_time = data.get('time')
        lat = data.get('lat')
        lng = data.get('lng')       
        tz = get_timezone(lat, lng)
        if tz == "Timezone information not available.":
            return jsonify({'status': 'error', 'message': 'Invalid timezone information'}), 400
        natal_info, natal_ascmc = astro_charts(to_jd_ut(birth_date, birth_time, tz), float(lat), float(lng))
        years_dict = get_biyearly_info(datetime.date.today().year, tz, float(lat), float(lng), natal_info, birth_date, birth_time)        
        result = {
            "": instruction_msg,
            "natal_chart": natal_info,
            "natal_ascmc": natal_ascmc,
            "yearly_info": years_dict
        }
        
        return jsonify(result)
    
    except Exception as e:
        logging.error(f"Error in birth_chart_enriched: {str(e)}", exc_info=True)
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
