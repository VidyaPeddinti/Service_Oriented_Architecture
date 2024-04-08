import socket
import threading

host = 'localhost'
port = 9000

api_ports = {
    "passbook": 9001,
    "add_balance_api": 7000,
    "withdrawal_api": 8000
}

def send_request_to_server(host, port, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    request = f"{message}"
    client_socket.send(request.encode())

    response = client_socket.recv(1024).decode()

    client_socket.close()
    return response

def handle_client(client_socket):
    print(f"Connection from {addr}")
    while True:
        data = client_socket.recv(1024).decode()
        print("received data from client api", data)

        if not data:
            break
        
        data = data.split(";")
        name = data[0]
        choice = data[1]

        if choice == "3":
            str1 = "get_trans"
            message = f"{name};{str1}"

            res1 = send_request_to_server(host, api_ports["add_balance_api"], message)
            res2 = send_request_to_server(host, api_ports["withdrawal_api"], message)
            
            mess = f"{choice};{res1};{res2}"

            response = send_request_to_server(host, api_ports["passbook"], mess)
            print("sending response to client_api:", response)
         

        elif choice == "4":
            str1 = "get_balance"
            message = f"{name};{str1}"
            res1 = send_request_to_server(host, api_ports["add_balance_api"], message)
            res2 = send_request_to_server(host, api_ports["withdrawal_api"], message)
            
            mess = f"{choice};{res1};{res2}"

            response = send_request_to_server(host, api_ports["passbook"], mess)
            print("sending response to client_api:", response)
            
        else:
            response = "invalid input"

        client_socket.send(response.encode())

    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print(f"Passbook Server api listening on {host}:{port}")

while True:
    client_socket, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
