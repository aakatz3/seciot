from iotsec_settings import *
from flask import json
from flask import Flask,request
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
		c.execute("create table iotdata(home_guid text,client_or_server integer,msg_time text,state text,UNIQUE (home_guid,client_or_server)  ON CONFLICT REPLACE);")
		conn.commit()


@app.route("/home/<path>", methods=['GET', 'POST'])                                                                                                                
def home_service(path, redir = 0):
	check_db()
	conn = sqlite3.connect(SQL_DB_PATH)   
	c = conn.cursor()

	if 'state' in request.json:
		c.execute("insert or replace into iotdata (home_guid, client_or_server,msg_time, state) values (?,?,datetime('now','localtime'),?);" , [request.json['guid'], IOT_HOME_NODE, request.get_data()])
		conn.commit()

#	try:
	print request.get_data()
	c.execute("select * from iotdata where home_guid=? and client_or_server=?" , (request.json['guid'], IOT_MOBILE_DEVICE))
        data = c.fetchone()
        try:
                data = data[3]
        except:
                data = None
               
        if(data == None):
                if(redir == 0):
                        mobile_service(redir = 1)
        return data
#	except:
#		return json.jsonify([])




@app.route("/mobile/<path>", methods=['GET', 'POST'])                                                                                                                
def mobile_service(path, redir = 0):
	check_db()
	conn = sqlite3.connect(SQL_DB_PATH)   
	c = conn.cursor()

	if 'state' in request.json:
		c.execute("insert or replace into iotdata (home_guid, client_or_server,msg_time, state) values (?,?,datetime('now','localtime'),?);" , [request.json['guid'],IOT_MOBILE_DEVICE, request.get_data()])
		conn.commit()

#	try:
	c.execute("select * from iotdata where home_guid=? and client_or_server=?" , [request.json['guid'], IOT_HOME_NODE])
        data = c.fetchone()
        try:
                data = data[3]
        except:
                data = None
               
        if(data == None):
                if(redir == 0):
                        home_service(redir = 1)
        return data
#	except:
#		return json.jsonify([])

@app.route("/")                                                                                                                              
def main():                                                                                                                                  
    return "Hello, world!!!"                                                                                                                 

if __name__ == "__main__":                                                                                                                   
    app.run(host="0.0.0.0",port=8031,debug=True)                                                                                                                                
                                                                                                                                             


