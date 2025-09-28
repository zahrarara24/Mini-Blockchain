# Praktikum Blockchain - Sesi 1
Mini Blockchain implementasi dengan Python

Blockchain adalah teknologi yang memungkinkan penyimpanan data dalam blok-blok yang saling terhubung. Setiap blok berisi transaksi dan dijamin keamanannya melalui proses mining. Mining dilakukan dengan mencari angka nonce yang menghasilkan hash dengan awalan nol sesuai tingkat kesulitan. Semua transaksi dalam blok dirangkum menjadi satu hash menggunakan struktur Merkle tree. Sistem validasi memastikan seluruh rantai blok tetap konsisten dan tidak dapat diubah.

## Cara Menjalankan

1. Setup Virtual Environment :
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows

2. Jalankan Program dan Testing :
python chain.py
python tests.py

