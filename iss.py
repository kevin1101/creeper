from bs4 import BeautifulSoup # BeautifulSoup4
import urllib.request

url = 'http://www.ishadowsocks.org/'

data = BeautifulSoup(urllib.request.urlopen(url).read() , "lxml").find_all("div", "col-sm-4")

print(data[3])