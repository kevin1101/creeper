from bs4 import BeautifulSoup # BeautifulSoup4
import urllib.request

def get_content(string):
	return string.split(":")[-1]

url = 'http://www.ishadowsocks.org/'

data = BeautifulSoup(urllib.request.urlopen(url).read() , "lxml").find_all("div", "col-sm-4")

a = data[3].find_all("h4")
print(a[0].text.split(":")[0])
print(get_content(a[0].text))
print(get_content(a[1].text))
print(get_content(a[2].text))
print(get_content(a[3].text))

b = data[4].find_all("h4")
print(b[0].text.split(":")[0])
print(get_content(b[0].text))
print(get_content(b[1].text))
print(get_content(b[2].text))
print(get_content(b[3].text))

c = data[5].find_all("h4")
print(c[0].text.split(":")[0])
print(get_content(c[0].text))
print(get_content(c[1].text))
print(get_content(c[2].text))
print(get_content(c[3].text))