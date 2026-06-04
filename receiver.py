import socket
import threading
import time

# Список усіх підключених студентів
clients = []
muted_ips = {}


# НОВА ФУНКЦІЯ: Розсилає повідомлення всім підключеним клієнтам
def broadcast(message, sender_conn=None):
    for client_conn, client_addr in clients[:]:
        # Відправляємо всім, ОКРІМ того, хто це написав (щоб не було дублювання)
        if client_conn != sender_conn:
            try:
                client_conn.send(message.encode('utf-8'))
            except:
                if (client_conn, client_addr) in clients:
                    clients.remove((client_conn, client_addr))


def kick_connection(conn):
    for kick in clients[:]:
        if kick[0] == conn:
            clients.remove(kick)
            conn.close()
            break


# Функція, яка постійно слухає одного конкретного студента
def listen_to_client(conn, addr):
    ip, port = addr[0], addr[1]
    while True:
        try:
            # Чекаємо повідомлення від студента
            data = conn.recv(1024)
            if not data:
                break  # Якщо порожньо, студент відключився

            msg_text = data.decode('utf-8')
            now = time.time()

            if ip in muted_ips:
                if now < muted_ips[ip]:
                    rem = int((muted_ips[ip] - now) / 60) + 1
                    conn.send(f"[СЕРВЕР]: У вас МУТ. Залишилося {rem} хв.".encode('utf-8'))
                    continue
                else:
                    del muted_ips[ip]

            # Формуємо текст повідомлення
            formatted_msg = f"[Студент {port}]: {msg_text}"

            # Виводимо у вас (на сервері)
            print(f"\n{formatted_msg}")

            # ГОЛОВНА МАГІЯ: Пересилаємо повідомлення всім іншим!
            broadcast(formatted_msg, conn)

        except:
            break

    # Якщо сталася помилка або студент вийшов
    print(f"\nСтудент {addr} відключився.")
    kick_connection(conn)

    # Повідомляємо всім, що хтось вийшов
    broadcast(f"--- Студент {port} покинув чат ---")


# Функція, яка чекає на нові підключення
def accept_connections(server):
    while True:
        conn, addr = server.accept()

        print(f"\nНовий студент підключився: {addr}")
        clients.append((conn, addr))

        # Повідомляємо всім у чаті, що приєднався новий учасник
        broadcast(f"--- Студент {addr[1]} приєднався до чату ---", conn)

        # Створюємо окремий потік для цього студента
        thread = threading.Thread(target=listen_to_client, args=(conn, addr), daemon=True)
        thread.start()


# --- Головна частина програми ---
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 5000))
server.listen(10)  # Готові прийняти до 10 студентів

print("Сервер запущено! Чекаємо студентів...")
print("Команди:"
      "\n //kick [port]"
      "\n //mute [port] [time]"
      "\n //unmute [port]"
      )

# Запускаємо процес прийняття підключень у фоновому потоці
accept_thread = threading.Thread(target=accept_connections, args=(server,), daemon=True)
accept_thread.start()

# Головний потік: тут ви просто пишете повідомлення
while True:
    msg = input("")
    parts = msg.split()
    if not parts: continue

    if parts[0] == "//kick" and len(parts) > 1:
        target_port = parts[1]
        kicked = False

        for c_conn, c_addr in clients[:]:

            if str(c_addr[1]) == target_port:
                try:
                    c_conn.send("\n[СЕРВЕР]: Вас було виключено викладачем.\n".encode('utf-8'))
                except:
                    pass

                print(f"Ви вигнали студента з портом {target_port}")
                kick_connection(c_conn)
                broadcast(f"--- Студент {target_port} був виключений ---")
                kicked = True
                break

        if not kicked:
            print(f"Помилка: Студента з портом {target_port} не знайдено.")

    elif parts[0] == "//mute" and len(parts) > 2:
        target_port, mute_time = parts[1], int(parts[2])
        for c_conn, c_addr in clients:
            if str(c_addr[1]) == target_port:
                muted_ips[c_addr[0]] = time.time() + (mute_time * 60)
                c_conn.send(f"\n[СЕРВЕР]: Вам дано МУТ на {mute_time} хв.\n".encode('utf-8'))
                print(f"Мут для {target_port} на {mute_time} хв.")
                break

    elif parts[0] == "//unmute" and len(parts) > 1:
        target_port = parts[1]
        for c_conn, c_addr in clients:
            if str(c_addr[1]) == target_port:
                if c_addr[0] in muted_ips:
                    del muted_ips[c_addr[0]]
                    c_conn.send("\n[СЕРВЕР]: З вас знято МУТ. Ви можете писати.\n".encode('utf-8'))
                    print(f"МУТ знято для порта {target_port}")
                break

    else:
        # Звичайне повідомлення від викладача
        formatted_msg = f"[Викладач]: {msg}"
        broadcast(formatted_msg)