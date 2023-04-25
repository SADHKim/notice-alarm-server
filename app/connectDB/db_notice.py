import pymysql

def g_notices(conn):
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        sql = "SELECT num, title, writer, time from notices ORDER BY num DESC"
        cursor.execute(sql)
        
        row = cursor.fetchall()
        cursor.close()
        
        if not row:
            return False
        else:
            return row
    except Exception as e:
        cursor.close()
        return e
    
def p_notice(conn, title, content, time):
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO notice (title, content, writer, time) VALUES ('%s', '%s', 'admin', '%s')" %(title, content, time)
        
        cursor.execute(sql)
        conn.commit()
        
        cursor.close()
    except Exception as e:
        cursor.close()
        return e
    
    return True