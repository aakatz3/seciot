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
	except:
		conn = sqlite3.connect(SQL_DB_PATH)
		c = conn.cursor()
		c.execute("create table iotdata(base_guid text,client_or_server integer,msg_time text,state text, node_map text,UNIQUE (base_guid,client_or_server)  ON CONFLICT REPLACE);") 
		conn.commit()


@app.route("/home/", methods=['GET', 'POST'])                                                                                                                
def home_service(redir = 0):
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
		c.execute("insert or replace into iotdata (base_guid, node_map) values (?,?);" , [guid, request.json[node_map]])
	return get_nodes()
	

@app.route("/mobile/", methods=['GET', 'POST'])                                                                                                                
def mobile_service(redir = 0):
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
			c.execute("select * from iotdate where base_guid=?;", guid)
			if(c.fetchone() == None):
				return guid
	
	
	
if __name__ == "__main__":                                                                                                                   
    app.run(host="0.0.0.0",port=80,debug=True)                                                                                                                                
                                                                                                                                             


