import socket
import hashlib
from _thread import *
import threading
import os


lock = threading.Lock()


def Filesender(request):
    emp = 0

    pieces = request.split(" ")
    req_server = pieces[1].split("/")[1]
    a = pieces[0]
    if "/localhost:" not in pieces[1]:
        header = "HTTP/1.1 404 Not Found \r\n"
        header += "Content-length: size"
        header += "\r\n"
        header += "\n</body>\n</html>"
        header += '<!DOCTYPE<html><head> 404 Not Found </title></head><body><h1>FILE NOT FOUND</h1><p>404 Not Found.</p></body></html>' # IF NOTHING GIVEN PRINT ERROR
    else:
        try:
            if a == 'GET':
                if "/favicon.ico" in pieces[1]:
                    domain = ""
                    for i in pieces:
                        if "localhost:8888/localhost" in i:
                            domain = i
                    req_port = int(domain.split("/")[3].split(":")[1])
                    emp += int(domain.split("/")[4].split("/")[0].split("\r\n")[0])
                else:
                    req_port = int(req_server.split(":")[1])
                    emp += int(pieces[1].split("/")[2])

                if int(emp) < 10000:
                    encryiption = hashlib.sha256()  # ENCRYPTION TYPE
                    encryiption.update(pieces[1].encode())  # ENCRYPT THE URI
                    cache = (encryiption.hexdigest() + ".cache")  # CACHE NAME = ENCRYPTED URI
                    if os.path.exists(cache):
                        print("Cache Hit!")
                        f = open(cache, "rb" )
                        r = f.read()
                        header = "HTTP/1.1 200 OK\r\n"
                        header += "Content-length: size"
                        header += "\r\n"
                        header += "\n</body>\n</html>"
                        header += ("THIS FILE IS " + str(emp) + "BYTES LONG!")
                        header += str(r)
                        f.close()
                    else:
                        print("Cache Miss!")
                        request = request.replace(pieces[1], '/' + str(emp), 1)
                        try:
                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection: # IF CACHE IS NOT EXISTS
                                connection.connect(("localhost", req_port)) #CONNECT TO SERVER
                                connection.sendall(request.encode()) # SEND ALL DATA
                                header = connection.recv(1024) # 1024 BYTE
                                file = open(str(cache), "wb") # OPEN A CACHE FOR LATER USAGE
                                file.write(header)
                                file.close()
                        except:
                            header = "HTTP/1.1 404 Not Found \r\n"
                            header += "Content-length: size"
                            header += "\r\n"
                            header += "\n</body>\n</html>"
                            header += '<!DOCTYPE<html><head> 404 Not Found </title></head><body><h1>FILE NOT FOUND</h1><p>404 Not Found.</p></body></html>'

                else:
                    header = "HTTP/1.1 400 Bad Request \r\n"
                    header += "Content-length: size"
                    header += "\r\n"
                    header += "\n</body>\n</html>"
                    header += '<!DOCTYPE<html><head> 400 Bad Request </title></head><body><h1>BAD REQUEST</h1><p>400 Bad Request</p></body></html>'

            else:
                header = "HTTP/1.1 501 Not Implemented \r\n"
                header += "Content-length: size"
                header += "\r\n"
                header += "\n</body>\n</html>"
                header += '<!DOCTYPE<html><head> 501 Not Implemented </title></head><body><h1>NOT IMPLEMENTED</h1><p>501 Not Implemented</p></body></html>'
        except ValueError:
            header = "HTTP/1.1 400 Bad Request \r\n"
            header += "Content-length: size"
            header += "\r\n"
            header += "\n</body>\n</html>"
            header += '<!DOCTYPE<html><head> 400 Bad Request </title></head><body><h1>BAD REQUEST</h1><p>400 Bad Request</p></body></html>'
    return header



def server_thread(clientconnection):
    req = clientconnection.recv(1024) # 1024 BYTE RECEIVED
    print(req.decode().split('\r\n')[0])  #PRINTS THE REQUEST
    response = Filesender(req.decode()) #THE RESULT WE GOT
    if type(response) == bytes:
        print(response.decode().split('\r\n')[0])
        clientconnection.sendall(response)
    else:
        print(response.split("\r\n")[0])
        clientconnection.sendall(response.encode())
    lock.release() #THREAD UNLOCKED
    clientconnection.close() #CONNECTION CLOSED



def Main():
    port = 8888
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(("localhost", port))
    serversocket.listen(1)
    print("HTTP server is accessable at: http://localhost:"+str(port)+"/")
    while True:
        clientsocket, address = serversocket.accept()
        lock.acquire()
        start_new_thread(server_thread, (clientsocket,))


if __name__ == '__main__':
    Main()
