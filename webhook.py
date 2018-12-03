import json
import os
import requests
import time

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    
    res = makeResponse(req)
    
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeResponse(req):
    #if req.get("queryResult").get("intent") != "CheckWeather":
    #    return {}
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    date_r = parameters.get("date")
    date = date_r[:date_r.index("T")]
    if city is None:
        return None
    r=requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=57de430303f8486f100006d5aa44ffdf')
    json_object = r.json()
    weather=json_object['list']
    condition = ''
    for i in range(0,30):
        if date in weather[i]['dt_txt']:
            condition= weather[i]['weather']['description']
            break
    response = "The forecast for " +city+ " for "+date+" is "+condition
    return {
    "fulfillmentText": response 
    }
     

    #return jsonify(reply)
    #{
    #"speech": speech,
    #"displayText": speech,
    #"source": "apiai-weather-webhook"
    #}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

















