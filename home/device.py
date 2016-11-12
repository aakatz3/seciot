#!/usr/bin/env python
class IOTDeviceController(object):
	statepool = {"off":0,"on":1,"locked":2,"unlocked":3, "tripped":4, "untripped":5, "tampered":6, "untampered":7}
	devType = {"switch":0, "sensor":1, "entry":2}
	def __init__(self, name):
		self.name = name
		
	
	def export(self):
		return {"devname":self.name, "states":self.states, "type":self.devicetype};
	
	def setState(self, state):
		if(state in statepool):
			self.state = statepool[state]

if __name__ == "__main__":
	foobar = IOTDevice("foo", ["on", "off"], "widget")
	print foobar.export()
	
