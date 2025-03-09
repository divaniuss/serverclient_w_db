import socket
from datetime import datetime
# client

IP = '127.0.0.1'
PORT = 4000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

choice = input("Вы хотите записать заметку(+) или вывести их(-)?: ")

if choice == "+":
    date = datetime.now().strftime("%Y-%m-%d")
    title = input("Введите название заметки: ")
    text = input("Введите текст: ")
    message = f"{date} {title} {text}"
    client.send(message.encode())
elif choice == "-":
    message = f"vivod"
    client.send(message.encode())
else:
    print(f"Выберете +/-")
    client.close()


response = client.recv(1024).decode()
print(f"Ответ сервера: {response}")

client.close()
