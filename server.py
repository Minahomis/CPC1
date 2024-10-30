from _thread import *
import socket

server = socket.socket()
port = 1234
hostname = socket.gethostbyname(socket.gethostname())
server.bind((hostname, port)) # привязываем к сокету хост и порт сервера
server.listen(10) # начинаем прослушивать входящие подключения
print('Сервер работает. IP:', hostname)

# содержит подключение, адрес, имя (con, addr, username)
clients = []

def remove_client(client):
    if client in clients:
        clients.remove(client)
        print('Пользователь отключен:', client[2])

# закрывает соединение со всеми клиентами
def disconnect_clients():
    for client in clients:
        try:
            client[0].close()
        except:
            continue

# функция для отправки сообщения всем клиентам
def send_message(message, from_client):
    for client in clients:
        if client != from_client: # не отправляем самому себе
            try:
                client[0].send(message.encode())
            except:
                # если не можем отправить сообщение, значит он отключился
                remove_client(client)

# функция для обработки пользователя
def client_thread(con, addr):
    con.send('Вы подключились к чату'.encode())

    username = con.recv(1024).decode()
    client = (con, addr, username)
    clients.append(client)
    print('Подключился пользователь:', username)

    # всегда ждем сообщения от клиента
    while True:
        try:
            message = con.recv(1024)
            if message:
                message = username + ': ' + message.decode()
                send_message(message, client)
                print(message)
            else:
                # если получили пустое сообщение, то потому что он отключился
                remove_client(client)
        except:
            # если не может прочитать сообщение от этого клиента,
            # то убираем его из списка (если он там был)
            remove_client(client)
            continue

# всегда проверям, хочет ли подключиться клиент
while True:
    try:
        con, addr = server.accept()
        start_new_thread(client_thread, (con, addr)) # новый поток
    except KeyboardInterrupt:
        # если нажали контрл с, то сервер завершает работу
        break

# отключаем всех и закрываем сервер
disconnect_clients()
server.close()
