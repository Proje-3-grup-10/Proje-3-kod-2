import random
import ayarlar as opt

class BulmacaMotoru:
    def __init__(self):
        self.size = opt.BOYUT
        self.tahta = []
        self.hedef = []
        self.kurulum()

    def kurulum(self):
        # 1'den 8'e kadar sayıları oluştur ve sonuna 0 (boşluk) ekle
        # 0 her zaman boş hücreyi temsil eder. Son parça gizleneceği için
        # hedef durumumuz [[1, 2, 3], [4, 5, 6], [7, 8, 0]] olmalıdır.
        sayilar = list(range(1, self.size * self.size)) + [0]
        self.hedef = [sayilar[i:i + self.size] for i in range(0, len(sayilar), self.size)]
        # Mevcut tahtayı hedefin kopyası olarak başlat
        self.tahta = [satir[:] for satir in self.hedef]

    def bosluk_bul(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.tahta[r][c] == 0:
                    return r, c

    def hareket_et(self, r, c):
        br, bc = self.bosluk_bul()
        # Eğer tıklanan hücre boşluğun yanındaysa (mesafe 1 ise) yer değiştir
        if abs(r - br) + abs(c - bc) == 1:
            self.tahta[br][bc], self.tahta[r][c] = self.tahta[r][c], self.tahta[br][bc]
            return True
        return False

    def karistir(self):
        # Çözülebilir bir oyun için rastgele 150 geçerli hamle yap
        hamle = 0
        while hamle < 150:
            r, c = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if self.hareket_et(r, c):
                hamle += 1

    def kazandi_mi(self):
        # Tahta ile hedef durum aynı mı kontrol et
        return self.tahta == self.hedef
