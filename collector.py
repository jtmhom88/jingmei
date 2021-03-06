#!/usr/bin/python

import sys
import os
import mysql.connector
lib_path = os.path.abspath('./lib') # LINUX
sys.path.append(lib_path)
sys.path.append('./conf')
from dict_cursor import DictCursor
from mysql_utils import *
from get_article_urls import *
from get_article_lines import *
from get_wsj_opener import *
from mysql.connector.errors import Error
import datasources

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
	myconf = { 
	"user":"bexxx",
	"password":"raxxx",
	"host":"127.0.0.1"
	}
	print "Cannot find env varibles",e
	print "Using local configs"
	pass


if __name__ == '__main__':
	datasources = datasources.datasources
	print myconf
	conn = mysql.connector.connect(**myconf) # Choose connection config set
	wsjopener = getcookieopener(lib_path+'/cookies.txt')
	article_list = getarticlelist(datasources)
	cookieopeners = {"wsj" : wsjopener, "moneybeat" : wsjopener}
	for k in article_list.iterkeys():
		print k.encode('utf-8'),article_list[k]
		insert_url(conn, k, article_list[k][0], article_list[k][1])

	#Get un-downloaded articles
	relevant_article_list = get_urls_with_codes(conn, 0)
	for j in relevant_article_list:
		articlesource = j[2]
		url = j[1]
		idx = j[0]
		code, lines = getarticlelines(datasources, url, articlesource, cookieopeners)
		update_download_code(conn, idx, code)
		linecount = 1
		for line in lines:
			try:
				insert_article_line(conn, url, articlesource,idx, linecount, line)
				pass
			except mysql.connector.Error as err:
				print "Mysql error no: %s" % repr(err.errno)
				raise
			except Exception, e:
				raise
			else:
				pass
			finally:
				linecount = linecount+1
				pass
			
exit
