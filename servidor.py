import socket
import threading


class Client:

    def __init__(self, sock, addr):
        self.username = ''
        self.nickname = ''
        self.socket = sock
        self.ip = addr[0]
        self.port = addr[1]


class ChatServer:

    def __init__(self):
        self.server_socket = None
        self.clients_list = []
        self.last_received_message = ""
        self.create_listening_server()

    def newClientHandler(self, client, args):
        args = args.split()
        client.username = args[1]
        client.nickname = args[2]
        self.last_received_message = client.nickname + " joined the chat"
        print(self.last_received_message)
        self.broadcast_to_all_clients(client)

    def nickClientHandler(self):
        pass

    def deleteClientHandler(self):
        pass

    def subscribeChannelHandler(self):
        pass

    def unsubscribeChannelHandler(self):
        pass

    def listChannelHandler(self):
        pass

    def create_listening_server(self):

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((socket.gethostname(), 50000))
        print("Waiting for connection...")
        self.server_socket.listen(5)
        self.receive_messages_in_a_new_thread()

    def receive_messages(self, client):
        while True:
            incoming_buffer = client.socket.recv(256)
            if not incoming_buffer:
                break
            self.last_received_message = incoming_buffer.decode('utf-8')
            msg = self.last_received_message
            if client.username == client.nickname == '':
                if msg.split()[0] == "!USER":
                    self.newClientHandler(client, msg)
                else:
                    client.socket.sendall("To create a new user insert: !USER <username> <nickname>".encode('utf-8'))
            else:
                self.broadcast_to_all_clients(client)
        client.socket.close()

    def broadcast_to_all_clients(self, sender):
        for client in self.clients_list:
            if client.socket is not sender.socket:
                msg = sender.nickname + ": " + self.last_received_message

                if 'joined the chat' in msg:
                    msg = self.last_received_message

                client.socket.sendall(str(msg).encode('utf-8'))

    def receive_messages_in_a_new_thread(self):
        while True:
            so, (ip, port) = self.server_socket.accept()
            self.add_to_clients_list(Client(so, (ip, port)))
            t = threading.Thread(target=self.receive_messages, args=(Client(so, (ip, port)),))
            t.start()
            so.sendall("Connected on server!".encode('utf-8'))

    def add_to_clients_list(self, client):
        if client not in self.clients_list:
            self.clients_list.append(client)


if __name__ == '__main__':

    try:
        ChatServer()
    except ConnectionResetError:
        pass
