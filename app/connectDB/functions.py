import pymysql

from .db_email import *
from .db_user import *
from .db_website import *
from .db_notice import *

conn = None


def connect(id, pwd, db):
    global conn
    conn = pymysql.connect(host='localhost', user=id, passwd=pwd, db=db, charset='utf8')

def disconnect():
    global conn
    conn = None

## db_email ##
def push_email(user, email, website):
    return p_email(conn, user, email, website)
    
def delete_email(user, email, website):
    return d_email(conn, user, email, website)
    
    
## db_user ##
def push_user(info):
    return p_user(conn, info)
    
def update_user(info):
    return u_user(conn, info)
    
def get_user_info(user):
    return g_user_info(conn, user)

def id_overlap_check(id):
    return c_id_overlap(conn, id)

def login(userid, userpwd):
    return c_login(conn, userid, userpwd)

## db_website ##
def get_asks():
    return g_asks(conn)

def push_ask(name, url):
    return p_ask(conn, name, url)

def get_user_websites(user):
    return g_user_websites(conn, user)


## db_notice ##
def get_notices():
    return g_notices(conn)

def push_notice(title, content, time):
    return p_notice(conn, title, content, time)