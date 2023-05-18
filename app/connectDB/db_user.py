import pymysql
import random

# check if user's id is overlaped #
def c_id_overlap(conn, userid):
    cursor = conn.cursor()
    
    try:
        sql = "SELECT id FROM users WHERE id = '%s'" % userid
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

def c_login(conn, userid, userpwd):
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
    


# get user's information, and push information to databse #
# return True if successed or return False if failed #
def p_user(conn, info):
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

# update user's passwd or email. !!NOT ID!!  #
# return True if successed or return False if failed #
def u_password(conn, user, curr, new):
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
    

def u_email(conn, user, new):
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


# get user's id and return user's id, passwd, email #
def g_user_info(conn, user):
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
    
def f_password(conn, id, email):
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