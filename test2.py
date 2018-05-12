# -*- coding: utf-8 -*-

import os
import socket

HOST = '127.0.0.1'
PORT = 50007

os.chdir(r'C:\Users\ichet\PycharmProjects\test1')

with open('top.txt', 'r', encoding='utf8') as f:
    info = dict(x.strip().split(' : ') for x in f.readlines())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected client')

data = ''
while 1:
    dt = conn.recv(1024)
    data += dt.decode('utf8')
    if data == 'quit':
        print('Завершується!')
        break
    conn.send(info.get(data, 'Я не знаю, що від мене хочуть?!').encode('utf8'))
    data = ''
conn.close()
print('Завершено!')