import socket

from _thread import *
import threading



lock = threading.Lock() # THREAD IS LOCKED


def Filesender(request):
    header = ""
    pieces = request.split("\n") # REQUESTS ARE SPLITTED TAKING THEM AS VALUES MORE EFFICIENTLY
    if len(pieces) > 0:
        a = (pieces[0].split("/")[0])
        if a == "GET ": # IN REQUEST LIST IF REQUESTED METHOD IS GET PROCESS WILL MOVE ON
            if "/favicon.ico" in pieces[0]: # FAVICON REQUESTS WAS BREAKING OUR SERVER SO WE WRITE A FAVICON HANDLER
                domain = ""
                for i in pieces:
                    print("BU I HARFIII",i)
                    if "localhost:" in i:
                        domain = i
                emp = domain.split("/")[3]
            else:
                emp = pieces[0].split("/")[1].split(" ")[0]
            try:
                if int(emp) > 99 and int(emp) < 20001: # ERROR HANDLER FILE MUST BE MIN. 100 MAX 20.000 BYTES
                    print(str(emp) + " byte file requested")
                    f = open('newfile.html', "wb")  #CREATE A FILE FOR WRITING
                    size = ((int(emp)* 128 - 1))/1000 # FILE BYTE CALCULATION
                    f.write(b"welcome " * int(size)) # WRITE "WELCOME" UNTIL FILE IS GIVEN BYTES
                    f.close()
                    read = open("newfile.html", "rb")
                    r = read.read() #READ THE BYTE
                    #read.close()
                    header += "HTTP/1.1 200 OK\r\n"
                    header += "Content-type: text/html; charset=utf-8 \r\n"
                    header += "Content-length: size"
                    header += "\r\n"
                    header += "\n</body>\n</html>"
                    header += "<html>\n<head>\n<title>THIS FILE IS " + str(emp) + " BYTES!</title>\n</head>\n<body>\n"
                    header += str(r)  # HEADER = CREATED FILE
                    read.close()
                else: #ERROR HANDLER
                    header += "HTTP/1.1 400 Bad Request\r\n"
                    header += "Content-type: text/html; charset=utf-8 \r\n"
                    header += "Content-length: size"
                    header += "\r\n"
                    header += "\n</body>\n</html>"
                    header += "<!DOCTYPE<html><head><title>400</title></head><body><h1>BAD REQUEST</h1><p>ERROR(400).</p></body></html>"
            except ValueError: #ERROR HANDLER
                header += "HTTP/1.1 400 Bad Request\r\n"
                header += "Content-type: text/html; charset=utf-8 \r\n"
                header += "Content-length: size"
                header += "\r\n"
                header += "\n</body>\n</html>"
                header += "<!DOCTYPE<html><head><title>400</title></head><body><h1>BAD REQUEST</h1><p>ERROR(400).</p></body></html>"
        else: #ERROR HANDLER
            header += "HTTP/1.1 501 Not Implemented\r\n"
            header += "Content-type: text/html; charset=utf-8 \r\n"
            header += "Content-length: size"
            header += "\r\n"
            header += "\n</body>\n</html>"
            header += "<!DOCTYPE<html><head><title>501</title></head><body><h1>NOT IMPLEMENTED</h1><p>ERROR(501).</p></body></html>"
    return header


def server_thread(clientconnection):
    req = clientconnection.recv(1024) # RECEIVE 1024BYTES
    print(req.decode().split('\r\n')[0])  #PRINTS THE REQUEST
    response = Filesender(req.decode()) # THE RESULT WE GOT
    print(response.split('\r\n')[0])
    clientconnection.sendall(response.encode()) #SEND ALL THE DATA TO CLIENT
    lock.release() #THREAD UNLOCKED
    clientconnection.close() #CONNECTION CLOSED



def Main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #CREATE A TCP SOCKET
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = int(input("Insert an port number for server: ")) # GIVE A NUMBER ON TERMINAL
    serversocket.bind(("localhost", port)) # USE GIVEN PORT NUMBER AND USE LOCALHOST FOR SERVER DOMAIN
    serversocket.listen(1) # LISTENS TO CLIENT
    print("HTTP server is accessable at: http://localhost:"+str(port)+"/")
    while True:
        clientsocket, address = serversocket.accept() # RETURN ACCEPTED CLIENT OBJECTS TO CLIENTSOCKET AND ADDRESS
        lock.acquire() #LOCK THREAD
        start_new_thread(server_thread, (clientsocket,)) #NEW THREAD CREATION


if __name__ == '__main__':
    Main()