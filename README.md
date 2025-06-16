# Simple AI Chatbot

Sebuah chatbot berbasis AI yang menggunakan Google Gemini API dengan antarmuka baris perintah (CLI) yang interaktif.

## 🚀 Fitur

- 💬 Obrolan interaktif dengan AI
- 💾 Simpan dan muat riwayat obrolan
- 🔍 Pencarian dalam riwayat chat
- � Ekspor ke format PDF
- 🎨 Antarmuka berwarna dengan emoji
- ⚡ Indikator loading animasi

## 📋 Persyaratan

- Python 3.8+
- Kunci API Google Gemini
- Dependensi yang terdaftar di `requirements.txt`

## 🛠️ Instalasi

1. Clone repositori ini:
   ```bash
   git clone https://github.com/username/simple-ai-chatbot.git
   cd simple-ai-chatbot
   ```

2. Buat environment virtual (disarankan):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   # atau
   source venv/bin/activate  # Linux/Mac
   ```

3. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```

4. Buat file `.env` di direktori utama dan tambahkan kunci API Anda:
   ```env
   GEMINI_API_KEY=your_api_key_here
   DEFAULT_MODEL=gemini-1.5-flash
   ```

## 🚀 Penggunaan

Jalankan aplikasi:
```bash
python -m src.chatbot
```

### 🎯 Perintah yang Tersedia

| Perintah | Deskripsi |
|----------|-----------|
| `bantuan` | Tampilkan pesan bantuan |
| `simpan [nama]` | Simpan sesi chat saat ini |
| `daftar` | Tampilkan daftar sesi tersimpan |
| `muat <nomor>` | Muat sesi tertentu |
| `cari <kata kunci>` | Cari di semua chat |
| `cari di <file> <kata kunci>` | Cari di file tertentu |
| `export pdf` | Ekspor chat ke file PDF |
| `keluar` | Keluar dari aplikasi |

## 🏗️ Struktur Proyek

```
simple-ai-chatbot/
├── src/
│   └── chatbot/
│       ├── __init__.py
│       ├── __main__.py     # Entry point aplikasi
│       ├── config.py       # Konfigurasi dan tema
│       ├── core.py         # Logika utama chatbot
│       └── storage.py      # Penyimpanan dan manajemen file
├── tests/                  # File-file test
│   ├── conftest.py        # Konfigurasi pytest
│   ├── test_core.py       # Test untuk core.py
│   └── test_storage.py    # Test untuk storage.py
├── .env.example           # Contoh file konfigurasi
├── .gitignore
├── pytest.ini            # Konfigurasi pytest
├── README.md
└── requirements.txt       # Dependensi
```

## 🧪 Menjalankan Test

Untuk menjalankan test:
```bash
python -m pytest tests/ -v
```

## 🤝 Berkontribusi

1. Fork repositori ini
2. Buat branch fitur baru
3. Commit perubahan Anda
4. Push ke branch
5. Buat Pull Request

## 📜 Lisensi

Proyek ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detailnya.

---

Dibuat dengan ❤️ oleh [Audyari Wiyono] - [@username]