import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import ayarlar as opt

class BulmacaArayuz:
    def __init__(self, pencere, motor, mod):
        self.pencere = pencere
        self.motor = motor
        self.mod=mod
        self.parcalar = {} # 1-8 arasındaki parçaların resimlerini tutar
        self.son_parca_gorseli = None # Sağ alt köşe parçası, kazanılınca gösterilecek
        self.bos_gorsel = None # Oyun sırasında boş hücre için kullanılacak görsel
        self.butonlar = [] # Buton nesnelerini tutar

        if self.mod=="resim":
            self.resim_sec_ve_hazirla()
        else:
            self.pencere.geometry(f"{opt.PENCERE_BOYUTU}x{opt.PENCERE_BOYUTU}")
            self.butonlari_olustur()

    def resim_sec_ve_hazirla(self):
        yol = filedialog.askopenfilename(filetypes=[("Resim Dosyaları", "*.jpg *.png *.jpeg")])
        if not yol:
            self.pencere.destroy()
            return
        
        tam_resim = ImageOps.fit(Image.open(yol),(opt.PENCERE_BOYUTU, opt.PENCERE_BOYUTU), centering=(0.5, 0.5))
        
        # Resmi 3x3 parçaya böl
        kırpılan_parçalar = []
        for r in range(opt.BOYUT):
            for c in range(opt.BOYUT):
                kutu = (c*opt.HUCRE_BOYUTU, r*opt.HUCRE_BOYUTU, (c+1)*opt.HUCRE_BOYUTU, (r+1)*opt.HUCRE_BOYUTU)
                parca = tam_resim.crop(kutu)
                kırpılan_parçalar.append(ImageTk.PhotoImage(parca))
        
        # İlk 8 parçayı oyunda kullanılacak 'parcalar' sözlüğüne (1..8 anahtarlarıyla) ekle
        for i in range(1, 9):
            self.parcalar[i] = kırpılan_parçalar[i-1]
        
        # 9. (son) parçayı gizlemek üzere sakla (p7 -> parcalar[8] olduğu için 8 numaralı parça)
        # Hayır, 3x3'te parçalar 0'dan 8'e kadardır. Son parça (sağ alt) index 8'dir.
        # Bizim motorumuzda parça numaraları 1'den 8'e kadar. Yani, motorun 8 numaralı parçası,
        # arayüzün 8. karesidir. Son parça (9.) gizlenecektir.
        
        # Sonuç: Parçalar 1..8 arası hareket edecek. Motorun '0' değeri arayüzde boş hücredir.
        # 9. parça (sağ alt) oyuna dahil edilmeyecek.
        # Son parça indeksini al: BOYUT * BOYUT - 1. Bu 3x3 için 8. indeks.
        self.son_parca_gorseli = kırpılan_parçalar[opt.BOYUT * opt.BOYUT - 1]
        
        # Oyun sırasında boş hücre için düz renkli bir görsel hazırla
        bos_resim = Image.new('RGB', (opt.HUCRE_BOYUTU, opt.HUCRE_BOYUTU), color='darkgrey')
        self.bos_gorsel = ImageTk.PhotoImage(bos_resim)
        
        self.butonlari_olustur()

    def butonlari_olustur(self):
        for r in range(opt.BOYUT):
            satir_btns = []
            for c in range(opt.BOYUT):
                # Butonların kenarlıklarını minimal tutarak parçalar arasındaki geçişi iyileştir
                btn = tk.Button(self.pencere, relief="flat", borderwidth=1,
                               command=lambda r=r, c=c: self.tikla(r, c))
                btn.grid(row=r, column=c)
                satir_btns.append(btn)
            self.butonlar.append(satir_btns)
        self.guncelle()

    def guncelle(self):
        for r in range(opt.BOYUT):
            for c in range(opt.BOYUT):
                deger = self.motor.tahta[r][c]
                # Eğer hücre boşsa (motorun tahtasında 0 ise)
                if deger == 0:
                    # Oyun kazanıldıysa, bu boş hücreyi saklanan son parça ile doldur
                    if self.motor.kazandi_mi() and r == (opt.BOYUT - 1) and c == (opt.BOYUT - 1):
                        self.butonlar[r][c].config(image=self.son_parca_gorseli)
                    # Oyun devam ediyorsa, boş slot görselini göster
                    else:
                        self.butonlar[r][c].config(image=self.bos_gorsel)
                # Diğer durumlarda (1..8 parçaları), parçanın kendi resmini göster
                else:
                    self.butonlar[r][c].config(image=self.parcalar[deger])

    def tikla(self, r, c):
        if self.motor.hareket_et(r, c):
            self.guncelle()
            if self.motor.kazandi_mi():
                messagebox.showinfo("Tebrikler!", "Bulmacayı çözdünüz ve resim tamamlandı!")
