#!/usr/bin/env python
import datetime
import time
import json
import urllib2
import sqlite3
import sys
import RPi.GPIO as GPIO
import socket
from datetime import datetime
import iotsec_settings
import seciot
import json
import time
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

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
	time.sleep(1)
	GPIO.cleanup()

def do_reset():
	#Reset to factory!!
	die()


GPIO.setmode(GPIO.BCM)

#Input Pins
TAMPER = 4
RESET = 16
BUTTON = 21

#Output Pins
BUZ = 26
BUTTON_LED = 17
LCD_BACKLIGHT = 19
NET_STATUS = 12
ERR_LED = 20

#Display pins
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0



#Setup pins

for pin in [TAMPER, RESET, BUTTON]:
	GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
for pin in [BUTTON_LED, BUZ, LCD_BACKLIGHT, NET_STATUS, ERR_LED]:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin,0)

# Setup LCD Display
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
disp.begin(contrast=60)
disp.clear()
disp.display()


try:
	while True:
		#Internet monitoring LED
		if(internet()):
			GPIO.output(NET_STATUS, 1)
		else:
			GPIO.output(NET_STATUS,0)

		#Tamper Detection
		if GPIO.input(TAMPER) == 0:
			GPIO.output(BUZ,1)
			GPIO.output(ERR_LED, 1)
		else:
			GPIO.output(BUZ,0)
		
		# LCD output
		if GPIO.input(BUTTON) == 1:
			disp.clear()
			disp.display()
			# Create blank image for drawing.
			# Make sure to create image with mode '1' for 1-bit color.
			image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
			# Get drawing object to draw on image.
			draw = ImageDraw.Draw(image)
			# Draw a white filled box to clear the image.
			draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
			# Load default font.
			font = ImageFont.load_default()
			# Write some text.
			draw.text((8,30), 'Hello World!', font=font)
			# Display image.
			disp.image(image)
			disp.display()
			GPIO.output(LCD_BACKLIGHT, 1)
			GPIO.output(BUTTON_LED, 1)
		else:
			GPIO.output(BUTTON_LED, 0)
			disp.clear()
			disp.display()
			GPIO.output(LCD_BACKLIGHT, 0)

		
		if GPIO.input(RESET) == 1:
			print "reset"
			steptime = datetime.now().microsecond + 5000
			while GPIO.input(RESET) and (steptime < datetime.now().microsecond):
				time.sleep(0.05)
			if GPIO.input(RESET):
				do_reset()
		time.sleep(0.05)
except KeyboardInterrupt:
	die()
