txt = "http://127.0.0.1:27600xxx/abcdef/gjkd/dsadas"
txt2 = "http://127.0.0.1:2600xxx/abc/def"


host = "" # 127.0.0.1
port = ""
path = "" # /abcdef/gjkd/dsadas

# get port
# port_split = txt2.split(":")
# port_split = port_split[2].split("/")
# port = port_split[0]

# get host and path
x = txt2[7:].split("/")

if len(x) >= 2:
    #print("yeah")
    host = x[0]

    for i in range(1, len(x)):
        path += "/" + x[i]

    #print(host)
    #print(path)

port = host.split(":")[1]
print("Host: %s\n" % (host))
print("Port: %s\n" % (port))
print("Path: %s\n" % (path))
#print(x)