import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, messagebox
from tkinter import ttk

class ChatClientGUI:
    def __init__(self, root, client_id):
        self.root = root
        self.root.title(f"Chat Client - Cliente {client_id}")

        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use the "clam" theme for a modern appearance

        self.client_id = client_id

        self.chat_window = scrolledtext.ScrolledText(self.root, state='disabled', wrap=tk.WORD)
        self.chat_window.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.message_entry = Entry(self.root, font=("Helvetica", 12))
        self.message_entry.pack(padx=10, pady=5, expand=True, fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)  # Send message on Enter key press

        self.send_button = Button(self.root, text="Send", command=self.send_message, font=("Helvetica", 12))
        self.send_button.pack(padx=10, pady=5)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1", 12345))

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def send_message(self, event=None):  # event argument is added for the key binding
        message = self.message_entry.get()
        if message:
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.message_entry.delete(0, tk.END)
                self.display_message(f"Você: {message}")  # Exibe a mensagem do próprio cliente
            except:
                messagebox.showerror("Error", "Failed to send message. Please try again.")

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                self.display_message(message)
            except:
                break

    def display_message(self, message):
        self.chat_window.config(state='normal')
        self.chat_window.insert(tk.END, message + '\n')
        self.chat_window.config(state='disabled')
        self.chat_window.see(tk.END)

def main():
    root = tk.Tk()
    app = ChatClientGUI(root, client_id=2)  # Altere o valor de client_id conforme necessário
    root.mainloop()

if __name__ == "__main__":
    main()
