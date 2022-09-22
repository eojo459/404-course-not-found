#!/usr/bin/env python3
import socket
import sys
import time
from weakref import ProxyType, proxy

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():

    proxy_host = 'www.google.com'
    proxy_port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
    
        # setup proxy
        print("Starting Proxy Server...")
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                remote_ip = get_remote_ip(proxy_host)

                # connect proxy to google
                proxy_end.connect((remote_ip, proxy_port))

                # send data and shutdown
                send_data = conn.recv(BUFFER_SIZE)
                proxy_end.sendall(send_data)
                proxy_end.shutdown(socket.SHUT_WR)

                #recieve data, wait a bit, then send it back
                full_data = proxy_end.recv(BUFFER_SIZE)
                time.sleep(0.5)
                conn.sendall(full_data)
            
            conn.close()

if __name__ == "__main__":
    main()
