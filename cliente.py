import socket
import threading
import time


def receive_messages_from_server(so):
    while 1:
        buffer = so.recv(256)
        if not buffer:
            break
        message = buffer.decode('utf-8')
        print(message)

    so.close()


if __name__ == '__main__':

    print("Connecting...")

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    time.sleep(5)
    cliente.connect((socket.gethostname(), 50000))
    msg = ''

    while 1:
        t = threading.Thread(target=receive_messages_from_server, args=(cliente,))
        t.start()

        if not msg:
            msg = input()
        else:
            cliente.send(msg.encode('utf-8'))
            msg = ''
