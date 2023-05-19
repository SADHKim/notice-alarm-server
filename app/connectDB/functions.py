import pymysql
import random

from conf import DB_ID as id, DB_PWD as pwd, DB_NAME as db

conn = None

def connect():
    global conn
    conn = pymysql.connect(host='localhost', user=id, passwd=pwd, db=db, charset='utf8')

def disconnect():
    global conn
    conn = None
    

## email_list ##
def push_email(user, email, website):
    try:
        cursor = conn.cursor()
        
        sql = "SELECT email FROM email_list WHERE user_id = '%s', AND email = '%s'" % (user, email)
        cursor.execute(sql)
        
        row = cursor.fetchall()
        if not row:
            cursor.close()
            return False
        
                
        sql = "INSERT INTO email_list (user_id, email, website_name) VALUES ('%s', '%s', '%s')" % (user, email, website)
        cursor.execute(sql)
        
        conn.commit()
        cursor.close()
    except Exception as e:
        cursor.close()
        return e
    
    return True
    
def delete_email(user, email, website):
    try:
        cursor = conn.cursor()
            
        sql = "DELETE FROM email_list where user_id = '%s' && email = '%s' && website_name = '%s'" % (user, email, website)
        cursor.execute(sql)
        
        conn.commit()
        cursor.close()
    except Exception as e:
        cursor.close()
        return e
    
    return True

def get_recievers(name):
    try:
        cursor = conn.cursor()
        
        sql = "SELECT email FROM email_list WHERE website_name = '%s'" % name
        cursor.execute(sql)
        
        rows = cursor.fetchall()
        cursor.close()
        if not rows:
            return False
        
        return rows
    except Exception as e:
        cursor.close()
        return e
    
    
## users ##
def push_user(info):
    cursor = conn.cursor()
    
    try:
        sql = "INSERT INTO users (id, passwd, email) VALUES ('%s', '%s', '%s')" % (info['id'], info['passwd'], info['email'])
        cursor.execute(sql)
        
        conn.commit()
        cursor.close()
        
    except Exception as e:
        cursor.close()
        return e
    
    return True
    
def update_password(user, curr, new):
    try:
        cursor = conn.cursor()
        
        sql = "SELECT id FROM users WHERE id = '%s' AND passwd = '%s'" % (user, curr)
        cursor.execute(sql)
        
        row = cursor.fetchone()
        if not row:
            return False
        
        sql = "UPDATE users SET passwd = '%s' WHERE id = '%s' AND passwd = '%s'" %(new, user, curr)
        cursor.execute(sql)
        
        conn.commit()
        cursor.close()
        
        return True
    except Exception as e:
        cursor.close()
        return e

def update_email(user, new):
    try:
        cursor = conn.cursor()
        
        sql = "UPDATE users SET email = '%s' WHERE id = '%s'" %(new, user)
        cursor.execute(sql) # change email in users table
        
        sql = "UPDATE email_list SET email = '%s' WHERE user_id = '%s'" %(new, user)
        cursor.execute(sql) # change email in email_list table
        
        conn.commit()
        cursor.close()
        
        return True
    except Exception as e:
        cursor.close()
        return e
    
def get_user_info(user):
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        sql = "SELECT id, email, passwd FROM users where id = '%s'" % user
        cursor.execute(sql)
        
        row = cursor.fetchone()
        cursor.close()
        
        return row
    except Exception as e:
        cursor.close()
        return e

def id_overlap_check(id):
    cursor = conn.cursor()
    
    try:
        sql = "SELECT id FROM users WHERE id = '%s'" % id
        cursor.execute(sql)
        
        row = cursor.fetchall()
        cursor.close()
        
        if not row:
            return True
        else:
            return False
        
    except Exception as e:
        cursor.close()
        return e

def login(userid, userpwd):
    cursor = conn.cursor()
    
    try:
        sql = "SELECT id, passwd FROM users WHERE id = '%s'" % userid
        cursor.execute(sql)
        
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return False
        
        
        if row[0] == userid and row[1] == userpwd:
            return True
        else:
            return False
    except Exception as e:
        cursor.close()
        return e

def find_password(id, email):
    try:
        cursor = conn.cursor()
        
        sql = "select id from users where id = '%s' and email = '%s'" % (id, email)
        cursor.execute(sql)
        
        row = cursor.fetchone()
        if not row:
            return False
        
        newPass = 'noticealarm' + str(random.randint(0, 10000))
        sql = "update users set passwd = '%s' where id = '%s' and email = '%s'" % (newPass, id, email)
        cursor.execute(sql)
        
        conn.commit()
        cursor.close()
        
        return newPass
    except:
        cursor.close()
        return 'error'

def delete_user(user, password):
    try:
        cursor = conn.cursor()
        sql = "select id from users where id = '%s' and passwd = '%s'" % (user, password)
        
        cursor.execute(sql)
        row = cursor.fetchone()
        
        if not row:
            return False
        
        sql = "delete from users where id = '%s' and passwd = '%s'" %(user, password)
        cursor.execute(sql)
        sql = "delete from email_list where user_id = '%s'" % user
        cursor.execute(sql)
        
        conn.commit()
        cursor.close()
        return True
    except:
        return 'error'

