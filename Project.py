kendaraan=["*" for i in range (4)]
for i in range (4):
  kendaraan[i]=str(input()) #saat tap kartu data kendaraan tercatat [plat nomor, jenis kendaraan, gerbang masuk, saldo e-toll]
print ("sisa saldo e-toll anda sebesar Rp.", kendaraan[4] ) # gerbang terbuka

