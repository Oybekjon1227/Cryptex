from AES_shifrlash import appeal
from AES_deshifrlash import appearal
from kalit_almashish import run

import tkinter as tk
from tkinter import messagebox



def shifrlash():
    matn = textbox.get("1.0", "end").strip()
    
    # Agar bo‘sh bo‘lsa
    if not matn:
        messagebox.showwarning("Xato", "Matn kiritilmagan!")
    else:
        appeal(matn)

def deshifrlash():
    decode = appearal() 
    textbox.delete("1.0", "end")
    textbox.insert("1.0", decode)
    # messagebox.showinfo("Deshifrlash", "Bu joyda deshifrlash funksiyasi ishlaydi!")

def yordam():
    messagebox.showinfo("Yordam", "Matnni kiriting va tegishli tugmani bosing.")

def kalit_almashish():
    run()
    # messagebox.showinfo("Kalit almashish", "Bu joyda kalit almashish funksiyasi ishlaydi!")


# === Asosiy GUI ishga tushirish (faqat main.py ishga tushganda) ===
if __name__ == "__main__":
    # --- Oyna yaratamiz ---
    oyna = tk.Tk()
    oyna.title("Shifrlash dasturi")
    oyna.geometry("600x300")
    oyna.resizable(False, False)

    # --- Tugmalar joylashuvi ---
    frame_tugmalar = tk.Frame(oyna)
    frame_tugmalar.pack(pady=20)

    btn_width = 15
    btn1 = tk.Button(frame_tugmalar, text="Shifrlash", width=btn_width, command=shifrlash)
    btn2 = tk.Button(frame_tugmalar, text="Deshifrlash", width=btn_width, command=deshifrlash)
    btn3 = tk.Button(frame_tugmalar, text="Yordam", width=btn_width, command=yordam)
    btn4 = tk.Button(frame_tugmalar, text="Kalit almashish", width=btn_width, command=kalit_almashish)

    btn1.grid(row=0, column=0, padx=5)
    btn2.grid(row=0, column=1, padx=5)
    btn3.grid(row=0, column=2, padx=5)
    btn4.grid(row=0, column=3, padx=5)

    # --- Matn maydoni ---
    textbox = tk.Text(oyna, height=10, font=("Arial", 12))
    textbox.pack(padx=15, fill='x', pady=20)

    # --- Oyna ishga tushadi ---
    oyna.mainloop()
