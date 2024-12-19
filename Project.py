import os
import time
import cv2

# Data rute dan tarif tol
rute_tol = {
        ("baros","pasirkoja"): {"mobil": 4000, "truk": 9000, "bus": 6500},
        ("baros","kopo"): {"mobil": 4000, "truk": 9000, "bus": 6500},
        ("baros","toha"): {"mobil": 5500, "truk": 12000, "bus": 8500},
        ("baros","buahbatu"): {"mobil": 5500, "truk": 12000, "bus": 8500},
        ("baros","cileunyi"): {"mobil": 7500, "truk": 17500, "bus": 13000},
        ("pasirkoja","kopo"):{"mobil": 2500, "truk": 6000, "bus": 4500},
        ("pasirkoja","toha"): {"mobil": 4000, "truk": 9000, "bus": 6500},
        ("pasirkoja","buahbatu"): {"mobil": 4000, "truk": 9000, "bus": 6500},
        ("pasirkoja","cileunyi"): {"mobil": 7500, "truk": 17500, "bus": 13000},
        ("kopo", "toha"): {"mobil": 2500, "truk": 6000, "bus": 4500},
        ("kopo", "buahbatu"): {"mobil": 4000, "truk": 9000, "bus": 6500},
        ("kopo", "cileunyi"): {"mobil": 6500, "truk": 15000, "bus": 8000},
        ("toha", "buahbatu"): {"mobil": 2500, "truk": 6000, "bus": 4500},
        ("toha", "cileunyi"): {"mobil": 5000, "truk": 12000, "bus": 8500},
        ("buahbatu", "cileunyi"): {"mobil": 5000, "truk": 12000, "bus": 8500},
        ("kopo", "kopo"): {"mobil": 15000, "truk": 35000, "bus": 26000},
        ("toha", "toha"): {"mobil": 15000, "truk": 35000, "bus": 26000},
        ("buahbatu", "buahbatu"): {"mobil": 15000, "truk": 35000, "bus": 26000},
        ("cileunyi", "cileunyi"): {"mobil": 15000, "truk": 35000, "bus": 26000},
        ("pasirkoja","pasirkoja"): {"mobil": 15000, "truk": 35000, "bus": 26000},
        ("baros","baros"): {"mobil": 15000, "truk": 35000, "bus": 26000},
    }

# Fungsi menampilkan tabel tarif tol berdasarkan gerbang masuk
def tampilkan_tabel_tarif(masuk, jenis_kendaraan):
    print(f"\nTarif untuk gerbang masuk {masuk} (jenis kendaraan: {jenis_kendaraan}):")
    print(f"{'Gerbang Keluar':<15}{'Tarif':>10}")
    print("-" * 25)
    for (start, end), tarif in rute_tol.items():
        if start == masuk or end == masuk:
            print(f"{end if start == masuk else start:<15}{tarif[jenis_kendaraan]:>10}")

# Fungsi menghitung tarif
def hitung_tarif(masuk, keluar, jenis_kendaraan):
    rute = (masuk, keluar)
    if rute in rute_tol:
        return rute_tol[rute].get(jenis_kendaraan)
    else:
        rute = (keluar, masuk)
        return rute_tol.get(rute, {}).get(jenis_kendaraan)

# Fungsi gerbang keluar
def gerbang_keluar(kendaraan, keluar):
    tarif_tol = hitung_tarif(kendaraan["masuk"], keluar, kendaraan["jenis_kendaraan"])
    if tarif_tol is None:
        print(f"Rute dari {kendaraan['masuk']} ke {keluar} tidak tersedia.")
        return False
    if kendaraan["saldo"] >= tarif_tol:
        kendaraan["saldo"] -= tarif_tol
        print(f"Saldo kendaraan {kendaraan['plat_nomor']} dipotong sebesar {tarif_tol}. Sisa saldo: {kendaraan['saldo']}")
        print("Gerbang Terbuka")
        return True
    else:
        print(f"Saldo tidak mencukupi. Silakan bayar manual sebesar {tarif_tol}.")
        qris_image = cv2.imread("qris.jpg")
        if qris_image is not None:
            cv2.imshow("QRIS Pembayaran", qris_image)
            print("QRIS ditampilkan. Silakan scan untuk melakukan pembayaran.")
            print("Tekan tombol apa saja setelah pembayaran selesai.")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print("Pembayaran manual berhasil!")
            print("Gerbang Terbuka")
        return False

def main():
    # Database kendaraan
    kendaraan_list = [
        {"plat_nomor": "D1234ABC", "jenis_kendaraan": "mobil", "saldo": 0},
        {"plat_nomor": "B5678DEF", "jenis_kendaraan": "truk", "saldo": 75000},
        {"plat_nomor": "F91011GHI", "jenis_kendaraan": "bus", "saldo": 60000}
    ]

    # Memilih kendaraan
    print("Daftar kendaraan:")
    for i, kdr in enumerate(kendaraan_list, 1):
        print(f"{i}. Plat Nomor: {kdr['plat_nomor']}, Jenis: {kdr['jenis_kendaraan']}, Saldo: {kdr['saldo']}")

    pilihan = int(input("Pilih kendaraan (masukkan nomor): ")) - 1
    kendaraan_dipilih = kendaraan_list[pilihan]

    # Memilih gerbang masuk
    gerbang_masuk = input("Masukkan gerbang masuk (Kopo, Toha, Buahbatu, Cileunyi, Pasir Koja, Baros): ").lower()
    kendaraan_dipilih["masuk"] = gerbang_masuk

    # Menampilkan tabel tarif
    tampilkan_tabel_tarif(gerbang_masuk, kendaraan_dipilih["jenis_kendaraan"])
    print("Gerbang terbuka")
    time.sleep(10)
    os.system("cls" if os.name == "nt" else "clear")

    # Memilih gerbang keluar
    gerbang_keluar_user = input("Masukkan gerbang keluar (Kopo, Toha, Buahbatu, Cileunyi, Pasir Koja, Baros): ").strip().lower().replace(" ", "")
    gerbang_keluar(kendaraan_dipilih, gerbang_keluar_user)

if __name__ == "__main__":
    main()
