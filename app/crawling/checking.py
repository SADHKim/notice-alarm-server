import connectDB
from .checking_websites import crawling


def checking():
    result = []
    
    connectDB.connect()
    sites = connectDB.get_websites()
    
    for site in sites:
        result.append(crawling(site))
    
    connectDB.disconnect()
    
    return result