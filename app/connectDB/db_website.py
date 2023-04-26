import pymysql

def p_ask(conn, name, url):
    try:
        cursor = conn.cursor()
        
        sql = "SELECT url FROM websites WHERE url = '%s'" % url
        cursor.execute(sql)
        
        row = cursor.fetchall()
        if not row:
            return False
        
        sql = "INSERT INTO websites (name, url) VALUES ('%s', '%s')" %(name, url)
        cursor.execute(sql)
        conn.commit()
        
        cursor.close()
    except Exception as e:
        cursor.close()
        return e
    
    return True

def g_asks(conn):
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        sql = "SELECT * FROM websites ORDER BY num DESC"
        cursor.execute(sql)
        
        row = cursor.fetchall()
        cursor.close()
        return row
    except Exception as e:
        cursor.close()
        return e
        
        
def g_user_websites(conn, user):
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