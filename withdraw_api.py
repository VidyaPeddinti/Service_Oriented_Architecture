import socket
import threading

def send_request_to_server(host, port, message):
    client1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client1_socket.connect((host, port))
    print("connected to withdraw server")

    request = f"{message}"

    client1_socket.send(request.encode())

    response = client1_socket.recv(1024).decode()
    print("received from withdraw server")

    client1_socket.close()

    return response

def handle_client(client_socket, withdraw_host, withdraw_port):

    print(f"Connection from {addr}")
    
    while True:
        data = client_socket.recv(1024).decode()
        print("received data from client api", data)
        if not data:
            break
        response = send_request_to_server(withdraw_host, withdraw_port, data)
        print("sending response to cleint_api:", response)
        client_socket.send(response.encode())
    client_socket.close()

host = 'localhost'
port = 8000

withdraw_port = 8001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print(f"Withdraw Server api listening on {host}:{port}")

while True:
    client_socket, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, host, withdraw_port))
    client_thread.start()
