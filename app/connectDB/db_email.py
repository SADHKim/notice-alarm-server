def p_email(conn, user, email, website):
    try:
        cursor = conn.cursor()
                
        sql = "INSERT INTO email_list (user_id, email, website_name) VALUES ('%s', '%s', '%s')" % (user, email, website)
        cursor.execute(sql)
        
        conn.commit()
        cursor.close()
    except Exception as e:
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
        return e
    
    return True
