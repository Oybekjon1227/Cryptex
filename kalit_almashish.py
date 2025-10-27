import tkinter as tk
from ECDH_key_generate import ecdh_key_generate
from AES_key_generate import aes_key_generate

def button1_action():
    
    ecdh_key_generate()

def button2_action():
    
    aes_key_generate()
    
def run():
    root = tk.Tk()
    root.title("Kalit almashish")
    root.geometry("200x100")

    btn1 = tk.Button(root, text="create a key", command=button1_action)
    btn1.pack(pady=10)

    btn2 = tk.Button(root, text="receiving key", command=button2_action)
    btn2.pack(pady=10)

    root.mainloop()
