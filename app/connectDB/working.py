import pymysql

conn = None
def connect(id, pwd, db):
    global conn
    
    conn = pymysql.connect(host='localhost', user=id, passwd=pwd, db=db, charset='utf8')
    
def push_email(user, email, website):
    try:
        cursor = conn.cursor()
                
        sql = "INSERT INTO email_list (user_id, email, website_name) VALUES ('%s', '%s', '%s')" % (user, email, website)
        cursor.execute(sql)
        
        conn.commit()
        cursor.close()
    except:
        return False
    
    return True

def delete_email(user, email, website):
    try:
        cursor = conn.cursor()
            
        sql = "DELETE FROM email_list where user_id = '%s' && email = '%s' && website_name = '%s'" % (user, email, website)
        cursor.execute(sql)
        
        conn.commit()
        cursor.close()
    except:
        return False
    
    return True

    
    