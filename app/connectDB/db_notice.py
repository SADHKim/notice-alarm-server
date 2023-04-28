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
        
        return row
    except Exception as e:
        cursor.close()
        return e
    
def g_num_notice(conn, num):
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

def d_notice(conn, num):
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
    
def p_notice(conn, title, content, time):
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