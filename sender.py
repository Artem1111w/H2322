import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
#10.0.3.224
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('10.0.3.35',5000))


root = tk.Tk()
root.title("Записка qq")
root.geometry('450x500')

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD,font=("Arial", 12))
chat_area.pack(padx= 10,pady= 10, fill=tk.BOTH, expand=True)
chat_area.config(state= tk.DISABLED)

msg_entry = tk.Entry(root, font=("Arial",14))
msg_entry.pack(padx= 10,pady= 10, fill=tk.X, expand=True)

def send_msg(event=None):
    text = msg_entry.get()
    if text:
        client.send(text.encode('utf-8'))
        msg_entry.delete(0, tk.END)
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, text + "\n")
        chat_area.yview(tk.END)
        chat_area.config(state=tk.DISABLED)



send_btn = tk.Button(
    root,
    text="Send",
    command=send_msg,
    bg="green",
    font=("Arial",10)
)
send_btn.pack(side=tk.RIGHT, padx= 10,pady= 10)

msg_entry.bind("<Return>", send_msg)


def lister_to_server(client):
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            msg = data.decode('utf-8')

            chat_area.config(state=tk.NORMAL)
            chat_area.insert(tk.END, msg + "\n")
            chat_area.yview(tk.END)
            chat_area.config(state=tk.DISABLED)

        except:
            break


lister_thread= threading.Thread(target=lister_to_server, args=(client,))
lister_thread.start()

root.mainloop()
