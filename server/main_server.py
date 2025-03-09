import socket
import pyodbc
from datetime import datetime

# Параметры подключения к базе данных
server_base = r'localhost\SQLEXPRESS'
database = 'db_name'
username = ''
password = ''

IP = '127.0.0.1'
PORT = 4000

# Строка подключения
dsn = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_base};DATABASE={database};Trusted_Connection=yes'

# Запуск сервера
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(1)
print("Сервер запущен, ожидание подключения...")

conn, addr = server.accept()
print(f"Подключение от: {addr}")

request = conn.recv(1024).decode()

if request == 'vivod':
    try:
        with pyodbc.connect(dsn) as conn_db:
            cursor = conn_db.cursor()
            cursor.execute("SELECT * FROM [Notes]")
            rows = cursor.fetchall()


            result_str = ""
            for row in rows:
                result_str += f"\nID:{row[0]} Дата: {row[1]}, Название: {row[2]}, Текст: {row[3]}"

            conn.send(result_str.encode())
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        conn.send(f"Ошибка подключения: {e}".encode())

else:
    try:
        date, title, text = request.split(' ', 2)
        conn_db = pyodbc.connect(dsn)
        cursor = conn_db.cursor()

        insert_query = "INSERT INTO  [Notes] ([date], [title], [text]) VALUES (?, ?, ?)"
        values = (date, title, text)
        cursor.execute(insert_query, values)
        conn_db.commit()

        result_str = "Данные успешно вставлены"
        conn.send(result_str.encode())
        # Закрытие соединения
        cursor.close()
        conn_db.close()

    except Exception as e:
        print(f"Ошибка подключения: {e}")
        result_str = (f"Ошибка подключения: {e}")
        conn.send(result_str.encode())


conn.close()
server.close()