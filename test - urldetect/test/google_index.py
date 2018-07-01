from googlesearch import search
query = "https://www.geeksforgeeks.org/performing-google-search-using-python-code/"
l = list(search(query, tld="com", num=2, stop=1, pause=2))
print(l)
print(len(l))
if len(l) != 0:
    score17 = 1
else:
    score17 = -1
print(score17)