import os
from dotenv import load_dotenv
from colorama import Fore, Back, Style, init

# Inisialisasi colorama
init(autoreset=True)

# Load environment variables from .env file
load_dotenv()

# Definisi kelas Theme di luar Config
class Theme:
    # Warna Utama
    PRIMARY = Fore.CYAN
    SECONDARY = Fore.BLUE
    SUCCESS = Fore.GREEN
    WARNING = Fore.YELLOW
    ERROR = Fore.RED
    INFO = Fore.CYAN
    
    # Warna Teks
    TEXT = Fore.WHITE
    TEXT_SECONDARY = Fore.LIGHTBLACK_EX
    
    # Warna Background
    BG_PRIMARY = Back.CYAN
    BG_SECONDARY = Back.BLUE
    
    # Style
    BOLD = Style.BRIGHT
    DIM = Style.DIM
    RESET = Style.RESET_ALL

# Konfigurasi Pesan
class Messages:
    WELCOME = f"""
{Theme.PRIMARY}{Theme.BOLD}=== Selamat Datang di AI Assistant ==={Style.RESET_ALL}
Ketik {Theme.SUCCESS}/bantuan{Style.RESET_ALL} untuk melihat daftar perintah yang tersedia.
"""

    HELP = f"""
{Theme.PRIMARY}{Theme.BOLD}📖 DAFTAR PERINTAH{Style.RESET_ALL}

{Theme.BOLD}Perintah Dasar:{Style.RESET_ALL}
  {Theme.SUCCESS}keluar{Style.RESET_ALL} - Keluar dari aplikasi
  {Theme.SUCCESS}bantuan{Style.RESET_ALL} - Tampilkan pesan bantuan ini

{Theme.BOLD}Manajemen Chat:{Style.RESET_ALL}
  {Theme.SUCCESS}simpan [nama]{Style.RESET_ALL} - Simpan chat saat ini
  {Theme.SUCCESS}daftar{Style.RESET_ALL} - Tampilkan daftar sesi tersimpan
  {Theme.SUCCESS}muat <nomor>{Style.RESET_ALL} - Muat sesi tertentu

{Theme.BOLD}Pencarian:{Style.RESET_ALL}
  {Theme.SUCCESS}cari <kata kunci>{Style.RESET_ALL} - Cari di semua chat
  {Theme.SUCCESS}cari di <file> <kata kunci>{Style.RESET_ALL} - Cari di file tertentu

{Theme.BOLD}Ekspor:{Style.RESET_ALL}
  {Theme.SUCCESS}export txt{Style.RESET_ALL} - Ekspor chat ke file teks
  {Theme.SUCCESS}export pdf{Style.RESET_ALL} - Ekspor chat ke file PDF
"""

class Icons:
    USER = "👤"
    BOT = "🤖"
    LOADING = "⏳"
    SUCCESS = "✅"
    ERROR = "❌"
    WARNING = "⚠️"
    INFO = "ℹ️"

class Config:
    """Konfigurasi aplikasi."""
    
    # Konfigurasi API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-1.5-flash")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Konfigurasi Aplikasi
    BOT_NAME = "AI Assistant"
    USER_NAME = "You"
    
    # Gunakan kelas yang sudah didefinisikan di luar
    Theme = Theme
    Messages = Messages
    Icons = Icons
    
    @classmethod
    def validate_config(cls):
        """Validasi konfigurasi yang diperlukan."""
        required_vars = ["GEMINI_API_KEY"]
        missing_vars = [var for var in required_vars if not getattr(cls, var, None)]
        
        if missing_vars:
            missing_str = ", ".join(missing_vars)
            raise ValueError(f"Variabel lingkungan berikut diperlukan tetapi tidak ditemukan: {missing_str}")
        
        return True
