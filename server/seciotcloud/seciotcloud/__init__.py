from iotsec_settings import *
from flask import Flask,request,json
import os
import hashlib
import sqlite3

SQL_DB_PATH = '/var/www/seciotcloud/seciotcloud/iotsec.db'
#SQL_DB_PATH = '/Users/phar/andrew/iotsec.db'


#import pycrypto
                                                                                                                                            
app = Flask(__name__)                                                                                                                        


#
#
#  /service/{GUID}
#

def check_db():
	try:
		conn = sqlite3.connect(SQL_DB_PATH)
		c = conn.cursor()
		c.execute("select * from iotdata");
		c.execute("select * from iotguid")
	except:
		conn = sqlite3.connect(SQL_DB_PATH)
		c = conn.cursor()
		c.execute("create table iotdata(base_guid text,client_or_server integer,msg_time text,state text, node_map text,UNIQUE (base_guid,client_or_server)  ON CONFLICT REPLACE);")
		c.execute("create table iotguid(base_guid text,guid_list text, UNIQUE (base_guid, guid_list)  ON CONFLICT REPLACE);")
		conn.commit()


@app.route("/home/<path>", methods=['GET', 'POST'])                                                                                                                
def home_service(path, redir = 0):
	if(redir == 1):
		print "redirected"
	check_db()
	conn = sqlite3.connect(SQL_DB_PATH)   
	c = conn.cursor()

	if 'state' in request.json:
		c.execute("insert or replace into iotdata (base_guid, client_or_server,msg_time, state) values (?,?,datetime('now','localtime'),?);" , [request.json['guid'], IOT_HOME_NODE, request.get_data()])
		conn.commit()

#	try:
	print request.get_data()
	c.execute("select * from iotdata where base_guid=? and client_or_server=?;" , (request.json['guid'], IOT_MOBILE_DEVICE))
        data = c.fetchone()
        try:
                data = data[3]
        except:
                data = None
               
        if(data == None):
                if(redir == 0):
                        mobile_service(redir = 1)
		else:
			print "RETURNING NONE!"
        return data
#	except:
#		return json.jsonify([])

@app.route("/nodes/get", methods=['POST'])
def get_nodes():
	guid = request.args.get('guid')
	check_db()
	conn = sqlite3.connect(SQL_DB_PATH)   
	c = conn.cursor()
	c.execute("select node_map from iotdata where base_guid=?;", guid)
	return c.fetchone()

		
		
@app.route("/nodes/set", methods=['POST'])
def set_nodes():
	guid = request.json['guid']
	check_db()
	conn = sqlite3.connect(SQL_DB_PATH)   
	c = conn.cursor()
	if request.method == 'POST':
		c.execute("insert or replace into iotdata (base_guid, node_map) values (?,?);" , [guid, request.json[guid_list])
	return get_nodes()
	

@app.route("/mobile/<path>", methods=['GET', 'POST'])                                                                                                                
def mobile_service(path, redir = 0):
	if(redir == 1):
		print "redirecting"
	check_db()
	conn = sqlite3.connect(SQL_DB_PATH)   
	c = conn.cursor()

	if 'state' in request.json:
		c.execute("insert or replace into iotdata (base_guid, client_or_server,msg_time, state) values (?,?,datetime('now','localtime'),?);" , [request.json['guid'],IOT_MOBILE_DEVICE, request.get_data()])
		conn.commit()

#	try:
	c.execute("select * from iotdata where base_guid=? and client_or_server=?;" , [request.json['guid'], IOT_HOME_NODE])
        data = c.fetchone()
        try:
                data = data[3]
        except:
                data = None
               
        if(data == None):
                if(redir == 0):
                        home_service(redir = 1)
		else:
			print "RETURNING NONE!"
        return data
#	except:
#		return json.jsonify([])

@app.route("/")                                                                                                                              
def main():                                                                                                                                  
    return "Hello, world!!!"                                                                                                                 
51
@app.route("/guid/new")
	def new_guid():
		check_db()
		conn = sqlite3.connect(SQL_DB_PATH)
		c = conn.cursor()
		while True:
			guid = hashlib.sha1(os.urandom(100)).hexdigest()
			c.execute("select * from iotguid where base_guid=?;", guid)
			if(c.fetchone() == None):
				guid_list = { IOT_HOME_NODE : set(),  IOT_MOBILE_DEVICE : set(), IOT_CLOUD_SERVICE : set()}
					c.execute("insert or replace into iotguid (base_guid, guid_list) values (?,?);" , [guid, json.dumps(guid_list, ensure_ascii=True)])
					c.commit()
				return guid
		
		

@app.route("/guid/add/<path>", methods=['GET'])
def add_guid(path)
		base_guid = request.args.get('guid')
		guid_type = request.args.get('type')
		check_db()
		conn = sqlite3.connect(SQL_DB_PATH)
		c = conn.cursor()
		c.execute("select guid_list from iotguid where base_guid=?;", guid)
		guid_list = c.fetchone()
		if(guid_list == None):
			return None
		guid_list = json.loads(guid_list)
		loop = True
		new_guid = None
		while loop:
			new_guid = hashlib.sha1(guid + os.urandom(100)).hexdigest()
			c.execute("select * from iotguid where base_guid=?;", new_guid)
			if(c.fetchone() == None):
				loop = False
				for sub_guid_list in guid_list:
					for test_guid in sub_guid_list:
						if test_guid == new_guid:
							loop = True
		guid_list[str(guid_type)].append(new_guid)
		c.execute("insert or replace into iotguid (base_guid, guid_list) values (?,?);" , [guid, json.dumps(guid_list, ensure_ascii=True)])
		c.commit()
		return new_guid
	
	
if __name__ == "__main__":                                                                                                                   
    app.run(host="0.0.0.0",port=80,debug=True)                                                                                                                                
                                                                                                                                             


