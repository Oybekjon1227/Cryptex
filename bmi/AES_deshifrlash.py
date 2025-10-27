from Crypto.Cipher import AES
from open_file import file_path
import os
from tkinter import messagebox

def load_key():
    """keys papkasidan secret.key faylini avtomatik o‘qiydi."""
    key_path = os.path.join("keys", "secret.key")

    if not os.path.exists(key_path):
        messagebox.showerror("Xatolik", f"Kalit topilmadi!\n{key_path}")
        raise FileNotFoundError(f"Kalit fayli topilmadi: {key_path}")

    with open(key_path, "rb") as f:
        return f.read()

def decrypt_message():
    """Tanlangan faylni AES yordamida deshifrlaydi."""
    path = file_path()  # Foydalanuvchi tanlagan fayl
    if not path:
        messagebox.showwarning("Ogohlantirish", "Fayl tanlanmadi.")
        return ""

    with open(path, "rb") as f:
        data = f.read()

    key = load_key()

    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]

    try:
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        message = cipher.decrypt_and_verify(ciphertext, tag)
        print("📩 Deshifrlangan xabar:", message.decode())
        return message.decode()
    except Exception as e:
        messagebox.showerror("Xatolik", f"Deshifrlashda xato: {e}")
        return ""

def appearal():
    """GUI tomonidan chaqiriladigan soddalashtirilgan funksiya."""
    decode = decrypt_message()
    return decode

if __name__ == "__main__":
    decrypt_message()
