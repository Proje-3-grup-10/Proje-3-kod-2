import tkinter as tk
from tkinter import messagebox
from motor import BulmacaMotoru
from arayuz import BulmacaArayuz
import ayarlar as opt

def calistir():
    root = tk.Tk()
    root.title(opt.BASLIK)
    
    # Pencerenin boyutunu sabitle (Kullanıcı büyütüp küçültemesin, arayüz bozulmasın)
    root.resizable(False, False)

    # Başlangıçta kullanıcıya soruyoruz
    cevap = messagebox.askyesno("Oyun Modu", "Resimli oynamak ister misiniz?\n(Evet: Resimli, Hayir: Sayili 1-8)")
    mod = "resim" if cevap else "sayi"
    
    # Motoru başlat
    oyun_motoru = BulmacaMotoru()
    oyun_motoru.karistir()
    
    # Arayüzü başlat
    app = BulmacaArayuz(root, oyun_motoru, mod)
    
    root.mainloop()

if __name__ == "__main__":
    calistir()
