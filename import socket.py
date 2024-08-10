import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5555))
server.listen()

clients = []

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)
                client.close()

print("Server started...")
while True:
    client_socket, addr = server.accept()
    print(f"Connection from {addr}")
    clients.append(client_socket)
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
