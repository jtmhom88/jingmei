#!/usr/bin/python

import sys
import os
import mysql.connector
lib_path = os.path.abspath('./lib') # LINUX
sys.path.append(lib_path)
configs_path = os.path.abspath('./conf') # LINUX
sys.path.append(configs_path)
from dict_cursor import DictCursor
from mysql_utils import *
from configs import *

# Configs
# Load Env Variables if they exist, otherwise use local configs
try:
	mysql_user = os.environ['MYSQL_USER']
	mysql_pwd = os.environ['MYSQL_PWD']
	mysql_ip = os.environ['MYSQL_IP']
	myconf = {"user": mysql_user,
            "password":mysql_pwd,
            "host":mysql_ip}
	pass
except Exception, e:
	myconf = mysql_creds['aws1']
	print "Cannot find env varibles",e
	print "Using local configs"
	pass

if __name__ == '__main__':
	print myconf
	conn = mysql.connector.connect(**myconf) # Choose connection config set
	insert_url(conn,'http://wsj.com/randomarticle.htm','wsj')

