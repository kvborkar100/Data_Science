from urllib.request import urlopen
import lxml.html
import tldextract
url = 'https://www.google.com'

connection = urlopen(url)
dom =  lxml.html.fromstring(connection.read())
extracted = tldextract.extract(url)
main_domain = extracted.domain
yes = 0
no = 0
count = 0
for link in dom.xpath('//a/@href'): # select the url in href for all a tags(links)
    link = str(link)
    count+=1
    if main_domain in link:
        yes+=1
    elif link.startswith('/'):
        yes += 1
    else:
        print(link)
        no+=1
print((yes/count)*100)
print((no/count)*100)
n_per = (no/count)*100
if n_per > 70:
    score15 = -1
elif 60 <= n_per <= 70 :
    score15 = 0
else:
    score15 = 1
print(score15)
