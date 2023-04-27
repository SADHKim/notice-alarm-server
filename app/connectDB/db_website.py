import pymysql

def g_websites(conn):
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        sql = "SELECT name, url, class, tag from websites ORDER BY num DESC"
        cursor.execute(sql)
        
        rows = cursor.fetchall()
        cursor.close()
        
        return rows
    except Exception as e:
        cursor.close()
        return e
    
def p_website(conn, info):
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO websites (name, url, class, tag) VALUES ('%s', '%s', '%s', '%s')" %(info['name'], info['url'], info['class'], info['tag'])
        
        cursor.execute(sql)
        conn.commit()
        
        cursor.close()
        return True
    except Exception as e:
        cursor.close()
        return e
    
def d_website(conn, info):
    try:
        cursor = conn.cursor()
        
        sql = "SELECT name FROM websites WHERE name='%s' AND url='%s'" %(info['name'], info['url'])
        cursor.execute(sql)
        
        row = cursor.fetchone()
        if not row:
            cursor.close()
            return False
        
        
        sql = "DELETE FROM websites WHERE name='%s' AND url='%s'" %(info['name'], info['url'])
        cursor.execute(sql)
        
        conn.commit()
        cursor.close()
        
        return True
    except Exception as e:
        cursor.close()
        return e
        

def p_ask(conn, name, url):
    try:
        cursor = conn.cursor()
        
        sql = "SELECT url FROM asks WHERE url = '%s'" % url
        cursor.execute(sql)
        
        row = cursor.fetchall()
        if not row:
            return False
        
        sql = "INSERT INTO asks (name, url) VALUES ('%s', '%s')" %(name, url)
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
        
        sql = "SELECT * FROM asks ORDER BY num DESC"
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
    
def d_user_website(conn, user, website):
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
    
def p_user_website(conn, user, email, website):
    try:
        cursor = conn.cursor()
        
        sql = "SELECT FROM email_list WHERE user_id = '%s' AND website_name = '%s'" % (user, website)
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