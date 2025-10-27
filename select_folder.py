import tkinter as tk
from tkinter import filedialog

def choose_folder():
    """
    File Explorer oynasini ochadi va foydalanuvchi tanlagan folder path ni qaytaradi.
    Agar Cancel bosilsa, None qaytaradi.
    """
    root = tk.Tk()
    root.withdraw()  # asosiy tk oynasini yashirish

    folder_path = filedialog.askdirectory(title="Papkani tanlang")
    
    if folder_path == "":
        return None
    return folder_path

# ===== Demo =====
if __name__ == "__main__":
    path = choose_folder()
    if path:
        print("Siz tanlagan folder:", path)
    else:
        print("Hech narsa tanlanmadi.")
