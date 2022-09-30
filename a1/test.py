from ast import Assert
from urllib import request

#BASEURL = "http://127.0.0.1:8080"



baseurl = "http://127.0.0.1:8080"

url = baseurl + "/../../../../../../../../../../../../etc/group"
url2 = "http://www.reddit.com"
req = request.urlopen(url, None, 3)
print(req.getcode())
print(req.info())
print(req.getheaders())
Assert( req.getcode() == 200)
Assert( req.info().get_content_type() == "text/css")
