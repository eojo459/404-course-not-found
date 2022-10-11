import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('softwareprocess.es', 80)
client_socket.connect(server_address)

request_header = b'GET / HTTP/1.1\r\nHost: softwareprocess.es\r\n\r\n'
client_socket.send(request_header)

response = b''
while True:
    recv = client_socket.recv(1024)
    if not recv:
        break
    response += recv 

print(response.decode())
client_socket.close()   