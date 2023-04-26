### get users' mail from database ###

import connectDB


### the function returns recievers list(tuple) with database table name as params ###
def get_recievers(websiteName):
    
    connectDB.connect()
    recieversList = connectDB.get_recievers(websiteName)
    connectDB.disconnect()
    
    return recieversList