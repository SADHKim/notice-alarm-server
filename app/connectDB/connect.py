import pymysql

conn = None

def connect(id, pwd, db):
    global conn
    
    conn = pymysql.connect(host='localhost', user=id, passwd=pwd, db=db, charset='utf8')