# Praktikum Blockchain

Mini blockchain sederhana berbasis Python untuk memahami konsep dasar penyimpanan blok, mining, Merkle tree, serta simulasi fork & reorganisasi chain.  

Blockchain adalah teknologi yang memungkinkan penyimpanan data dalam blok-blok yang saling terhubung. Setiap blok berisi transaksi dan dijamin keamanannya melalui proses mining. Mining dilakukan dengan mencari angka nonce yang menghasilkan hash dengan awalan nol sesuai tingkat kesulitan. Semua transaksi dalam blok dirangkum menjadi satu hash menggunakan struktur Merkle tree. Sistem validasi memastikan seluruh rantai blok tetap konsisten dan tidak dapat diubah.


## Cara Menjalankan

1. Setup Virtual Environment
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux/Mac

### 2. Jalankan Program dan Testing
python chain.py
python tests.py

### 3. Generate proof dan verifikasi
python cli.py --difficulty 3

### 4. Simulasi fork dan reorganisasi blockchain
python fork_sim.py


## Definisi Work
Work dalam blockchain diukur dari jumlah nol di awal hash blok. Semakin banyak nol berarti work lebih besar dan mining lebih sulit. Cumulative work adalah total work dari genesis block hingga blok terakhir dalam suatu chain.

## Aturan Best Tip
Sistem memilih best tip berdasarkan chain dengan cumulative work tertinggi. Jika cumulative work sama, chain dengan hash lexicographically lebih kecil yang dipilih. Aturan ini memastikan konsensus terdistribusi.

## Penjelasan REORG
REORG terjadi ketika chain alternatif memiliki cumulative work lebih tinggi daripada chain utama. Sistem secara otomatis beralih ke chain yang lebih valid ini untuk menjaga integritas blockchain. Proses ini mencegah double spending dan mempertahankan konsistensi data.


