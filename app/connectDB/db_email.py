import pymysql

def p_email(conn, user, email, website):
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

def d_email(conn, user, email, website):
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

def g_recievers(conn, name):
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
        
