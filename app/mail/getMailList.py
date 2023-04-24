### get users' mail from database ###

import pymysql
from conf import DB_ID, DB_PWD, DB_NAME


### the function returns recievers list(tuple) with database table name as params ###
def get_recievers(websiteName):
    
    conn = pymysql.connect(host='localhost', user=DB_ID, passwd=DB_PWD, db=DB_NAME, charset='utf8')
    cursor = conn.cursor()
    
    sql = 'SELECT email FROM email_list WHERE website_name = "' + websiteName + '"'
    cursor.execute(sql)
    
    ## the list of tuple ##
    recieversList = cursor.fetchall()
    
    cursor.close()
    conn = None
    
    return recieversList