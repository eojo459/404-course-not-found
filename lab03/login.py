#!/usr/bin/env python3

import cgi
import cgitb
import os
import secret
from hello import get_env
from templates import login_page, secret_page
cgitb.enable()

# print("Content-Type: text/html")    # HTML is following
# print()                             # blank line, end of headers

# source: https://docs.python.org/3/library/cgi.html
form = cgi.FieldStorage()

username = form.getfirst("username")
password = form.getfirst("password")

#print("Username: " + str(username)) # q4
#print("Password: " + str(password)) # q4

# list of environment variables
env = get_env()

get_cookies = os.environ['HTTP_COOKIE']

if 'HTTP_COOKIE' in env and len(get_cookies) > 0:
    #get_cookies = os.environ['HTTP_COOKIE']
    result = {}
    cookie = get_cookies.strip().split(";")
    for item in cookie:
        cookie1 = item.strip().split("=")
        result[cookie1[0]] = cookie1[1]

header = ""
header += "Content-Type: text/html\r\n"

body = ""

# check if login is correct
if username is not None:
    body += secret_page(username=username,password=password)
    body += "Set-Cookie: last-vist=now\r\n"
else:
    body += login_page()

print(header)
print()
print(body)


#print(secret_page(username=username,password=password))