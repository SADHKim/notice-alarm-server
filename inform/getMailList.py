### get users' mail from database ###

import pymysql

### the function returns recievers list(tuple) with database table name as params ###
def get_recievers(websiteName):
    
    conn = pymysql.connect(host='localhost', user='', passwd='', db='', charset='utf8')
    cursor = conn.cursor()
    
    sql = 'SELECT email FROM eamil_list WHERE website_name = ' + websiteName
    cursor.execute(sql)
    
    ## the list of tuple ##
    recieversList = cursor.fetchall()
    
    return recieversList