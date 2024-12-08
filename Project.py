import os
import time 

# fungsi "kendaraan" membuat dictionary berisi data kendaraan: plat nomor, jenis kendaraan, saldo awal, dan pintu masuk
def kendaraan(plat_nomor, jenis_kendaraan, saldo=0, masuk=None):
    return {
        "plat_nomor": plat_nomor,
        "jenis_kendaraan": jenis_kendaraan,
        "saldo": saldo,
        "masuk": masuk
    }

# fungsi "saldo_akhir" mengecek apakah saldo kendaraan mencukupi untuk membayar tarif tol.
def saldo_akhir(kendaraan, tarif):
    if kendaraan["saldo"] >= tarif:
        kendaraan["saldo"] -= tarif
        return True
    else:
        return False

# fungsi "hitung_tarif" akan menghitung tarif tol yang perlu dibayar pengguna kendaraan
def hitung_tarif(masuk, keluar, jenis_kendaraan):
    rute_tol = {
        ("kopo", "toha"): {"mobil": 5500, "truk": 11000, "bus": 8250},
        ("kopo", "buahbatu"): {"mobil": 5500, "truk": 11000, "bus": 8250},
        ("kopo", "cileunyi"): {"mobil": 6500, "truk": 13000, "bus": 9750},
        ("toha", "buahbatu"): {"mobil": 2500, "truk": 5000, "bus": 3750},
        ("toha", "cileunyi"): {"mobil": 5500, "truk": 11000, "bus": 8250},
        ("buahbatu", "cileunyi"): {"mobil": 5500, "truk": 11000, "bus": 8250},
        ("kopo", "kopo"): {"mobil": 13000, "truk": 26000, "bus": 19500},
        ("toha", "toha"): {"mobil": 13000, "truk": 26000, "bus": 19500},
        ("buahbatu", "buahbatu"): {"mobil": 13000, "truk": 26000, "bus": 19500},
        ("cileunyi", "cileunyi"): {"mobil": 13000, "truk": 26000, "bus": 19500}
    }
    rute = (masuk, keluar)
    if rute in rute_tol:
        return rute_tol[rute].get(jenis_kendaraan)
    else:
        rute = (keluar, masuk)
        return rute_tol.get(rute, {}).get(jenis_kendaraan)

# fungsi "gerbang_keluar" dipakai ketika kendaraan keluar dari tol
# fungsi ini memproses:
# Menghitung tarif tol berdasarkan gerbang masuk, keluar, dan jenis kendaraan.
# Memanggil saldo_akhir untuk mengecek dan memotong saldo jika mencukupi.
# Jika saldo cukup, saldo akan dipotong, dan gerbang otomatis terbuka.
# Jika saldo tidak mencukupi, pesan bahwa saldo tidak cukup akan ditampilkan, beserta jumlah tarif untuk pembayaran manual.
def gerbang_keluar(kendaraan, keluar):
    tarif_tol = hitung_tarif(kendaraan["masuk"], keluar, kendaraan["jenis_kendaraan"])
    if tarif_tol is None:
        print(f"Rute dari {kendaraan['masuk']} ke {keluar} tidak tersedia.")
        return False
    if saldo_akhir(kendaraan, tarif_tol):
        print(f"Saldo kendaraan {kendaraan['plat_nomor']} dipotong sebesar {tarif_tol}, rute yang dilalui {kendaraan['masuk']} - {keluar}. Sisa saldo: {kendaraan['saldo']}")
        time.sleep(1)
        print("Gerbang Terbuka")
        return True
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Kendaraan {kendaraan['plat_nomor']} tidak memiliki saldo yang cukup untuk melalui rute {kendaraan['masuk']} - {keluar}.")
        time.sleep(1)
        print(f"Silahkan lakukan pembayaran manual senilai {tarif_tol}")
        time.sleep(1)
        input("Tekan Enter jika pembayaran berhasil")
        print("Pembayaran manual berhasil!")
        print("Gerbang Terbuka")
        return False

# Fungsi "tambah_kendaraan" meminta pengguna untuk memasukkan informasi kendaraan.
def tambah_kendaraan():
    plat_nomor = input("Masukkan Plat Nomor: ")
    jenis_kendaraan = input("Masukkan jenis kendaraan (mobil, truk, bus): ").lower()
    saldo = float(input("Masukkan saldo kendaraan: "))
    masuk = input("Masukkan gerbang masuk kendaraan (Kopo, Toha, Buahbatu, Cileunyi): ").lower()
    return kendaraan(plat_nomor, jenis_kendaraan, saldo, masuk)

def main():
    # kendaraan_list adalah list untuk menyimpan data semua kendaraan yang ditambahkan.
    kendaraan_list = []

    # Menambahkan data kendaraan ke dalam sistem
    while True:
        tambah_lagi = input("Tambah kendaraan lain? (ya/tidak): ").strip().lower()
        if tambah_lagi == 'ya':
            kdr = tambah_kendaraan()
            kendaraan_list.append(kdr)
        else:
            break

    # Memilih kendaraan dengan plat nomor untuk diproses saat kendaraan hendak keluar tol
    while True:
        print("\nDaftar kendaraan:")
        for kdr in kendaraan_list:
            print(f"Plat Nomor: {kdr['plat_nomor']}, Jenis: {kdr['jenis_kendaraan']}, Saldo: {kdr['saldo']}, Gerbang Masuk: {kdr['masuk']}")

        plat_nomor = input("Masukkan plat nomor kendaraan yang ingin diproses: ").strip()
        
        # Mencari kendaraan berdasarkan plat nomor
        kendaraan_dipilih = None
        for k in kendaraan_list:
            if k["plat_nomor"] == plat_nomor:
                kendaraan_dipilih = k
                break
        
        # kendaraan terpilih akan diproses di gerbang keluar
        if kendaraan_dipilih:
            keluar = input("Masukkan gerbang keluar kendaraan (Kopo, Toha, Buahbatu, Cileunyi): ")
            gerbang_keluar(kendaraan_dipilih, keluar)
        else:
            print("Plat nomor tidak ditemukan dalam daftar kendaraan.")

        lanjut = input("Apakah Anda ingin memproses kendaraan lain? (ya/tidak): ").strip().lower()
        if lanjut != 'ya':
            break

if __name__ == "__main__":
    main()
