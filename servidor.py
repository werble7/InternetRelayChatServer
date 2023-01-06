import socket
import threading


class Cliente:

    def __init__(self, sock, addr):
        self.username = ''
        self.nickname = ''
        self.socket = sock
        self.addr = addr


class ChatServer:
    clients_list = []

    last_received_message = ""

    def __init__(self):
        self.server_socket = None
        self.create_listening_server()

    # listen for incoming connection
    def create_listening_server(self):

        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.bind((socket.gethostname(), 50000))
        print("Esperando conexão..")
        self.server_socket.listen(5)
        self.receive_messages_in_a_new_thread()

    def receive_messages(self, so, addr):
        while True:
            incoming_buffer = so.recv(256)
            if not incoming_buffer:
                break
            last_user = addr
            self.last_received_message = incoming_buffer.decode('utf-8')
            self.broadcast_to_all_clients(last_user)
        so.close()

    def broadcast_to_all_clients(self, addr):
        print(addr, ":", self.last_received_message)

    def receive_messages_in_a_new_thread(self):
        while True:
            client = so, (ip, port) = self.server_socket.accept()
            self.add_to_clients_list(client)
            print('Connected to ', ip, ':', str(port))
            t = threading.Thread(target=self.receive_messages, args=(so, (ip, port)))
            t.start()

    def add_to_clients_list(self, client):
        if client not in self.clients_list:
            self.clients_list.append(client)


if __name__ == '__main__':

    try:
        ChatServer()
    except ConnectionResetError:
        pass










    '''while 1:
        cliente_sock, cliente_addr = servidor.accept()
        lista_clientes.append(Cliente(cliente_sock, cliente_addr))
    
        print("Conectado com", lista_clientes[-1].addr)
    
        while 1:
            for cliente in lista_clientes:
                msg_recv = cliente.socket.recv(512).decode('utf-8')
                if msg_recv:
                    print(cliente.addr, ":", msg_recv)'''
