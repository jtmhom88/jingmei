#import global_config as config
import sys
#sys.path.append(config.local_site_packages_path)
import mysql.connector
from mysql.connector.cursor import MySQLCursor

class DictCursor(MySQLCursor):
    """
    Extension of Mysql cursor class.
    Usage cursor = DictCursor(conn) (where conn is the connection object)
    """
    def print_test(self):
        print "I am a Dict Cursor"
    
    def fetchone(self):
        row = self._fetch_row()
        if row:
            row = self._row_to_python(row)
            return dict(zip(self.column_names,row))
        return None
        
    def fetchmany(self,size=None):
        res = []
        cnt = (size or self.arraysize)
        while cnt > 0 and self._have_unread_result():
            cnt -= 1
            row = self.fetchone()
            if row:
                res.append(row)
            
        return res
    
    def fetchall(self):
        if not self._have_unread_result():
            raise errors.InterfaceError("No result set to fetch from.")
        res = []
        (rows, eof) = self._connection.get_rows()
        self._rowcount = len(rows)
        for i in xrange(0,self.rowcount):
            res.append(dict(zip(self.column_names,self._row_to_python(rows[i]))))
        self._handle_eof(eof)
        return res
