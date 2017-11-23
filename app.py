#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "model.cost":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    mobile_Model = parameters.get("mobile-model")
    online_storeName = parameters.get("online-storeName")
    cost = {'Flipkart':{'Samsung S8':9000,  'Samsung S8 Plus':10000},'Amazon':{'Samsung S8':9500,  'Samsung S8 Plus':10500}}

    speech = "Cost of the model " + mobile_Model + " in " + online_storeName + " is INR " + str(cost[online_storeName][mobile_Model])

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    #print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
