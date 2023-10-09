import socket
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
nicknames = []

print("Server has started...")

def clientthread(conn, addr):
    conn.send("Welcome to this chatroom!".encode('utf-8'))
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                print ( message)
                broadcast( message , conn)
            else:
                remove(conn)
                removeNicknames(nickname)
        except:
            continue

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message.encode('utf-8'))
            except:
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def removeNicknames(name):
    if name in nicknames:
        nicknames.remove(name)

while True:
    conn, addr = server.accept()
    conn.send('NICKNIAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    nicknames.append(nickname)
    list_of_clients.append(conn)
    message = f'{nickname} joined....'
    print(message)
    broadcast(message, conn)
    new_thread = Thread(target= clientthread,args=(conn,addr))
    new_thread.start()
