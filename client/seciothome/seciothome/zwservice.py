#!/usr/bin/env python
import openzwave
import unicodedata
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from louie import dispatcher, All
import sys
import time
from device import IOTDeviceController
import iotsec_settings
from seciot import *
import json

class ZWDeviceController(IOTDeviceController):
	def louie_network_started(network):
	    print("Hello from network : I'm started : homeid %0.8x - %d nodes were found." % \
        	(network.home_id, network.nodes_count))	

	def louie_network_failed(network):
	    print("Hello from network : can't load :(.")	
	
	def louie_network_ready(network):
	    print("Hello from network : I'm ready : %d nodes were found." % network.nodes_count)
	    print("Hello from network : my controller is : %s" % network.controller)
	    dispatcher.connect(louie_node_update, ZWaveNetwork.SIGNAL_NODE)
	    dispatcher.connect(louie_value_update, ZWaveNetwork.SIGNAL_VALUE)

	def louie_node_update(network, node):
	    print('Hello from node : %s.' % node)

	def louie_value_update(network, node, value):
		print('Hello from value : %s.' % value)
	
		
	def __init__(self, name, location, nodefilename="nodenames.json"):
		IOTDeviceController.__init__(self, name)
		
		#Restore node stuff
		nodefile=open(nodefilename, 'r')
		nodejson=nodefile.read()
		self.node_dict = json.loads(nodejson)

		

		#Init options
		device="/dev/ttyACM0"
		sniff=300.0
		options = ZWaveOption(device, \
		 config_path="/opt/openzwave/config", \
		 user_path=".", cmd_line="")
		options.set_logging(False)
		options.set_console_output(False)
		options.lock()
		#Create a network object
		self.network = ZWaveNetwork(options, autostart=False)
		self.network.set_poll_interval(10,True)
		#We connect to the louie dispatcher
		dispatcher.connect(self.louie_network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
		dispatcher.connect(self.louie_network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
		self.network.start()
		#We wait for the network.
		print "***** Waiting for network to become ready : "
		for i in range(0,300):
			if self.network.state>=self.network.STATE_READY or i == 20:
				print "***** Network is ready"
				break
			else:
				sys.stdout.write(".")
				sys.stdout.flush()
			time.sleep(1.0)
		#We update the name of the controller
		self.network.controller.node.name = name
		self.network.controller.node.location = location	
			
		
	def export(self):
		#list of devices
		#each device has zwavename, friendly name, device type, statepool, currentstates (timestamped)
		#return self.network.nodes
		return self.node_dict.keys()
	
	def readState(self, node):
		print "read",self.node_dict
		print "read",node
		if(type(node) in [str,unicode]):
			nodenum = self.node_dict[node]
		else:
			print type(node)
			nodenum = node
		mynode = self.network.nodes[nodenum]
		for switch in mynode.get_switches():
			state =  mynode.get_switch_state(switch)
			return state;
		
			
	def setState(self, node, state):
		print "set",self.node_dict
		print "set",node
		if(type(node) in [str,unicode]):
			nodenum = self.node_dict[node]
		else:
			nodenum = node
		if state in [1, "1", u'1', True]:
			boolstate = True
		elif state in [0, "0", u'0', False]:
			boolstate = False
		else:
			print state
			print type(state)
			raise error("bad")
		print state
		for switch in self.network.nodes[nodenum].get_switches():
			self.network.nodes[nodenum].set_switch(switch,boolstate)

	
if __name__ == "__main__":
	#Create controller and network service
	zwave = ZWDeviceController(iotsec_settings.IOT_ZWAVE_NAME, iotsec_settings.IOT_ZWAVE_LOCATION)
	zwavepoll = SecIOT("osrsrv.aakportfolio.com","enc_key", IOT_HOME_NODE)

	i = 0
	while True:
		i ^= i
		#for node in zwave.export():
		#	if not zwave.readState(node) == zwavepoll.getvalue(node):
		#		zwavepoll.setvalue(node, zwave.readState(node))

		if i == 0:
#			print zwavepoll.poll_state(IOT_HOME_NODE)
			print zwavepoll.poll_state(IOT_MOBILE_DEVICE)
			for node in zwave.export():
                                anode =node #unicodedata.normalize('NFKD', node).encode('ascii','ignore')
                                zwave.setState(anode, zwavepoll.getvalue(anode))
			time.sleep(0.5)
                else:

                        for node in zwave.export():
				anode = node#unicodedata.normalize('NFKD', node).encode('ascii','ignore')
                                if not zwave.readState(anode) == zwavepoll.getvalue(anode):
					state = zwave.readState(anode)
				print anode,":",state
				zwavepoll.setvalue(anode, state)
                        zwavepoll.push_state()
                        time.sleep(.5)
		time.sleep(0.5)
