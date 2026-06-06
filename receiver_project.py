import socket
import threading
import time
import tkinter as tk
from tkinter import scrolledtext

# Список усіх підключених студентів
clients = []
muted_ips = {}

# Список для збереження історії відправлених повідомлень та індекс для навігації
history = []
history_index = -1


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
            log_message(formatted_msg)

            # ГОЛОВНА МАГІЯ: Пересилаємо повідомлення всім іншим!
            broadcast(formatted_msg, conn)

        except:
            break

    # Якщо сталася помилка або студент вийшов
    log_message(f"Студент {addr} відключився.")
    kick_connection(conn)

    # Повідомляємо всім, що хтось вийшов
    broadcast(f"--- Студент {port} покинув чат ---")


# Функція, яка чекає на нові підключення
def accept_connections(server):
    while True:
        try:
            conn, addr = server.accept()

            log_message(f"Новий студент підключився: {addr}")
            clients.append((conn, addr))

            # Повідомляємо всім у чаті, що приєднався новий учасник
            broadcast(f"--- Студент {addr[1]} приєднався до чату ---", conn)

            # Створюємо окремий потік для цього студента
            thread = threading.Thread(target=listen_to_client, args=(conn, addr), daemon=True)
            thread.start()
        except:
            break


def log_message(message):
    log_chat.config(state=tk.NORMAL)
    log_chat.insert(tk.END, message + "\n")
    log_chat.yview(tk.END)
    log_chat.config(state=tk.DISABLED)


def send_message(event=None):
    global history_index
    msg = entry_msg.get()
    if not msg:
        return

    # Додаємо повідомлення в історію, якщо воно не дублює попереднє
    if not history or history[-1] != msg:
        history.append(msg)
    history_index = len(history)  # Скидаємо індекс на кінець списку

    entry_msg.delete(0, tk.END)

    parts = msg.split()
    if not parts:
        return

    if parts[0] == "//help":
        help_text = (
            "[СЕРВЕР]: Доступні команди:"
            "\n  //help - показати це повідомлення"
            "\n  //kick [port] - вигнати студента з чату"
            "\n  //mute [port] [time] - дати мут на к-сть хвилин"
            "\n  //unmute [port] - зняти мут"
        )
        log_message(help_text)


    if parts[0] == "//kick" and len(parts) > 1:
        target_port = parts[1]
        kicked = False

        for c_conn, c_addr in clients[:]:
            if str(c_addr[1]) == target_port:
                try:
                    c_conn.send("\n[СЕРВЕР]: Вас було виключено викладачем.\n".encode('utf-8'))
                    c_conn.send("//exit").encode('utf-8')
                except:
                    pass

                log_message(f"Ви вигнали студента з портом {target_port}")
                kick_connection(c_conn)
                broadcast(f"--- Студент {target_port} був виключений ---")
                kicked = True
                break

        if not kicked:
            log_message(f"Помилка: Студента з портом {target_port} не знайдено.")

    elif parts[0] == "//mute" and len(parts) > 2:
        target_port, mute_time = parts[1], int(parts[2])
        for c_conn, c_addr in clients:
            if str(c_addr[1]) == target_port:
                muted_ips[c_addr[0]] = time.time() + (mute_time * 60)
                c_conn.send(f"\n[СЕРВЕР]: Вам дано МУТ на {mute_time} хв.".encode('utf-8'))
                log_message(f"Мут для {target_port} на {mute_time} хв.")
                break

    elif parts[0] == "//unmute" and len(parts) > 1:
        target_port = parts[1]
        for c_conn, c_addr in clients:
            if str(c_addr[1]) == target_port:
                if c_addr[0] in muted_ips:
                    del muted_ips[c_addr[0]]
                    c_conn.send("\n[СЕРВЕР]: З вас знято МУТ. Ви можете писати.\n".encode('utf-8'))
                    log_message(f"МУТ знято для порта {target_port}")
                break

    elif parts[0] == "//online":
        count = len(clients)
        log_message(f"[СЕРВЕР]: Зараз в онлайн {count} студентів.")
        if count > 0:

            ports_list = ", ".join([str(c_addr[1]) for _, c_addr in clients])
            log_message(f"Список портів: {ports_list}")

    else:
        # Звичайне повідомлення від викладача
        formatted_msg = f"[Викладач]: {msg}"
        log_message(formatted_msg)
        broadcast(formatted_msg)


# Функції для навігації по історії стрілочками вгору та вниз
def history_up(event):
    global history_index
    if history and history_index > 0:
        history_index -= 1
        entry_msg.delete(0, tk.END)
        entry_msg.insert(0, history[history_index])
    return "break"


def history_down(event):
    global history_index
    if history:
        if history_index < len(history) - 1:
            history_index += 1
            entry_msg.delete(0, tk.END)
            entry_msg.insert(0, history[history_index])
        else:
            history_index = len(history)
            entry_msg.delete(0, tk.END)
    return "break"


root = tk.Tk()
root.title("Final Project")
root.geometry("450x500")

log_chat = scrolledtext.ScrolledText(root, width=50, height=20, state=tk.DISABLED)
log_chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

frame_bottom = tk.Frame(root)
frame_bottom.pack(padx=10, pady=5, fill=tk.X)

entry_msg = tk.Entry(frame_bottom)
entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
entry_msg.bind("<Return>", send_message)
entry_msg.bind("<Up>", history_up)
entry_msg.bind("<Down>", history_down)


btn_send = tk.Button(frame_bottom, text="Send",command=send_message, font = ("Arial", 10))
btn_send.pack(side=tk.RIGHT)

# --- Головна частина програми ---
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 5000))
server.listen(10)  # Готові прийняти до 10 студентів

log_message("Сервер запущено! Чекаємо студентів...")
log_message("Команди:"
            "\n //kick [port]"
            "\n //mute [port] [time]"
            "\n //unmute [port]"
            "\n //online"
            "\n //help"
            )

# Запускаємо процес прийняття підключень у фоновому потоці
accept_thread = threading.Thread(target=accept_connections, args=(server,), daemon=True)
accept_thread.start()

root.mainloop()