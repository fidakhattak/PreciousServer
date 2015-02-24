# GrovePi + Grove Temperature & Humidity Sensor Pro
# http://www.seeedstudio.com/wiki/Grove_-_Temperature_and_Humidity_Sensor_Pro

import grovepi

# Connect the Grove Temperature & Humidity Sensor Pro to digital port D4
# SIG,NC,VCC,GND
dht_sensor = 2
analog_sensor = 2
while True:
    try:
        [temp_dht,humidity] = grovepi.dht(dht_sensor,1)
        print "dht_temp =", temp_dht, " humidity =", humidity
	analog_temp = grovepi.temp(analog_sensor)
	print "analog_temp = ", analog_temp

    except IOError:
        print "IOError"
