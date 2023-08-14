import socket
import threading

def handle_client(client_socket, clients, client_id):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"Received message from Cliente {client_id}: {message}")

            # Distribuir a mensagem para todos os outros clientes
            for client in clients:
                if client != client_socket:
                    try:
                        client.send(f"Cliente {client_id}: {message}".encode('utf-8'))
                    except:
                        clients.remove(client)
                else:
                    client.send(f"Você: {message}".encode('utf-8'))
        except:
            break

    client_socket.close()
    clients.remove(client_socket)

def main():
    host = "0.0.0.0"
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    clients = []
    client_id = 1

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket, clients, client_id))
        client_handler.start()
        
        client_id += 1

if __name__ == "__main__":
    main()
