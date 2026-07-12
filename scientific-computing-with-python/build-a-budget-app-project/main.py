class Kategori:
    def __init__(self, nama):
        self.nama = nama
        self.buku_besar = []
    
    def deposit(self, jumlah, deskripsi=""):
        self.buku_besar.append({"jumlah": jumlah, "deskripsi": deskripsi})
    
    def tarik(self, jumlah, deskripsi=""):
        if self.cek_dana(jumlah):
            self.buku_besar.append({"jumlah": -jumlah, "deskripsi": deskripsi})
            return True
        return False
    
    def get_saldo(self):
        return sum(item["jumlah"] for item in self.buku_besar)
    
    def transfer(self, jumlah, kategori):
        if self.cek_dana(jumlah):
            self.tarik(jumlah, f"Transfer ke {kategori.nama}")
            kategori.deposit(jumlah, f"Transfer dari {self.nama}")
            return True
        return False
    
    def cek_dana(self, jumlah):
        return jumlah <= self.get_saldo()
    
    def __str__(self):
        # Baris judul - 30 karakter dengan nama di tengah, diisi bintang
        judul = self.nama.center(30, "*")
        
        # Item buku besar
        item_baris = ""
        for item in self.buku_besar:
            deskripsi = item["deskripsi"][:23]
            jumlah = f"{item['jumlah']:.2f}"
            item_baris += f"{deskripsi:<23}{jumlah:>7}\n"
        
        # Total
        total = f"Total: {self.get_saldo():.2f}"
        
        return f"{judul}\n{item_baris}{total}"


def buat_grafik_pengeluaran(kategori_list):
    # Hitung total penarikan untuk setiap kategori
    penarikan = []
    for kategori in kategori_list:
        total_ditarik = 0
        for item in kategori.buku_besar:
            if item["jumlah"] < 0:
                total_ditarik += -item["jumlah"]
        penarikan.append(total_ditarik)
    
    # Hitung persentase
    total_pengeluaran = sum(penarikan)
    if total_pengeluaran > 0:
        persentase = [(pengeluaran / total_pengeluaran) * 100 for pengeluaran in penarikan]
    else:
        persentase = [0] * len(kategori_list)
    
    # Bulatkan ke bawah ke kelipatan 10 terdekat
    persentase_terbulat = [int(p // 10) * 10 for p in persentase]
    
    # Bangun grafik
    grafik = "Percentage spent by category\n"
    
    # Sumbu Y dan batang (dari 100 turun ke 0)
    for i in range(100, -1, -10):
        grafik += f"{i:>3}| "
        for p in persentase_terbulat:
            if p >= i:
                grafik += "o  "
            else:
                grafik += "   "
        grafik += "\n"
    
    # Garis horizontal
    grafik += "    " + "-" * (len(kategori_list) * 3 + 1) + "\n"
    
    # Nama kategori secara vertikal
    panjang_maks = 0
    for kategori in kategori_list:
        if len(kategori.nama) > panjang_maks:
            panjang_maks = len(kategori.nama)
    
    for i in range(panjang_maks):
        grafik += "     "
        for kategori in kategori_list:
            if i < len(kategori.nama):
                grafik += kategori.nama[i] + "  "
            else:
                grafik += "   "
        if i < panjang_maks - 1:
            grafik += "\n"
    
    return grafik


# Contoh penggunaan dengan method yang benar
if __name__ == "__main__":
    # Membuat kategori
    makanan = Kategori("Food")
    pakaian = Kategori("Clothing")
    hiburan = Kategori("Entertainment")
    
    # Melakukan transaksi - menggunakan method yang benar: tarik() bukan withdraw()
    makanan.deposit(1000, "deposit")
    makanan.tarik(10.15, "groceries")
    makanan.tarik(15.89, "restaurant and more food")
    makanan.transfer(50, pakaian)
    
    pakaian.deposit(500, "deposit")
    pakaian.tarik(25.55, "shoes")
    
    hiburan.deposit(1000, "deposit")
    hiburan.tarik(125, "concert tickets")
    
    # Menampilkan setiap kategori
    print(makanan)
    print()
    print(pakaian)
    print()
    print(hiburan)
    print()
    
    # Menampilkan grafik pengeluaran
    print(buat_grafik_pengeluaran([makanan, pakaian, hiburan]))
