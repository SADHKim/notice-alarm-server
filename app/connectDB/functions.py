import pymysql

from .db_email import *
from .db_user import *

conn = None


def connect(id, pwd, db):
    global conn
    conn = pymysql.connect(host='localhost', user=id, passwd=pwd, db=db, charset='utf8')

def disconnect():
    global conn
    conn = None

def push_email(user, email, website):
    return p_email(conn, user, email, website)
    
def delete_email(user, email, website):
    return d_email(conn, user, email, website)
    
def push_user(info):
    return p_user(conn, info)
    
def update_user(info):
    return u_user(conn, info)
    
def get_user_info(user):
    return g_user_info(conn, user)