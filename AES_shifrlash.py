from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import tkinter as tk 
from tkinter import filedialog, messagebox


# === 🔑 Kalit bilan ishlash ===
def generate_key(key_dir="keys", key_filename="secret.key"):
    """32 baytli (256-bit) tasodifiy kalit yaratadi va keys papkasiga saqlaydi."""
    # Papkani avtomatik yaratamiz, agar mavjud bo‘lmasa
    os.makedirs(key_dir, exist_ok=True)
    
    key_path = os.path.join(key_dir, key_filename)
    key = get_random_bytes(32)
    with open(key_path, "wb") as f:
        f.write(key)

    print(f"✅ Kalit '{key_path}' faylga saqlandi.")
    return key


def load_key(key_dir="keys", key_filename="secret.key"):
    """Oldindan yaratilgan kalitni keys papkasidan o‘qish."""
    key_path = os.path.join(key_dir, key_filename)
    with open(key_path, "rb") as f:
        return f.read()


# === 🔒 Shifrlash funksiyasi ===
def encrypt_message_to_path(message, key, output_path):
    """Berilgan matnni AES bilan shifrlab, tanlangan joyga yozadi."""
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())

    # nonce, tag va ciphertextni birlashtiramiz
    data = cipher.nonce + tag + ciphertext

    # Papka mavjudligini tekshirish
    folder = os.path.dirname(output_path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(data)

    print(f"🔒 Xabar shifrlanib '{output_path}' faylga yozildi.")


# === 💾 Save As oynasi orqali saqlash ===
def appeal_save_as_dialog(message, key_dir="keys", key_filename="secret.key", default_filename="encrypted_message.bin"):
    """
    Tkinter 'Save As' dialog ochadi — foydalanuvchi joy va nomni tanlaydi.
    Tanlangan joyga AES bilan shifrlangan fayl yoziladi.
    """
    # Tkinter asosiy oynasini yashiramiz
    root = tk.Tk()
    root.withdraw()

    # Fayl nomi va turini sozlaymiz
    filetypes = [("Binary files", "*.bin"), ("All files", "*.*")]

    save_path = filedialog.asksaveasfilename(
        title="Saqlash (Save As)",
        initialfile=default_filename,
        defaultextension=".bin",
        filetypes=filetypes
    )

    if not save_path:
        print("❎ Saqlash bekor qilindi.")
        return False

    # Kalitni keys papkasidan yuklaymiz yoki yaratamiz
    try:
        key = load_key(key_dir, key_filename)
        print("🔑 Mavjud kalit fayldan o‘qildi.")
    except FileNotFoundError:
        key = generate_key(key_dir, key_filename)

    # Shifrlashni amalga oshiramiz
    encrypt_message_to_path(message, key, save_path)

    try:
        messagebox.showinfo("Muvaffaqiyat", f"Xabar shifrlanib:\n{save_path}\nga saqlandi.")
    except:
        pass

    return True


# === Asosiy chaqiruvchi ===
def appeal(message):
    success = appeal_save_as_dialog(message)
    if success:
        messagebox.showinfo("Muvaffaqiyat", "Xabar shifrlanib saqlandi.")
    else:
        messagebox.showerror("Xatolik", "Xabar shifrlanib saqlanmadi.")


# === Misol ishlatish ===
if __name__ == "__main__":
    text_to_encrypt = "Bu juda maxfiy xabar — Save As orqali saqlanadi."
    success = appeal_save_as_dialog(text_to_encrypt)
    if success:
        print("✅ Finish.")
    else:
        print("⚠️ Saqlash amalga oshmadi.")
