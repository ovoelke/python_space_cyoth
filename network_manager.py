import socket
import threading

from settings import *


class NetworkManager:
    def __init__(self, host=SERVER_HOST, port=SERVER_PORT):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.opponents = []
        self.is_server = False
        self.is_active = False

    def start_server(self):
        if self.is_server or self.is_active:
            return

        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.is_server = True
        print(f"Server started on {self.host}:{self.port}")
        threading.Thread(target=self._accept_connections).start()

    def stop(self):
        self.is_active = False
        self.is_server = False

    def connect_to_server(self):
        try:
            self.sock.connect((self.host, self.port))
            print(f"Connected to host: {self.host}:{self.port}")
            threading.Thread(target=self._receive_data).start()
        except Exception as e:
            print(f"Connection to host failed: {e}")

    def _accept_connections(self):
        while self.is_active:
            client_socket, client_address = self.sock.accept()
            self.clients.append(client_socket)
            print(f"Accepting client connection from: {client_address}")
            threading.Thread(target=self._handle_client, args=(client_socket,)).start()

    def _handle_client(self, client_socket):
        self.is_active = True
        while self.is_active:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Receiving data from client: {data.decode()}")
                self.broadcast_data(data, client_socket)
            except Exception as e:
                print(f"Error while handle client: {e}")
                break
        client_socket.close()
        self.clients.remove(client_socket)

    def _receive_data(self):
        while self.is_active:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break

                print(f"Receiving data from Server: {data.decode()}")

            except Exception as e:
                print(f"Error while receive data: {e}")
                break

    def send_data(self, data):
        data_str = f"{data[0]},{data[1]}"
        if self.is_server:
            print(f"Sending data broadcast: {data_str}")
            self.broadcast_data(data_str.encode())
        else:
            try:
                self.sock.send(data_str.encode())
            except Exception as e:
                print(f"Error while send data: {e}")

    def broadcast_data(self, data, sender_socket=None):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(data)
                except Exception as e:
                    print(f"Error while sending data as broadcast: {e}")
                    client.close()
                    self.clients.remove(client)
