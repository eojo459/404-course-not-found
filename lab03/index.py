#!/usr/bin/env python3
import cgi
import cgitb
from templates import login_page
cgitb.enable()

print("Content-Type: application/json")    # HTML is following
print()                             # blank line, end of headers


print("Content-Type: text/html")
print()
print("<title>Hello</title><h2>Hello World</h2>")
print("<title>Hello</title><h2>Hello World2</h2>")
print("<title>Hello</title><h2>Hello World3</h2>")
print("yeah boy")

print(login_page())