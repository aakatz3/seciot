#!/usr/bin/python3

activate_this = '/var/www/seciotcloud/seciotcloud/webapp/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/seciotcloud/")

from seciotcloud import app as application
application.secret_key = '01189998819991197253'
