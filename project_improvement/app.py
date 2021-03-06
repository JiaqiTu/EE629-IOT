#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, Response
app = Flask(__name__)

from camera_pi import Camera

import Adafruit_DHT
import time

# get data from DHT sensor
def getDHTdata():		
	DHT11Sensor = Adafruit_DHT.DHT11
	DHTpin = 4
	hum, temp = Adafruit_DHT.read_retry(DHT11Sensor, DHTpin)
	
	if hum is not None and temp is not None:
		hum = round(hum)
		temp = round(temp, 1)
	return temp, hum


@app.route("/")
def index():
	timeNow = time.asctime( time.localtime(time.time()) )
	temp, hum = getDHTdata()
	
	templateData = {
      'time': timeNow,
      'temp': temp,
      'hum'	: hum
	}
	return render_template('index.html', **templateData)

@app.route('/camera')
def cam():
	timeNow = time.asctime( time.localtime(time.time()) )
	templateData = {
      'time': timeNow
	}
	return render_template('camera.html', **templateData)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port =8000, debug=True, threaded=True)
