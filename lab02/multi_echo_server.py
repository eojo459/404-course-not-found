#!/usr/bin/env python3
from multiprocessing import Process
import socket
import time

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)

            p = Process(target=echo_handler, args=(conn, addr))
            p.daemon = True
            p.start()
            #print("Process " + p + " started")
            
# processes will call this function
def echo_handler(conn, addr):
    #recieve data, wait a bit, then send it back
    full_data = conn.recv(BUFFER_SIZE)
    conn.sendall(full_data)
    #conn.shutdown(socket.SHUT_RDWR)
    conn.close()

if __name__ == "__main__":
    main()
