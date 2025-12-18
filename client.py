import socket
import json

name = input("Enter name: ")
age = int(input("Enter age: "))
msg = {'name': name, 'age': age}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 9999))
    s.sendall(json.dumps(msg).encode())
    data = s.recv(1024)
    response = json.loads(data.decode())
    print(f"Your assigned number is {response['number']}")