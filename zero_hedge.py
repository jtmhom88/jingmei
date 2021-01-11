#!/usr/bin/python
# -*- coding: utf-8 -*-

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
from datasources import datasources
import pprint as pp
# For parsing website
import re, urllib2, httplib, socket
from bs4 import BeautifulSoup
from urlparse import urljoin
from cookielib import CookieJar
import json

# Configs
# Load Env Variables if they exist, otherwise use local configs
try:
	mysql_user = os.environ['MYSQL_USER']
	mysql_pwd = os.environ['MYSQL_PWD']
	mysql_ip = os.environ['MYSQL_IP']
	#mysql_ip = os.environ['MYSQL_IPLOCAL']
	myconf = {"user": mysql_user,
	    "password":mysql_pwd,
	    "host":mysql_ip}
	pass
except Exception, e:
	myconf = { 
	#"user":"root",
	"user":"bexxx",
	"password":"mixxx",
	"host":"127.0.0.1"
	#"host":"54.244.239.236"
	}
	print "Cannot find env varibles",e
	print "Using local configs"
	pass


def upsert_paths(conn, urlstring):
	#Build opener with a cookie processor (required for some sites)
	cj = CookieJar()
	newopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	newopener.addheaders = [('User-agent',
                      'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.5.0')]
	o = urllib2.Request(urlstring)
	datasource='zerohedge'
	#pp.pprint(o)

	try:
		response = newopener.open(o, timeout=5)
		soup = BeautifulSoup(response.read())

	except urllib2.HTTPError:
		print('HTTPError')
	except urllib2.URLError:
		print('URLError')
	except httplib.IncompleteRead:
		print('IncompleteRead')
	except ValueError:
		print ('ValueError (bad URL?)')
	except socket.timeout:
		print('timeout')
	except socket.error:
		print('Socket error')
	finally:
		print "Got zerohedge article links "
	# Find the json that contain "path" key
	find_string = soup.body.findAll(text=re.compile(r'(.*)(?<=\"path\":\")([\w|\_|/|-]+)?(?=\")'), limit=100)
	line = find_string[0]
	#pp.pprint(line)
	#print "length= ", len(line)
	json_obj = json.loads(line)
	#pp.pprint(json_obj)
	#pp.pprint(json_obj['props']['pageProps']['results'])
	pageslist=json_obj['props']['pageProps']['results']
	#print "pageslist length: ",len(pageslist)
	#pp.pprint(pageslist)
	for page in pageslist:
		url = 'https://www.zerohedge.com'+page['path'].encode('utf-8')
		datasource='zerohedge'
		title=page['title'].encode('utf-8')
		print "path: ",url, "title: ",title
		insert_url(conn, url, datasource, title)
	return (len(pageslist))
			
if __name__ == '__main__':
	print myconf
	conn = mysql.connector.connect(**myconf) # Choose connection config set
	
	zeropages=['https://www.zerohedge.com','https://www.zerohedge.com/page/1','https://www.zerohedge.com/page/2','https://www.zerohedge.com/page/3','https://www.zerohedge.com/page/4','https://www.zerohedge.com/page/5','https://www.zerohedge.com/page/6','https://www.zerohedge.com/page/7','https://www.zerohedge.com/page/8','https://www.zerohedge.com/page/9','https://www.zerohedge.com/page/10']

	for page in zeropages:
		print "page: ",page
		ret = upsert_paths(conn, page)
		print "number of pages inserted: ",ret
exit

