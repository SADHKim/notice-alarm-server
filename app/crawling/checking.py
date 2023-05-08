import connectDB
from .checking_websites import crawling, make_driver, return_driver


def checking():
    result = []
    
    connectDB.connect()
    sites = connectDB.get_websites()
    make_driver()
    
    for site in sites:
        result.append(crawling(site))
    
    return_driver()
    connectDB.disconnect()
    
    return result