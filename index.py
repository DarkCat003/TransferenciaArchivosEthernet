import socket
import threading
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
import base64
import os

SAVE_DIR = r"C:\ArchivosRecibidos"
PORT = 5000
BUFFER_SIZE = 4096

# ---------- CIFRADO CESAR ----------
def get_shift(key):
    return sum(ord(c) for c in key) % 256

def caesar_encrypt(data, key):
    shift = get_shift(key)
    return bytes((b + shift) % 256 for b in data)

def caesar_decrypt(data, key):
    shift = get_shift(key)
    return bytes((b - shift) % 256 for b in data)

# ---------- RED ----------
def start_server():
    def server_thread():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((entry_ip.get(), PORT))
            s.listen(1)
            log("Esperando conexión...")
            conn, addr = s.accept()
            log(f"Conectado con {addr}")

            while True:
                header = conn.recv(10).decode()
                if not header:
                    break

                size = int(header.strip())
                encrypted = b""
                while len(encrypted) < size:
                    encrypted += conn.recv(BUFFER_SIZE)

                key = entry_key.get()
                data = caesar_decrypt(base64.b64decode(encrypted), key)

                if data.startswith(b"FILE:"):
                    name_len = int(data[5:8])
                    name = data[8:8+name_len].decode()
                    file_data = data[8+name_len:]
                    os.makedirs(SAVE_DIR, exist_ok=True)
                    with open(os.path.join(SAVE_DIR, "recibido_" + name), "wb") as f:
                        f.write(file_data)
                    log(f"Archivo recibido: {name}")
                else:
                    log("Mensaje recibido:")
                    log(data.decode())

        except Exception as e:
            messagebox.showerror("Error", str(e))

    threading.Thread(target=server_thread, daemon=True).start()

def send_text():
    try:
        key = entry_key.get()
        text = text_box.get("1.0", tk.END).encode()
        encrypted = caesar_encrypt(text, key)
        encoded = base64.b64encode(encrypted)

        send_data(encoded)
        log("Texto enviado")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def send_file():
    try:
        path = filedialog.askopenfilename()
        if not path:
            return

        key = entry_key.get()
        name = os.path.basename(path).encode()
        with open(path, "rb") as f:
            data = f.read()

        payload = b"FILE:" + f"{len(name):03}".encode() + name + data
        encrypted = caesar_encrypt(payload, key)
        encoded = base64.b64encode(encrypted)

        send_data(encoded)
        log(f"Archivo enviado: {name.decode()}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def send_data(encoded):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((entry_ip.get(), PORT))
    header = f"{len(encoded):<10}".encode()
    s.sendall(header + encoded)
    s.close()

# Apariencia global
ctk.set_appearance_mode("dark")      # "light" o "system"
ctk.set_default_color_theme("blue")  # "green", "dark-blue", etc.

# ---------- GUI ----------
def log(msg):
    output.insert(tk.END, msg + "\n")
    output.see(tk.END)

root = ctk.CTk()
root.title("Comunicación Ethernet Directa")
root.geometry("420x520")

# IP
label_ip = ctk.CTkLabel(root, text="IP destino / local:")
label_ip.pack(pady=(10, 0))

entry_ip = ctk.CTkEntry(root, width=300)
entry_ip.pack(pady=5)

# Llave
label_key = ctk.CTkLabel(root, text="Llave (frase):")
label_key.pack(pady=(10, 0))

entry_key = ctk.CTkEntry(root, width=300, show="*")
entry_key.pack(pady=5)

# Botón servidor
btn_server = ctk.CTkButton(
    root,
    text="Iniciar Servidor (Recibir)",
    command=start_server
)
btn_server.pack(pady=10)

# Caja de texto para enviar
text_box = tk.Text(root, height=5, width=45)
text_box.pack(pady=5)

# Botones de envío
btn_send_text = ctk.CTkButton(
    root,
    text="Enviar Texto",
    command=send_text
)
btn_send_text.pack(pady=4)

btn_send_file = ctk.CTkButton(
    root,
    text="Enviar Archivo",
    command=send_file
)
btn_send_file.pack(pady=4)

# Output / log
output = tk.Text(root, height=10, width=45)
output.pack(pady=10)

root.mainloop()
