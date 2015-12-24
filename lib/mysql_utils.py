#!/usr/bin/python

import sys
import os
import mysql.connector

#########################
# for mysql connection
"""
config = { 
    'user': mysql_user, 
    'password': mysql_pwd, 
    'host': mysql_ip
}
"""

# Pass it a config object, and it returns a connection object
def connect(config):
  # Connecting to Mysql
  try:
    cnx = mysql.connector.connect(**config) 
    pass
  except Exception, e:
    print "Mysql connect error:"
    raise e
  print "Success: connected"
  return cnx
  pass


# Pass it connection, url, and tag, and it inserts it
# tag example 'wsj'
def insert_url(connection, url, tag):
  cursor = connection.cursor(buffered=True) 
  query = "INSERT IGNORE INTO sentiment.article_urls (url,datasource) " \
            "VALUES(%s,%s)"
  #args = ('http://www.wsj.com/articles/the-best-coach-approach-promote-or-poach-1449792464', 'wsj')
  args = (url, tag)
  cursor.execute(query, args)
  if cursor.lastrowid:
    print('last insert id', cursor.lastrowid)
  else:
    print('last insert id not found')
  pass

#if __name__ == '__main__':
#    connect()