## asks ##
def get_asks():
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        sql = "SELECT name, url FROM asks ORDER BY num DESC"
        cursor.execute(sql)
        
        row = cursor.fetchall()
        cursor.close()
        
        return row
    except Exception as e:
        cursor.close()
        return e

def push_ask(name, url):
    try:
        cursor = conn.cursor()
        
        sql = "SELECT url FROM asks WHERE url = '%s'" % url
        cursor.execute(sql)
        
        row = cursor.fetchone()
        if row:
            return False
        
        sql = "INSERT INTO asks (name, url) VALUES ('%s', '%s')" %(name, url)
        cursor.execute(sql)
        conn.commit()
        
        cursor.close()
    except Exception as e:
        cursor.close()
        return e
    
    return True

def delete_ask(url):
    try:
        cursor = conn.cursor()
        
        sql = "SELECT name FROM asks WHERE url = '%s'" %url
        cursor.execute(sql)
        
        row = cursor.fetchone()
        if not row:
            return False
        
        sql = "DELETE FROM asks WHERE url = '%s'" %url
        cursor.execute(sql)
        
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        cursor.close()
        return e

## website ##
def get_user_websites(user):
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        sql = "SELECT website_name FROM email_list WHERE user_id = '%s' ORDER BY num DESC" % user
        cursor.execute(sql)
        
        rows = cursor.fetchall()
        cursor.close()
        
        return rows
    except Exception as e:
        cursor.close()
        return e

def delete_user_webiste(user, website):
    try:
        cursor = conn.cursor()
        
        sql = "SELECT website_name FROM email_list WHERE user_id = '%s' AND website_name = '%s'" %(user, website)
        cursor.execute(sql)
        
        row = cursor.fetchone()
        if not row:
            return False
        
        sql = "DELETE FROM email_list WHERE user_id = '%s' AND website_name = '%s'" %(user, website)
        cursor.execute(sql)
        
        conn.commit()
        cursor.close()
        
        return True
    except Exception as e:
        cursor.close()
        return e

def push_user_website(user, email, name):
    try:
        cursor = conn.cursor()
        
        sql = "SELECT user_id FROM email_list WHERE user_id = '%s' AND website_name = '%s'" % (user, website)
        cursor.execute(sql)
        row = cursor.fetchone()
        
        if row:
            return False
        
        sql = "INSERT INTO email_list (user_id, email, website_name) VALUES ('%s', '%s', '%s')" %(user, email, website)
        cursor.execute(sql)
        
        conn.commit()
        cursor.close()
        
        return True
    except Exception as e:
        cursor.close()
        return e

def get_websites():
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        sql = "SELECT name, url, class, path from websites ORDER BY num DESC"
        cursor.execute(sql)
        
        rows = cursor.fetchall()
        cursor.close()
        
        return rows
    except Exception as e:
        cursor.close()
        return e

def push_website(info):
    try:
        cursor = conn.cursor()
        
        sql = "SELECT name FROM websites where name = '%s'" % info['name']
        cursor.execute(sql)
        row = cursor.fetchone()
        
        if row:
            cursor.close()
            return False
        
        sql = "INSERT INTO websites (name, url, class, path) VALUES ('%s', '%s', '%s', '%s')" %(info['name'], info['url'], info['class'], info['path'])
        cursor.execute(sql)
        conn.commit()
        
        cursor.close()
        return True
    except Exception as e:
        cursor.close()
        return e

def delete_website(name):
    try:
        cursor = conn.cursor()
        
        sql = "SELECT name FROM websites WHERE name='%s'" % name
        cursor.execute(sql)
        
        row = cursor.fetchone()
        if not row:
            cursor.close()
            return False
        
        sql = "DELETE FROM websites WHERE name='%s'" % name
        cursor.execute(sql)
        sql = "DELETE FROM email_list WHERE website_name='%s'" %name
        cursor.execute(sql)
        
        conn.commit()
        cursor.close()

        return True
    except Exception as e:
        cursor.close()
        return e


## db_notice ##
def get_notices():
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        sql = "SELECT num, title, writer, time from notices ORDER BY num DESC"
        cursor.execute(sql)
        
        row = cursor.fetchall()
        cursor.close()
        
        return row
    except Exception as e:
        cursor.close()
        return e

def get_num_notice(num):
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT title, content, time FROM notices WHERE num = '%s'" %num
        cursor.execute(sql)
        
        row = cursor.fetchone()
        cursor.close()
        return row
    except Exception as e:
        cursor.close()
        return e

def push_notice(title, content, time):
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO notices (title, content, writer, time) VALUES ('%s', '%s', 'admin', '%s')" %(title, content, time)
        
        cursor.execute(sql)
        conn.commit()
        
        cursor.close()
    except Exception as e:
        cursor.close()
        return e
    
    return True

def delete_notice(num):
    try:
        cursor = conn.cursor()
        
        sql = "SELECT num FROM notices WHERE num = '%s'" %num
        cursor.execute(sql)
        
        row = cursor.fetchone()
        
        if not row:
            return False
        
        sql = "DELETE FROM notices WHERE num = '%s'" %num
        cursor.execute(sql)
        
        conn.commit()
        cursor.close()
        
        return True
    except Exception as e:
        return e

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