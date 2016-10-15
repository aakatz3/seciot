#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import socket
from datetime import datetime
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from PIL import Image

def internet(host="8.8.8.8", port=53, timeout=3):
   """
   Host: 8.8.8.8 (google-public-dns-a.google.com)
   OpenPort: 53/tcp
   Service: domain (DNS/TCP)
   """
   try:
     socket.setdefaulttimeout(timeout)
     socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
     return True
   except Exception as ex:
     print ex.message
     return False
def die():
	GPIO.output(26,1)
	time.sleep(10)
	GPIO.cleanup()
	exit()

# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# GPIO Setup
GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(17, GPIO.OUT)
GPIO.output(17,0)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27,0)
GPIO.setup(25, GPIO.OUT)
GPIO.output(25,0)
GPIO.setup(19, GPIO.OUT)
GPIO.output(19,0)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26,0)
GPIO.setup(6, GPIO.OUT)
GPIO.output(6,0)

# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

# Initialize display library.
disp.begin(contrast=60)

# Clear display.
disp.clear()
disp.display()



try:
	while True:
		if(GPIO.input(4) == 1):
			GPIO.output(17,1)
		else:
			GPIO.output(17,0)
		if(internet()):
			GPIO.output(6, 1)
		else:
			GPIO.output(6,0)
		if GPIO.input(20) == 1:
			# Load image and convert to 1 bit color.
			image = Image.open('happycat_lcd.ppm').convert('1')
			GPIO.output(19,1)
			# Display image.
			disp.image(image)
	        	disp.display()
		else:
		        disp.clear()
  		        disp.display()
		        GPIO.output(19,0)
    

		if GPIO.input(21) == 1:
			loopsleft = 5
			leds = { 1 : 17, 2 : 27, 3 : 6, 4 : 25, 5 : 26 }
			for led in leds.values():
				GPIO.output(led, 0)
			steptime = datetime.now().microsecond + 10000
			while GPIO.input(21) == 1:
				if(datetime.now().microsecond >= steptime):
					if(loopsleft == 0):
						time.sleep(5)
						die()
					else:
						steptime = datetime.now().microsecond + 1000
						GPIO.output(leds[loopsleft], 1)
						loopsleft = loopsleft - 1
				#else:
					#print steptime
					#print datetime.now().microsecond
			for led in leds.values():
				GPIO.output(led, 0)
				time.sleep(0.5)
		time.sleep(0.01)
except KeyboardInterrupt:
	die(disp)