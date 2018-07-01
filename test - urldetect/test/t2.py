from urllib.request import urlopen
import lxml.html
import tldextract
extracted = tldextract.extract("https://www.billboard.com/videos")
main_domain = extracted.domain
connection = urlopen("https://www.billboard.com/videos")
dom = lxml.html.fromstring(connection.read())
count_good = 0
count_bad = 0
for link in dom.xpath('//video/@src'):
    print(link)
