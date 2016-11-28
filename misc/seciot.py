#!/usr/bin/env python
import datetime
import time
import json
from iotsec_settings import *
import sqlite3
import sys
import requests
class SecIOT():
	def __init__(self, auth, home_or_mobile, guid = None, statefile="state.db"):
		self.server_host = server_host
		self.home_or_mobile = home_or_mobile
		self.auth = auth
		self.state_file = statefile
		self.protocol = protocol

		if guid is None:
			#Restore node stuff
			info=open("info.json", 'r')
	                guid=json.loads(info.read())["guid"];
		try:
			self.getvalues()
		except:
			self.dbconn = sqlite3.connect(self.state_file)
			c = self.dbconn.cursor()
			c.execute("create table valuetables(valname text,valvalue text,valtime text,modified integer);")
			c.execute("CREATE UNIQUE INDEX I1 ON valuetables(valname);")
			self.dbconn.commit()

		service_path = self.get_server_path(home_or_mobile)
		if service_path == None:
			raise "fail"
		else:
			self.service_path = service_path

		self.guid = guid

	@staticmethod
	def geturl(action):
    		return '%s://%s/%s/' % (protocol, server_host, action)


	@staticmethod
	def new_guid(url):
    		return '%s://%s/%s/' % ('https', self.server_host, action)

    		url = SecIOT.geturl('guid/new')
		print url
		r = requests.get(url, verify=cafile)
		self.guid = r.text
		print self.guid
		return self.guid

	def get_server_path(self, home_or_mobile):
		if home_or_mobile == IOT_MOBILE_DEVICE:
			service_path = "mobile"
		elif home_or_mobile == IOT_HOME_NODE:
			service_path = "home"
		else:
			service_path = None
		return service_path

	def poll_state(self, poll_type):
		url = SecIOT.geturl('poll')
		headers = {'Content-Type' : 'application/json'}
		payload = {'guid':self.guid, 'home_or_mobile': poll_type}

		print url

		r = requests.post(url, data=json.dumps(payload), headers=headers, verify=cafile)
	
		print r.text

		for v in r.json()['state']:
			t = self.getvalueall(v[0])
			print t,v
			beforetime = time.mktime(datetime.datetime.strptime(t[2], "%Y-%m-%d %H:%M:%S").timetuple())
			currenttime = time.mktime(datetime.datetime.strptime(v[2], "%Y-%m-%d %H:%M:%S").timetuple())
			if beforetime < currenttime:
				self.setvalue(v[0],v[1])

		return r.json()



	def push_state(self):
		self.dbconn = sqlite3.connect(self.state_file)
		c = self.dbconn.cursor()
		c.execute("select * from valuetables where modified=1")
		rc = c.rowcount
		print "rowcount %d" % rc

		c.execute("update valuetables set modified=0")
		self.dbconn.commit()

		url = SecIOT.geturl('push')
		headers = {'Content-Type' : 'application/json'}
		payload = {'guid':self.guid, 'home_or_mobile': self.home_or_mobile, 'state':self.getvalues()}
		
		print url

		r = requests.post(url, data=json.dumps(payload), headers=headers, verify=cafile)
		print r.text
		self.dbconn.close()
		return r.json()


	def getvalues(self):
		self.dbconn = sqlite3.connect(self.state_file)
		c = self.dbconn.cursor()
		c.execute("select * from valuetables")
		t = c.fetchall()
		self.dbconn.close()
		return t

	def setvalue(self, name, value):
		self.dbconn = sqlite3.connect(self.state_file)
		c = self.dbconn.cursor()
		c.execute("insert or replace into valuetables (valname,valvalue,valtime,modified) values (?,?,datetime('now','localtime'),1)",[name,value])
		self.dbconn.commit()
		self.dbconn.close()
	
	def getvalue(self, name):
		self.dbconn = sqlite3.connect(self.state_file)
		c = self.dbconn.cursor()
		c.execute("select * from valuetables where valname=?",[name])
		t =  c.fetchone()[1]
		self.dbconn.close()
		return t

	def getvalueall(self, name):
		self.dbconn = sqlite3.connect(self.state_file)
		c = self.dbconn.cursor()
		c.execute("select * from valuetables where valname=?",[name])
		t =  c.fetchone()
		self.dbconn.close()
		return t		

	def clearvalues(self):
		self.dbconn = sqlite3.connect(self.state_file)
		c = self.dbconn.cursor()
		c.execute("delete from valuetables")
		self.dbconn.commit()
		self.dbconn.close()



                                                                                                                                           
if __name__ == "__main__":                                                                                                                   
#	foobar = SecIOT("osrsrv.aakportfolio.com","sfasdasdfa","enc_key" , IOT_HOME_NODE);
	foobar = SecIOT("enc_key" , int(sys.argv[2]), guid="sfasdasdfa")
#	foobar = SecIOT("127.0.0.1:5000","sfasdasdfa","enc_key" , IOT_HOME_NODE);
#	foobar = SecIOT("127.0.0.1:5000","sfasdasdfa","enc_key" , IOT_MOBILE_DEVICE);
	
#	status = int(sys.argv[1])
#	print status

	push = True

	if int(sys.argv[1]) == 1:
		status = True
	elif int(sys.argv[1]) == 0:
		status = False
	elif int(sys.argv[1]) == -1:
		push = False

	if push:
		foobar.setvalue("switch1",status)
		foobar.setvalue("switch2",status)
		foobar.setvalue("switch3",status)
		foobar.setvalue("switch4",status)
		foobar.setvalue("switch5",status)
		print foobar.push_state()

	print "home", foobar.poll_state(IOT_HOME_NODE)

	print "mobile", foobar.poll_state(IOT_MOBILE_DEVICE)
	
	print foobar.getvalues()
