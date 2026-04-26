# 📘 Panduan Belajar Tim Skintify

Halo **Syaqila, Najla, dan Falisha!** Selamat datang di proyek kolaborasi Skintify. Di sini kalian akan belajar membangun aplikasi desktop menggunakan Python dan NiceGUI.

## 🛠 Konsep Utama yang Harus Dipahami:

### 1. State Management (`app/context.py`)
Bayangkan `state` adalah sebuah buku catatan besar yang bisa dibaca oleh semua halaman. 
- Jika kalian ingin tahu daftar skincare user, gunakan: `state.routine`
- Jika ingin menambah skincare: `state.routine.append(produk)`

### 2. Akses Data (`data_mgr`)
Objek ini adalah "asisten" yang bertugas mengambil data dari database atau file JSON.
- Contoh: `data_mgr.get_paginated_products()` mengambil daftar produk.
- Contoh: `data_mgr.analyze_routine()` menganalisis kesehatan kulit.

### 3. Komponen NiceGUI
- `ui.label()` -> Membuat teks.
- `ui.button()` -> Membuat tombol.
- `ui.row()` -> Membuat elemen berjejer ke samping.
- `ui.column()` -> Membuat elemen berjejer ke bawah.
- `with ui.card()` -> Membuat panel/kotak pembungkus.

## 🚀 Alur Kerja Kalian:
1. Buka file di folder nama kalian (misal: `app/ui/pages/najla/compare_page.py`).
2. Masukkan kode kalian di bawah komentar `# --- MULAI KERJAKAN DI SINI ---`.
3. Lihat contoh kode di file `CONTOH_KODE.py` jika bingung.
4. Simpan file, dan lihat perubahannya di aplikasi!

**Selamat Belajar & Semangat!** 🚀
