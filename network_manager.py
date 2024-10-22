import socket
import threading

from pygame import Vector2

from models.unit import Unit
from settings import *


class NetworkManager:
    def __init__(self, host=SERVER_HOST, port=SERVER_PORT):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.opponents = {}
        self.is_server = False
        self.is_running = False

    def start_server(self):
        if self.is_server or self.is_running:
            return

        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.is_server = True
        print(f"Server started on {self.host}:{self.port}")
        threading.Thread(target=self._accept_connections).start()

    def stop(self):
        self.is_server = False
        self.is_running = False

    def connect_to_server(self):
        try:
            self.sock.connect((self.host, self.port))
            print(f"Connected to host: {self.host}:{self.port}")
            threading.Thread(target=self._receive_data).start()
        except Exception as e:
            print(f"Connection to host failed: {e}")

    def _accept_connections(self):
        self.is_running = True
        while self.is_running:
            client_socket, client_address = self.sock.accept()
            self.clients.append(client_socket)
            print(f"Accepting client connection from: {client_address}")
            threading.Thread(target=self._handle_client, args=(client_socket,)).start()

    def _handle_client(self, client_socket):
        while self.is_running:
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
        self.is_running = True
        while self.is_running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break

                print(f"Receiving data from Server: {data.decode()}")

                # updating opponents
                encoded = data.decode()
                o_name = str(encoded.split(",")[0])
                o_loc_x = float(encoded.split(",")[1])
                o_loc_y = float(encoded.split(",")[2])
                o_tar_x = float(encoded.split(",")[3])
                o_tar_y = float(encoded.split(",")[4])
                unit = Unit(Vector2(o_loc_x, o_loc_y))
                unit.name = o_name
                unit.target = Vector2(o_tar_x, o_tar_y)
                self.opponents = { o_name: unit }

            except Exception as e:
                print(f"Error while receive data: {e}")
                break

    def send_data(self, player: Unit):
        data_str = f"{str(player.name)},{player.location[0]},{player.location[1]},{player.target[0]},{player.target[1]}"
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
