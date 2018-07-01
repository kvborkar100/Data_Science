from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
import socket
import urllib.request
import whois
from dateutil import relativedelta
import threading
from urllib.parse import urlsplit
import urllib, sys, bs4
import lxml.html
#from urllib.parse import urlsplit
import tldextract
from googlesearch import search
import pandas as pd
import matplotlib.pyplot as plt

class FeatureSet:

    def __init__(self, url):
        self.url_score = {}
        self.url = url

    def url_length(self):
        if len(self.url) >= 54 and len(self.url) < 75:
            score1 = 0
        elif len(self.url) >= 75:
            score1 = -1
        else:
            score1 = 1

        self.url_score['url_length'] = score1

        return self.url_score

    def having_at_symbol(self):

        score2 = 1

        for i in self.url:
            if i == '@':
                score2 = -1
                break

        self.url_score['having_at_symbol'] = score2

    def double_slash(self):

        score3 = 1

        for i in range(len(self.url)):
            if self.url[i - 1] == '/' and self.url[i] == '/':
                if i > 7:
                    score3 = -1
                    break

        self.url_score['double_slash'] = score3

    def https_token(self):

        if 'https://' in self.url:
            score4 = 1
        else:
            score4 = -1

        self.url_score['https_token'] = score4

    def ip_address(self):

        score5 = -1
        lenn = len(self.url)

        if 'https://' in self.url:
            score5 = 1
        elif 'http://' in self.url:
            for i in range(7, lenn):
                if self.url[i].isalpha() == True:
                    score5 = 1
                    break
        else:
            score5 = -1

        self.url_score['ip_address'] = score5

    def tiny_url(self):
        try:
            resp = urlopen(self.url)

            score6 = 1

            for i in self.url:
                if i not in resp.url:
                    score6 = -1
                    break
        except:
            score6 = -1

        self.url_score['tiny_url'] = score6

    def email_submit(self):

        if 'mailto:' in self.url:
            score7 = -1
        elif 'mail()' in self.url:
            score7 = -1
        else:
            score7 = 1

        self.url_score['email_submit'] = score7

    def check_ssl(self):

        score8 = 0

        try:
            req = requests.get(self.url, verify=True)
            score8 = 1

        except requests.exceptions.SSLError:
            score8 = -1
        except:
            score8 = -1

        self.url_score['check_ssl'] = score8

    def thred(self, new_url, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:

            result = sock.connect_ex((new_url, port))
        except:
            result = 400
        self.result_list.append(result)
        print(" checking port {} ....".format(port))

    def port(self):

        lenn = len(self.url) - 1

        score9 = 0

        if (self.url[lenn] != '/'):
            new_url = self.url + '/'

        else:
            new_url = self.url

        if 'https://' in new_url:
            new_url = new_url.replace('https://', '')

        elif 'http://' in new_url:
            new_url = new_url.replace('http://', '')

        for i in range(lenn):
            if new_url[i] == '/':
                j = i
                break
        new_url = new_url[:j:]
        # print(url)
        self.result_list = []

        result = 0
        threads = []
        port_list = [21, 22, 23, 80, 443, 445, 1433, 1521, 3306, 3389]

        for i in range(len(port_list)):
            t = threading.Thread(target=self.thred, args=(new_url, port_list[i]))
            threads.append(t)

        for i in range(len(threads)):
            threads[i].start()

        for i in range(len(threads)):
            threads[i].join()
        print(self.result_list)
        for i in self.result_list:
            if i == 0:
                result += 1
        if result > 2:
            score9 = -1
        else:
            score9 = 1
        self.url_score['port'] = score9


    def redirect(self):

        score10 = 0
        try:
            res = urllib.request.urlopen(self.url)

            finalurl = res.geturl()

            if len(self.url) != len(finalurl):
                score10 = -1
            elif self.url not in finalurl:
                score10 = -1
            else:
                score10 = 1
        except:
            score10 = 1

        self.url_score['redirect'] = score10


    def domain_length(self):
        score11 = 0
        try:
            r = whois.whois(self.url)
            ex_date = r.expiration_date
            cr_date = r.creation_date
            if type(ex_date) is list:
                diff = relativedelta.relativedelta(ex_date[0], cr_date[0])
            else:
                diff = relativedelta.relativedelta(ex_date, cr_date)
            if diff.years <= 1 and diff.months <= 6:
                score11 = -1
            else:
                score11 = 1

        except:
            score11 = -1
        finally:
            self.url_score['domain_length'] = score11


    def prefix_suffix(self):
        lenn = len(self.url) - 1

        score12 = 0

        if (self.url[lenn] != '/'):
            new_url = self.url + '/'

        else:
            new_url = self.url

        if 'https://' in new_url:
            new_url = new_url.replace('https://', '')

        elif 'http://' in new_url:
            new_url = new_url.replace('http://', '')

        for i in range(lenn):
            if new_url[i] == '/':
                j = i
                break
        new_url = new_url[:j:]
        if "-" in new_url:
            score12 = -1
        else:
            score12 = 1

        self.url_score['prefix_suffix'] = score12


    def sub_domain_check(self):
        lenn = len(self.url) - 1

        score12 = 0

        if (self.url[lenn] != '/'):
            new_url = self.url + '/'

        else:
            new_url = self.url

        if 'https://' in new_url:
            new_url = new_url.replace('https://', '')

        elif 'http://' in new_url:
            new_url = new_url.replace('http://', '')
        for i in range(lenn):
            if new_url[i] == '/':
                j = i
                break
        new_url = new_url[:j:]
        if 'www.' in new_url:
            new_url = new_url.replace('www.', '')
        ccTLD = ['.ac', '.ad', '.ae', '.af', '.ag', '.ai', '.al', '.am', '.ao', '.aq', '.ar', '.as', '.at', '.au',
                 '.aw', '.ax', '.az', '.ba', '.bb', '.bd', '.be', '.bf', '.bg', '.bh', '.bi', '.bj', '.bm', '.bn',
                 '.bo', '.br', '.bs', '.bt', '.bw', '.by', '.bz', '.ca', '.cc', '.cd', '.cf', '.cg', '.ch', '.ci',
                 '.ck', '.cl', '.cm', '.cn', '.co', '.cr', '.cu', '.cv', '.cw', '.cx', '.cy', '.cz', '.de', '.dj',
                 '.dk', '.dm', '.do', '.dz', '.ec', '.ee', '.eg', '.er', '.es', '.et', '.eu', '.fi', '.fj', '.fk',
                 '.fm', '.fo', '.fr', '.ga', '.gd', '.ge', '.gf', '.gg', '.gh', '.gi', '.gl', '.gm', '.gn', '.gp',
                 '.gq', '.gr', '.gs', '.gt', '.gu', '.gw', '.gy', '.hk', '.hm', '.hn', '.hr', '.ht', '.hu', '.id',
                 '.ie', '.il', '.im', '.in', '.io', '.iq', '.ir', '.is', '.it', '.je', '.jm', '.jo', '.jp', '.ke',
                 '.kg', '.kh', '.ki', '.km', '.kn', '.kp', '.kr', '.kw', '.ky', '.kz', '.la', '.lb', '.lc', '.li',
                 '.lk', '.lr', '.ls', '.lt', '.lu', '.lv', '.ly', '.ma', '.mc', '.md', '.me', '.mg', '.mh', '.mk',
                 '.ml', '.mm', '.mn', '.mo', '.mp', '.mq', '.mr', '.ms', '.mt', '.mu', '.mv', '.mw', '.mx', '.my',
                 '.mz', '.na', '.nc', '.ne', '.nf', '.ng', '.ni', '.nl', '.no', '.np', '.nr', '.nu', '.nz', '.om',
                 '.pa', '.pe', '.pf', '.pg', '.ph', '.pk', '.pl', '.pm', '.pn', '.pr', '.ps', '.pt', '.pw', '.py',
                 '.qa', '.re', '.ro', '.rs', '.ru', '.rw', '.sa', '.sb', '.sc', '.sd', '.se', '.sg', '.sh', '.si',
                 '.sk', '.sl', '.sm', '.sn', '.so', '.sr', '.ss', '.st', '.sv', '.sx', '.sy', '.sz', '.tc', '.td',
                 '.tf', '.tg', '.th', '.tj', '.tk', '.tl', '.tm', '.tn', '.to', '.tr', '.tt', '.tv', '.tw', '.tz',
                 '.ua', '.ug', '.uk', '.us', '.uy', '.uz', '.va', '.vc', '.ve', '.vg', '.vi', '.vn', '.vu', '.wf',
                 '.ws', '.ye', '.yt', '.za', '.zm', '.zw']
        for i in ccTLD:
            if i in new_url[-3:]:
                new_url = new_url.replace(i, '')
        num_dots = 0
        for j in new_url:
            if j == ".":
                num_dots += 1
        if num_dots == 2:
            score13 = 0
        elif num_dots > 2:
            score13 = -1
        else:
            score13 = 1
        self.url_score['sub_domain_check'] = score13


    def domain_age(self):
        try:
            extracted = tldextract.extract(self.url)
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
                if age < 0.498288:
                    score14 = -1
                else:
                    score14 = 1
        except:
            score14 = -1
        self.url_score['domain_age'] = score14

    def url_anchor(self):
        connection = urlopen(self.url)
        dom = lxml.html.fromstring(connection.read())
        extracted = tldextract.extract(self.url)
        main_domain = extracted.domain
        yes = 0
        no = 0
        count = 0
        for link in dom.xpath('//a/@href'):
            link = str(link)
            count += 1
            if main_domain in link:
                yes += 1
            elif link.startswith('/'):
                yes += 1
            else:
                no += 1
        # print((yes/count)*100)
        if count == 0:
            score15 = 0
        else:
            n_per = (no / count) * 100
            if n_per > 70:
                score15 = -1
            elif 60 <= n_per <= 70:
                score15 = 0
            else:
                score15 = 1
        self.url_score['url_anchor'] = score15

    def web_traffic(self):
        base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(self.url))
        try:
            rank = bs4.BeautifulSoup(urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + base_url).read(), "xml").find(
                "POPULARITY")['TEXT']
            if int(rank) <= 8000000:
                score16 = 1
            else:
                score16 = 0
        except:
            score16 = -1
        self.url_score['web_traffic'] = score16

    def google_index(self):
        query = self.url
        l = list(search(query, tld="com", num=2, stop=1, pause=2))
        if len(l) != 0:
            score17 = 1
        else:
            score17 = -1
        self.url_score['google_index'] = score17

    def favicon(self):
        try:
            extracted = tldextract.extract(self.url)
            main_domain = extracted.domain
            connection = urlopen(self.url)
            dom = lxml.html.fromstring(connection.read())
            link_ico = ''
            for link in dom.xpath('//@href'):
                if ".ico" in link:
                    link_ico = str(link)
                    break
            if main_domain in link_ico:
                score18 = 1
            elif link_ico.startswith('/'):
                score18 = 1
            else:
                score18 = -1
        except:
            score18 = -1
        self.url_score['favicon'] = score18

    def requesr_url(self):
        try:
            extracted = tldextract.extract(self.url)
            main_domain = extracted.domain
            connection = urlopen(self.url)
            dom = lxml.html.fromstring(connection.read())
            count_good = 0
            count_bad = 0
            for link in dom.xpath('//img/@src'):
                link = str(link)
                if link.startswith('/') or 'gravatar' in link or 'imgur' in link or main_domain in link:
                    count_good += 1
                else:
                    count_bad += 1
            if count_good > 0 or count_bad > 0:
                good_avg = (count_good / (count_good + count_bad)) * 100
                bad_avg = (count_bad / (count_good + count_bad)) * 100
                if good_avg > 70:
                    score19 = 1
                elif 50 <= good_avg <= 70:
                    score19 = 0
                else:
                    score19 = -1
            else:
                score19 = 0
        finally:
            self.url_score['requesr_url'] = score19

    def links_in_tags(self):
        try:
            extracted = tldextract.extract("https://www.google.com")
            main_domain = extracted.domain
            connection = urlopen("https://www.google.com")
            dom = lxml.html.fromstring(connection.read())
            good = 0
            count = 0
            for link in dom.xpath('//meta/@content'):
                count += 1
                link = str(link)
                if "http://" or "https://" or "www." in link or link.startswith("/"):
                    if main_domain in link:
                        good += 1
            for link in dom.xpath('//link/@href'):
                count += 1
                if main_domain in link or link.startswith('/'):
                    good += 1
            for link in dom.xpath('//script/@src'):
                count += 1
                if main_domain in link or link.startswith('/'):
                    good += 1
            good_avg = (good / count) * 100
            if good_avg >= 80:
                score20 = 1
            elif 30 < good_avg < 80:
                score20 = 0
            else:
                score20 = -1
        finally:
            self.url_score['links_in_tags'] = score20


def create(url):
    feature = FeatureSet(url)
    print("your current url is : ", feature.url)
    feature.url_length()
    feature.having_at_symbol()
    feature.double_slash()
    feature.https_token()
    feature.ip_address()
    feature.tiny_url()
    feature.email_submit()
    feature.check_ssl()
    feature.port()
    feature.redirect()
    feature.domain_length()
    feature.prefix_suffix()
    feature.sub_domain_check()
    feature.domain_age()
    feature.url_anchor()
    feature.web_traffic()
    feature.google_index()
    feature.favicon()
    feature.requesr_url()
    feature.links_in_tags()
    print("feature for given url is :", feature.url_score)
    feature_set = []
    for i in feature.url_score:
        feature_set.append(feature.url_score[i])
    print(feature_set)
    left = [1, 2, 3]
    values = feature_set
    height = [values.count(1), values.count(0), values.count(-1)]
    tick_label = ['1', '0', '-1']
    plt.bar(left, height, tick_label=tick_label,
            width=0.8, color=['green', 'orange', 'red'])
    plt.xlabel('Behavior Value')
    plt.ylabel('Count')
    plt.title('URL Behavior Graph (Values)')
    plt.show()
    return feature_set