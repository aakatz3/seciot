#!/usr/bin/env python
import datetime
import time
import json
import urllib2
from iotsec_settings import *
import sqlite3
import sys


class SecIOT():
	def __init__(self, server_host, guid, auth, home_or_mobile,statefile="state.db"):
		self.server_host = server_host
		self.home_or_mobile = home_or_mobile
		self.auth = auth
		self.state_file = statefile
		
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

	def get_server_path(self, home_or_mobile):
		if home_or_mobile == IOT_MOBILE_DEVICE:
			service_path = "mobile"
		elif home_or_mobile == IOT_HOME_NODE:
			service_path = "home"
		else:
			service_path = None
		return service_path

	def poll_state(self, poll_type):
		req = urllib2.Request('http://%s/%s/%s' % (self.server_host, self.get_server_path(poll_type), self.guid))
		req.add_header('Content-Type', 'application/json')

		tmsg = {'guid':self.guid, 'home_or_mobile': poll_type, 'state':self.getvalues()}

		response =  urllib2.urlopen(req, json.dumps(tmsg))

		f = response.read()
		
		print f
	
		for v in json.loads(f)['state']:
			t = self.getvalueall(v[0])
			print t,v
			beforetime = time.mktime(datetime.datetime.strptime(t[2], "%Y-%m-%d %H:%M:%S").timetuple())
			currenttime = time.mktime(datetime.datetime.strptime(v[2], "%Y-%m-%d %H:%M:%S").timetuple())
			if beforetime < currenttime:
				self.setvalue(v[0],v[1])

		return json.loads(f)

	def push_state(self):
		self.dbconn = sqlite3.connect(self.state_file)
		c = self.dbconn.cursor()
		c.execute("select * from valuetables where modified=1")
		rc = c.rowcount
		print "rowcount %d" % rc

		req = urllib2.Request('http://%s/%s/%s' % (self.server_host, self.service_path, self.guid))
		req.add_header('Content-Type', 'application/json')

#		if rc > 0:
		if 1:
			c.execute("update valuetables set modified=0")
			self.dbconn.commit()
			
			print 'URL http://%s/%s/%s' % (self.server_host, self.service_path, self.guid)

			tmsg = {'guid':self.guid, 'home_or_mobile': self.home_or_mobile, 'state':self.getvalues()}

			response =  urllib2.urlopen(req, json.dumps(tmsg))
			r =  response.read()
			self.dbconn.close()
			return r
#		else:
#			tmsg = {'guid':self.guid, 'home_or_mobile': self.home_or_mobile}
#			response =  urllib2.urlopen(req, json.dumps(tmsg))
#			r =  response.read()
#			self.dbconn.close()
#			return 	self.getvalues()

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
	foobar = SecIOT("osrsrv.aakportfolio.com","sfasdasdfa","enc_key" , IOT_MOBILE_DEVICE);

#	foobar = SecIOT("127.0.0.1:5000","sfasdasdfa","enc_key" , IOT_HOME_NODE);
#	foobar = SecIOT("127.0.0.1:5000","sfasdasdfa","enc_key" , IOT_MOBILE_DEVICE);
	
#	status = int(sys.argv[1])
#	print status

	if int(sys.argv[1]):
		status = True
	else:
		status = False

	foobar.setvalue("switch1",status)
	foobar.setvalue("switch2",status)
	foobar.setvalue("switch3",status)
	foobar.setvalue("switch4",status)
	foobar.setvalue("switch5",status)

	print foobar.push_state()

	print "home", foobar.poll_state(IOT_HOME_NODE)

	print "mobile", foobar.poll_state(IOT_MOBILE_DEVICE)
	
	print foobar.getvalues()
