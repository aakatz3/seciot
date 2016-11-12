#!/usr/bin/python

import threading
from threading import Thread
import zwservice
import gpiolib

Thread(target = gpiolib.start_gpio()).start()
Thread(target = zwservice.zwservice()).start()
#thread.start_new_thread(gpiolib.start_gpio())
#thread.start_new_thread(zwservice.zwservice())
while True:
	pass
