#!/usr/bin/python

import sys
import os
import mysql.connector

#########################
# for mysql connection

# config = { 
#      'user': 'xxx', 
#      'password': 'xxx', 
#      'host': 'xxx'
# }

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
def insert_url(connection, url, datasource):
  cursor = connection.cursor(buffered=True) 
  query = "INSERT IGNORE INTO sentiment.article_urls (url,datasource) " \
            "VALUES(%s,%s)"
  #args = ('http://www.wsj.com/articles/the-best-coach-approach-promote-or-poach-1449792464', 'wsj')
  args = (url, datasource)
  cursor.execute(query, args)
  if cursor.lastrowid:
    print('last insert id', cursor.lastrowid)
  else:
    print('last insert id not found, nothing inserted')
  pass

def insert_article_line(connection, url, datasource, article_idx, article_line_no, article_text ):
  cursor = connection.cursor(buffered=True) 
  query = "select count(*) from sentiment.article_lines where article_url = %s AND article_line_no = %s " 
  args = (url, article_line_no)
  try:
    cursor.execute(query, args)
    row = cursor.fetchone()
    exists = row[0]
    pass
  except Exception, e:
    print "Exception: cannot execute query %s" % (query)
    raise e

  pass
  if exists > 0:
    print "Failed: trying to re-insert row"
  else:
    print "inserting"
    try:
      query = "INSERT IGNORE INTO sentiment.article_lines (article_url, datasource, article_idx, article_line_no, article_text) " \
            "VALUES(%s,%s,%s,%s,%s)"
      args = (url,datasource, article_idx,article_line_no,article_text)
      print args
      cursor.execute(query, args)
      if cursor.lastrowid:
        print('last insert id', cursor.lastrowid)
      else:
        print('last insert id not found, nothing inserted')
      pass
    except Exception, e:
      msg = "Exception: Failed to insert query %s" % (query)
      print msg
      raise e
    else:
      pass
    finally:
      pass


# if __name__ == '__main__':
#     connection = connect(config)
#     url='http://www.msn.com/en-us/money/taxes/trump-tax-plan-would-cut-federal-revenue-22percent/ar-BBnPh7Q'
#     datasource='msn'
#     article_idx=58
#     article_line_no=0
#     article_text='Donald Duck'
#     insert_article_line(connection, url, datasource, article_idx, article_line_no, article_text )
#     pass
