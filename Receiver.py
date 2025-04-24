import tkinter as tk
from tkinter import messagebox
import serial
import serial.tools.list_ports
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

last_message = None

def read_messages():
    global last_message
    try:
        if ser.in_waiting > 0:
            #raw_message = ser.readline().decode('utf-8').strip()
            raw_message = ser.readline().decode('utf-8', errors='ignore').strip()
            if raw_message and raw_message != last_message:
                if '|' in raw_message:
                    encrypted_b64, key_b64 = raw_message.split('|', 1)
                    message_listbox.insert(tk.END, f"Received message: {encrypted_b64} |  Received Key: {key_b64}")
                    message_listbox.yview(tk.END)
                    if encrypted_b64 and key_b64:
                        try:
                            # Decode from base64
                            encrypted_message = base64.b64decode(encrypted_b64).decode('utf-8')
                            key = base64.b64decode(key_b64).decode('utf-8')

                            # Decrypt the message using XOR
                            decrypted_message = xor_encrypt_decrypt(encrypted_message, key)

                            # Display the decrypted message
                            message_listbox.insert(tk.END, f"Decrypted: {decrypted_message}")
                            message_listbox.yview(tk.END)

                            last_message = raw_message
                        except Exception as e:
                            message_listbox.insert(tk.END, f"Decryption failed: {e}")
                    else:
                        message_listbox.insert(tk.END, "Error: Incomplete message received.")
                else:
                    print(raw_message)
                    message_listbox.insert(tk.END, "Error: Invalid message format. No key found.")
        root.after(100, read_messages)
    except Exception as e:
        status_label.config(text=f"Error: {e}", fg="red")

def close_connection():
    try:
        ser.close()
        status_label.config(text="Connection closed.", fg="red")
    except Exception as e:
        messagebox.showerror("Error", f"Error closing connection: {e}")
    root.destroy()

root = tk.Tk()
root.title("Python Receiver")

status_label = tk.Label(root, text="Detecting ports...", fg="gray")
status_label.pack(pady=5)

ser = find_available_port()

message_listbox = tk.Listbox(root, width=60, height=20)
message_listbox.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=close_connection, bg="lightcoral")
exit_button.pack(pady=10)

read_messages()

root.protocol("WM_DELETE_WINDOW", close_connection)  # Close safely
root.mainloop()
