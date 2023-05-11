import connectDB
from .checking_websites import crawling, make_driver, return_driver
from mail import send_start_mail


def checking():
    result = []
    
    connectDB.connect()
    sites = connectDB.get_websites()
    make_driver()
    send_start_mail(sites)
    
    for site in sites:
        result.append(crawling(site))
    
    return_driver()
    connectDB.disconnect()
    
    return result