import socket
import threading
import time


class Client:

    def __init__(self, sock, addr):
        self.username = ''
        self.nickname = ''
        self.socket = sock
        self.channel = "channel 1"
        self.ip = addr[0]
        self.port = addr[1]


class ChatServer:

    def __init__(self):
        self.server_socket = None
        self.clients_list = []
        self.channel_list = ["channel 1"]
        self.last_received_message = ""
        self.create_listening_server()

    def commandHandler(self, client, args):
        if client.username == '' == client.nickname:
            if args.split()[0] == "!USER":
                self.newClientHandler(client, args)
            else:
                self.last_received_message = "!USER <username> <nickname> to join server"
                client.socket.sendall(self.last_received_message.encode('utf-8'))
        elif args[0] == "!":
            if args.split()[0] == "!NICK":
                self.nickClientHandler(client, args)
            elif args.split()[0] == "!LIST":
                self.listChannelHandler(client, args)
            else:
                client.socket.sendall("Command does not exist!".encode('utf-8'))
        else:
            self.broadcast_to_all_clients(client)

    def newClientHandler(self, client, args):
        args = args.split()
        if len(args) != 3:
            client.socket.sendall("!USER <username> <nickname> to join server".encode("utf-8"))
        else:
            client.username = args[1]
            client.nickname = args[2]
            self.last_received_message = f"{client.username} ({client.nickname}) has joined {client.channel}"
            print(self.last_received_message)
            self.broadcast_to_all_clients(client)

    def nickClientHandler(self, client, args):
        flag = False
        newNick = args.split()
        if len(newNick) != 2:
            client.socket.sendall("!NICK <newNick> to change the nickname!".encode('utf-8'))
        else:
            for client2 in self.clients_list:
                if client2.socket is not client.socket:
                    msg = f"{client.username} ({client.nickname}) has changed his nick to {newNick[1]}"
                    client2.socket.sendall(str(msg).encode('utf-8'))
                    flag = True
            if flag:
                client.nickname = newNick[1]
                print(msg)

    def deleteClientHandler(self):
        pass

    def subscribeChannelHandler(self):
        pass

    def unsubscribeChannelHandler(self):
        pass

    def listChannelHandler(self, client, args):
        if args != "!LIST":
            client.socket.sendall("!LIST to show all channels".encode('utf-8'))
        else:
            msg = "Channel list: "
            print(msg)
            client.socket.sendall(msg.encode("utf-8"))
            for channel in self.channel_list:
                print(channel)
                msg = channel
                client.socket.sendall(msg.encode("utf-8"))

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

            self.commandHandler(client, msg)

            if client.username != "":
                print(client.nickname + ": " + msg)

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
            so.sendall("Connected on channel 1!".encode('utf-8'))

    def add_to_clients_list(self, client):
        if client not in self.clients_list:
            self.clients_list.append(client)


if __name__ == '__main__':

    ChatServer()
