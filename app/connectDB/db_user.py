import pymysql

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
def u_user(conn, info):
    cursor = conn.cursor()
    
    try:
        sql = "UPDATE users SET passwd = '%s', email = '%s' WHERE id = '%s'" %(info['passwd'], info['email'], info['id'])
        cursor.execute(sql)
        
        conn.commit()
        cursor.close()
        
    except Exception as e:
        cursor.close()
        return e

    return True


# get user's id and return user's id, passwd, email #
def g_user_info(conn, user):
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        sql = "SELECT id, passwd, email FROM users where id = '%s'" % user
        cursor.execute(sql)
        
        row = cursor.fetchone()
        cursor.close()
        
        return row
    except Exception as e:
        cursor.close()
        return e