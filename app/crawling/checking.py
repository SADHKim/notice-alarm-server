from conf import sites
from .checking_websites import crawling


def checking():
    result = []
    
    for site in sites:
        result.append(crawling(site))
    
    return result