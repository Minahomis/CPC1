import socket
from _thread import *

client = socket.socket()
port = 1234
hostname = input('Введите IP сервера: ')
username = input('Введите свое имя: ')

try:
    client.connect((hostname, port))
except:
    print('Ошибка подключения (проверьте IP)')
    exit()

# получаем приветственное сообщение
client.send(username.encode())
respond = client.recv(1024)
print(respond.decode())

# функция, которая всегда принимает сообщения от сервера
def check_server():
    while True:
        try:
            message = client.recv(1024)
            if message:
                print(message.decode())
            else:
                # если пришло пустое сообщение, то значит соединение разорвано
                print('Соединение с сервером разорвано')
                break
        except:
            # если какая-то ошибка, то с сервером чтото не так
            print('Соединение с сервером разорвано')
            break

start_new_thread(check_server, ())

message = ' '
while True:
    try:
        # если сообщение не пустое, то отправляем
        if not message.isspace():
            client.send(message.encode())
        message = input()
    except KeyboardInterrupt:
        # если нажать контрл c, то выходим
        break

client.close()
