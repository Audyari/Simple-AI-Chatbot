# Simple AI Chatbot

Sebuah chatbot sederhana yang menggunakan Google Gemini API dengan kemampuan menyimpan, memuat, mengekspor, dan mencari dalam riwayat percakapan.

## 🌟 Fitur

- [x] **Dukungan Google Gemini API**
  - Menggunakan model `gemini-1.5-flash`
  - Konfigurasi mudah melalui file `.env`

- [x] **Manajemen Riwayat Chat**
  - Menyimpan percakapan ke file JSON
  - Memuat percakapan yang tersimpan
  - Memberi nama sesi percakapan
  - Melihat daftar sesi yang tersimpan

- [x] **Pencarian Canggih**
  - Cari pesan dalam seluruh riwayat
  - Cari dalam sesi tertentu
  - Tampilkan konteks pesan
  - Sorot kata kunci yang ditemukan

- [x] **Ekspor Chat**
  - Ekspor ke format TXT
  - Ekspor ke format PDF
  - Format yang rapi dan mudah dibaca

## 🚀 Cara Menggunakan

### Perintah yang Tersedia
- `keluar`/`quit` - Keluar dari aplikasi
- `simpan` - Menyimpan percakapan saat ini
- `daftar` - Menampilkan daftar sesi yang tersimpan
- `export txt` - Ekspor chat ke file teks
- `export pdf` - Ekspor chat ke file PDF
- `cari <kata kunci>` - Cari dalam seluruh riwayat chat
- `cari di <nama file> <kata kunci>` - Cari dalam file tertentu

### Mencari dalam Riwayat
1. **Cari di semua sesi**:
   ```
   cari halo
   ```
   Akan mencari kata "halo" di semua file chat.

2. **Cari di sesi tertentu**:
   ```
   cari di chat_20250616_103753.json halo
   ```
   Hanya mencari di file yang ditentukan.

3. **Hasil pencarian** akan menampilkan:
   - Nama sesi
   - Peran pengirim (Anda/Asisten)
   - Potongan teks yang relevan
   - Nama file sumber

### Contoh Output Pencarian:
```
=== Hasil Pencarian: 'halo' (3 ditemukan) ===

1. [Sesi Chat 1 - Anda]
   ... ini adalah contoh pesan yang mengandung kata **halo** di dalamnya ...
   File: chat_20250616_103753.json

2. [Sesi Chat 2 - Asisten]
   ... Anda mengatakan **halo** tadi, ada yang bisa saya bantu? ...
   File: chat_20250616_110245.json
```

## 🔧 Instalasi

1. **Clone repositori**
   ```bash
   git clone https://github.com/username/simple-ai-chatbot.git
   cd simple-ai-chatbot
   ```

2. **Buat dan aktifkan virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # MacOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Buat file .env**
   ```bash
   cp .env.example .env
   ```
   Kemudian edit file `.env` dan tambahkan API key Google Gemini Anda:
   ```
   GEMINI_API_KEY=your_api_key_here
   DEFAULT_MODEL=gemini-1.5-flash
   MAX_TOKENS=1000
   TEMPERATURE=0.7
   ```

5. **Jalankan aplikasi**
   ```bash
   python src/main.py
   ```

## 📁 Struktur Proyek

```
simple-ai-chatbot/
├── .env.example         # Template konfigurasi
├── requirements.txt     # Dependensi
├── chat_history/        # Folder penyimpanan riwayat chat
└── src/
    ├── main.py          # Entry point aplikasi
    └── chatbot/
        ├── __init__.py   # Inisialisasi package
        ├── config.py    # Konfigurasi aplikasi
        ├── core.py      # Logika utama chatbot
        └── storage.py   # Manajemen penyimpanan, ekspor, & pencarian
```

## 🤝 Berkontribusi

1. Fork repositori
2. Buat branch fitur (`git checkout -b fitur/namafitur`)
3. Commit perubahan (`git commit -m 'Menambahkan fitur xyz'`)
4. Push ke branch (`git push origin fitur/namafitur`)
5. Buat Pull Request

## 📝 Lisensi

Dilisensikan di bawah [MIT License](LICENSE).

---

Dibuat dengan ❤️ menggunakan Google Gemini API