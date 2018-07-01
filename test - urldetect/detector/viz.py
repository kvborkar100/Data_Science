import matplotlib.pyplot as plt
dict = {'url_length': 1, 'having_at_symbol': 1, 'double_slash': 1, 'https_token': -1, 'ip_address': 1, 'tiny_url': 1, 'email_submit': 1, 'check_ssl': 1, 'port': -1, 'redirect': -1, 'domain_length': 1, 'prefix_suffix': 1, 'sub_domain_check': 1, 'domain_age': 1, 'url_anchor': 1, 'web_traffic': 1, 'google_index': 1, 'favicon': 1, 'requesr_url': 1, 'links_in_tags': 0}
l = sorted(dict.items())
x,y = zip(*l)
plt.plot(x,y)
plt.show()