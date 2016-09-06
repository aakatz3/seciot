import RPi.GPIO as GPIO
import time
import socket
from datetime import datetime

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


GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(17, GPIO.OUT)
GPIO.output(17,0)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23,0)
GPIO.setup(24, GPIO.OUT)
GPIO.output(24,0)
GPIO.setup(25, GPIO.OUT)
GPIO.output(25,0)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26,0)


try:
	while True:
		if(GPIO.input(4) == 1):
			GPIO.output(17,1)
		else:
			GPIO.output(17,0)
		if(internet()):
			GPIO.output(23, 1)
		else:
			GPIO.output(23,0)
		if GPIO.input(21) == 1:
			steptime = datetime.now().microsecond + 1000
			loopsleft = 5
			leds = { 1 : 17, 2 : 23, 3 : 24, 4 : 25, 5 : 26 }
			for led in leds.values():
				GPIO.output(led, 0)
			while GPIO.input(21) == 1:
				if(datetime.now().microsecond >= steptime):
					if(loopsleft == 0):
						time.sleep(5)
						die()
					steptime = datetime.now().microsecond + 1000
					GPIO.output(leds[loopsleft], 1)
					loopsleft = loopsleft - 1
				else:
					print steptime
					print datetime.now().microsecond
					time.sleep(0.5)
				
		time.sleep(0.01)
except KeyboardInterrupt:
	die()
