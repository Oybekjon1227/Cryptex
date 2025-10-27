from tkinter import Tk, filedialog

def fayl_tanlash():
    # Tk oynasini yashiramiz (faqat Explorer chiqadi)
    root = Tk()
    root.withdraw()

    fayl_path = filedialog.askopenfilename(
        title="Fayl tanlang",
        filetypes=[
            ("Barcha fayllar", "*.*"),
            ("Matn fayllari", "*.txt;*.md;*.py;*.json;*.csv"),
            ("Kalit fayllari", "*.key;*.pem;*.der")
        ]
    )
    root.destroy()  # oynani butunlay yopamiz
    return fayl_path if fayl_path else None

def file_path():
    path = fayl_tanlash()
    return path

# --- Sinov uchun ---
if __name__ == "__main__":
    path = fayl_tanlash()
    if path:
        print("Tanlangan fayl yo‘li:", path)
    else:
        print("Hech narsa tanlanmadi.")
