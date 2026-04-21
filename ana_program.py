import tkinter as tk
from motor import BulmacaMotoru
from arayuz import BulmacaArayuz
import ayarlar as opt

def calistir():
    root = tk.Tk()
    root.title(opt.BASLIK)
    
    # Pencerenin boyutunu sabitle (Kullanıcı büyütüp küçültemesin, arayüz bozulmasın)
    root.resizable(False, False)
    
    # Motoru başlat
    oyun_motoru = BulmacaMotoru()
    oyun_motoru.karistir()
    
    # Arayüzü başlat
    app = BulmacaArayuz(root, oyun_motoru)
    
    root.mainloop()

if __name__ == "__main__":
    calistir()
