import tkinter as tk
from tkinter import messagebox
import serial
import serial.tools.list_ports
import random
import string
import base64

# XOR encryption and decryption function
def xor_encrypt_decrypt(data, key):
    return ''.join(chr(ord(data[i]) ^ ord(key[i % len(key)])) for i in range(len(data)))

# Auto-detect available ports
def find_available_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            ser = serial.Serial(port.device, 9600, timeout=1)
            status_label.config(text=f"Connected to virtual port on {port.device}", fg="green")
            return ser
        except (serial.SerialException, OSError):
            continue
    messagebox.showerror("Error", "No available ports found. Exiting...")
    exit()

# Send an encrypted message to the virtual receiver
def send_message():
    message = message_entry.get()
    if message.strip():
        try:
            # Generate a random key for XOR encryption
            key = ''.join(random.choices(string.ascii_letters + string.digits, k=len(message)))

            # XOR encryption
            encrypted_message = xor_encrypt_decrypt(message, key)

            # Encode the encrypted message and key in base64
            encrypted_b64 = base64.b64encode(encrypted_message.encode('utf-8')).decode('utf-8')
            key_b64 = base64.b64encode(key.encode('utf-8')).decode('utf-8')

            encrypted_entry.config(state=tk.NORMAL)
            encrypted_entry.delete(0, tk.END)
            encrypted_entry.insert(0, encrypted_b64)
            encrypted_entry.config(state=tk.DISABLED)

            key_entry.config(state=tk.NORMAL)
            key_entry.delete(0, tk.END)
            key_entry.insert(0, key_b64)
            key_entry.config(state=tk.DISABLED)

            ser.write((encrypted_b64 + '|' + key_b64 + '\n').encode('utf-8'))
            status_label.config(text=f"Encrypted and sent: {message}", fg="blue")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")
    else:
        messagebox.showwarning("Warning", "Please enter a message to send!")

def close_connection():
    try:
        ser.close()
        status_label.config(text="Connection closed.", fg="red")
    except Exception as e:
        messagebox.showerror("Error", f"Error closing connection: {e}")
    root.destroy()

root = tk.Tk()
root.title("Python Transmitter")

status_label = tk.Label(root, text="Detecting ports...", fg="gray")
status_label.pack(pady=5)

ser = find_available_port()

message_label = tk.Label(root, text="Enter message:")
message_label.pack(pady=5)
message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=5)

send_button = tk.Button(root, text="Send Message", command=send_message, bg="lightgreen")
send_button.pack(pady=10)

tk.Label(root, text="Encrypted Message:").pack(pady=5)
encrypted_entry = tk.Entry(root, width=50, state=tk.DISABLED)
encrypted_entry.pack(pady=5)

tk.Label(root, text="Encryption Key:").pack(pady=5)
key_entry = tk.Entry(root, width=50, state=tk.DISABLED)
key_entry.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=close_connection, bg="lightcoral")
exit_button.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", close_connection)  # Close safely
root.mainloop()