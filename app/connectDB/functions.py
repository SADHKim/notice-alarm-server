import pymysql

from .db_email import *
from .db_user import *
from .db_website import *
from .db_notice import *

from conf import DB_ID as id, DB_PWD as pwd, DB_NAME as db

conn = None

def connect():
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

def get_recievers(name):
    return g_recievers(conn, name)
    
    
## db_user ##
def push_user(info):
    return p_user(conn, info)
    
def update_password(user, curr, new):
    return u_password(conn, user, curr, new)

def update_email(user, new):
    return u_email(conn, user, new)
    
def get_user_info(user):
    return g_user_info(conn, user)

def id_overlap_check(id):
    return c_id_overlap(conn, id)

def login(userid, userpwd):
    return c_login(conn, userid, userpwd)

def find_password(id, email):
    return f_password(conn, id, email)

def delete_user(user, password):
    return d_user(conn, user, password)

## db_website ##
def get_asks():
    return g_asks(conn)

def push_ask(name, url):
    return p_ask(conn, name, url)

def delete_ask(url):
    return d_ask(conn, url)

def get_user_websites(user):
    return g_user_websites(conn, user)

def delete_user_webiste(user, website):
    return d_user_website(conn, user, website)

def push_user_website(user, email, name):
    return p_user_website(conn, user, email, name)

def get_websites():
    return g_websites(conn)

def push_website(info):
    return p_website(conn, info)

def delete_website(info):
    return d_website(conn, info)


## db_notice ##
def get_notices():
    return g_notices(conn)

def get_num_notice(num):
    return g_num_notice(conn, num)

def push_notice(title, content, time):
    return p_notice(conn, title, content, time)

def delete_notice(num):
    return d_notice(conn, num)

## for admin ##
def get_admin_profile():
    try:
        ret = {}
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        sql = "select id from users"
        tmp = cursor.execute(sql)
        ret['user_num'] = tmp
        
        sql = "select website_name, count(user_id) as cnt from email_list group by website_name"
        cursor.execute(sql)
        tmp = cursor.fetchall()
        ret['subscription_info'] = tmp
        
        cursor.close()
        return ret
    except Exception as e:
        print(e)
        return False