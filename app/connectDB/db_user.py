
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
        return e

    return True


# get user's id and return user's id, passwd, email #
def g_user_info(conn, user):
    cursor = conn.cursor()
    
    sql = "SELECT id, passwd, email FROM users where id = '%s'" % user
    cursor.execute(sql)
    
    row = cursor.fetchall()
    ret = {'id' : row[0], 'passwd' : row[1], 'email' : row[2]}
    
    cursor.close()
    return ret