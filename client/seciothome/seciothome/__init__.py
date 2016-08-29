from iotsec_settings import *
from flask import json
from flask import Flask,request
import sqlite3
from seciot import *

SQL_DB_PATH = '/var/www/seciothome/seciothome/iotsec.db'


#import pycrypto
                                                                                                                                            
app = Flask(__name__)                                                                                                                        



@app.route("/setstate", methods=['GET', 'POST'])                                                                                                                
def mobile_service():      

                             
	foobar = SecIOT("osrsrv.aakportfolio.com","sfasdasdfa","enc_key" , IOT_MOBILE_DEVICE, "/var/www/seciothome/seciothome/state_copy.db");
        
	foobar.setvalue(request.args.get('friendly', '') ,request.args.get('state', ''))
        
	print foobar.push_state()
	
	return str(foobar.poll_state(IOT_HOME_NODE))

	
@app.route("/")                                                                                                                              
def main():                                                                                                                                  
        page = "<html>\n"
        page += "<head>\n"
        page += "</head>\n"
        page += "<body>\n"

	#Restore node stuff
	nodefile=open('/var/www/seciothome/seciothome/nodenames.json', 'r')
	nodejson=nodefile.read()
	node_dict = json.loads(nodejson)

	
        for friendly in node_dict.keys():
		for state in [0,1]:
			page += "<a href=\"/setstate?friendly=%s&state=%d\">%s:%d</a><br>\n" % (friendly,state,friendly,state)
        page += "</body>\n"
        page += "</html>\n"

	return page

if __name__ == "__main__":                                                                                                                   
    app.run(host='0.0.0.0',debug=True, port=80)                                                                                                                  
              
                                                                                                                                             


