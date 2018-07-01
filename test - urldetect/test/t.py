import tldextract
from urllib.request import urlopen
import lxml.html
try:
    extracted = tldextract.extract("https://www.google.com")
    main_domain = extracted.domain
    connection = urlopen("https://www.google.com")
    dom = lxml.html.fromstring(connection.read())
    good = 0
    count = 0
    for link in dom.xpath('//meta/@content'):
        count+=1
        link = str(link)
        if "http://" or "https://" or "www." in link or link.startswith("/"):
            print(link)
            if main_domain in link:
                good+=1
    for link in dom.xpath('//link/@href'):
        print(link)
        count += 1
        if main_domain in link or link.startswith('/'):
            good+=1
    for link in dom.xpath('//script/@src'):
        print(link)
        count += 1
        if main_domain in link or link.startswith('/'):
            good+=1
    good_avg = (good / count) * 100
    print(good_avg)
    if good_avg >= 60:
        score20 = 1
    elif 20 < good_avg <60:
        score20 = 0
    else:
        score20 = -1


