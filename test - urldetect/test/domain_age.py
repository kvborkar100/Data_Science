import whois
import tldextract
extracted = tldextract.extract("https://archive.ics.uci.edu/ml/machine-learning-databases/00327/Training%20Dataset.arff")
domainname = "www." + extracted.domain + "." + extracted.suffix
w = whois.whois(domainname)
if w['creation_date'] == None:
    score14 = -1
else:
    try:
        if len(w['creation_date']) == 2:
            delta = w['expiration_date'][1] - w['creation_date'][1]
    except TypeError:
        delta = w['expiration_date'] - w['creation_date']
    age = (delta.days / 365)
    print(age)
    if age < 0.498288:
        score14 = -1
    else:
        score14 = 1
# print(w)
# print(w['creation_date'][1])
# print(w['expiration_date'][1])
#self.url_score['14'] = score14
