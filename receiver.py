import socket
import threading

# Список усіх підключених студентів
clients = []


# НОВА ФУНКЦІЯ: Розсилає повідомлення всім підключеним клієнтам
def broadcast(message, sender_conn=None):
    for client in clients:
        # Відправляємо всім, ОКРІМ того, хто це написав (щоб не було дублювання)
        if client != sender_conn:
            try:
                client.send(message.encode('utf-8'))
            except:
                pass


# Функція, яка постійно слухає одного конкретного студента
def listen_to_client(conn, addr):
    while True:
        try:
            # Чекаємо повідомлення від студента
            data = conn.recv(1024)
            if not data:
                break  # Якщо порожньо, студент відключився

            # Формуємо текст повідомлення
            msg_text = data.decode('utf-8')
            formatted_msg = f"[Студент {addr}]: {msg_text}"

            # Виводимо у вас (на сервері)
            print(f"\n{formatted_msg}")

            # ГОЛОВНА МАГІЯ: Пересилаємо повідомлення всім іншим!
            broadcast(formatted_msg, conn)

        except:
            break

    # Якщо сталася помилка або студент вийшов
    print(f"\nСтудент {addr} відключився.")
    if conn in clients:
        clients.remove(conn)

    # Повідомляємо всім, що хтось вийшов
    broadcast(f"--- Студент {addr} покинув чат ---")
    conn.close()


# Функція, яка чекає на нові підключення
def accept_connections(server):
    while True:
        conn, addr = server.accept()
        print(f"\nНовий студент підключився: {addr}")
        clients.append(conn)

        # Повідомляємо всім у чаті, що приєднався новий учасник
        broadcast(f"--- Студент {addr} приєднався до чату ---", conn)

        # Створюємо окремий потік для цього студента
        thread = threading.Thread(target=listen_to_client, args=(conn, addr))
        thread.start()


# --- Головна частина програми ---
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5000))
server.listen(10)  # Готові прийняти до 10 студентів

print("Сервер запущено! Чекаємо студентів...")

# Запускаємо процес прийняття підключень у фоновому потоці
accept_thread = threading.Thread(target=accept_connections, args=(server,))
accept_thread.start()

# Головний потік: тут ви просто пишете повідомлення
while True:
    msg = input("")
    formatted_msg = f"[Викладач]: {msg}"

    # Викладач розсилає повідомлення абсолютно всім
    broadcast(formatted_msg)
