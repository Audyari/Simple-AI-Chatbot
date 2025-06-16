import os
import time
import threading
import json
from typing import List, Dict, Optional, Union
from pathlib import Path
from colorama import Fore, Style, init

from .config import Config, Theme, Messages, Icons
from .storage import ChatHistory

# Inisialisasi colorama
init(autoreset=True)

class Chatbot:
    """Kelas utama untuk menangani logika chatbot."""
    
    def __init__(self, model: str = None):
        self.model_name = model or Config.DEFAULT_MODEL
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": "Anda adalah asisten AI yang ramah dan membantu."}
        ]
        self.chat = None
        self.history = ChatHistory()
        self.setup_gemini()
        self.loading = False
        self.loading_thread = None
    
    def setup_gemini(self):
        """Setup Google Gemini API."""
        import google.generativeai as genai
        
        # Validasi konfigurasi
        Config.validate_config()
        
        # Konfigurasi API
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(self.model_name)
        self.chat = self.model.start_chat(history=[])
        print(f"{Theme.INFO}Menggunakan model: {self.model_name}{Style.RESET_ALL}")
    
    def show_loading(self, message="Memproses..."):
        """Menampilkan indikator loading dengan animasi."""
        self.loading = True
        
        def animate():
            chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
            i = 0
            while self.loading:
                print(f"\r{Theme.INFO}{chars[i % len(chars)]} {message}", end="")
                i += 1
                time.sleep(0.1)
            # Hapus baris loading
            print("\r" + " " * (len(message) + 2) + "\r", end="")
        
        self.loading_thread = threading.Thread(target=animate)
        self.loading_thread.daemon = True
        self.loading_thread.start()
    
    def stop_loading(self):
        """Menghentikan indikator loading."""
        self.loading = False
        if self.loading_thread:
            self.loading_thread.join()
            self.loading_thread = None
    
    def print_header(self, title: str, icon: str = ""):
        """Mencetak header dengan gaya yang konsisten."""
        header = f"{Theme.PRIMARY}{Theme.BOLD}=== {icon} {title} ==={Style.RESET_ALL}"
        print(f"\n{header}")
    
    def print_success(self, message: str):
        """Mencetak pesan sukses."""
        print(f"{Icons.SUCCESS} {Theme.SUCCESS}{message}{Style.RESET_ALL}")
    
    def print_error(self, message: str):
        """Mencetak pesan error."""
        print(f"{Icons.ERROR} {Theme.ERROR}{message}{Style.RESET_ALL}")
    
    def print_warning(self, message: str):
        """Mencetak pesan peringatan."""
        print(f"{Icons.WARNING} {Theme.WARNING}{message}{Style.RESET_ALL}")
    
    def print_info(self, message: str):
        """Mencetak pesan informasi."""
        print(f"{Icons.INFO} {Theme.INFO}{message}{Style.RESET_ALL}")
    
    def confirm_action(self, message: str) -> bool:
        """Meminta konfirmasi pengguna."""
        response = input(f"{Theme.WARNING}{message} (y/n): ").strip().lower()
        return response in ['y', 'ya', 'yes']
    
    def get_response(self, user_input: str) -> str:
        """Mendapatkan respons dari model AI."""
        try:
            self.show_loading()
            response = self.chat.send_message(user_input)
            self.stop_loading()
            return response.text
        except Exception as e:
            self.print_error(f"Error saat memproses permintaan: {str(e)}")
            return "Maaf, terjadi kesalahan saat memproses permintaan Anda."
    
    def save_chat_session(self, session_name: str = None) -> str:
        """
        Menyimpan sesi chat saat ini.
        
        Args:
            session_name: Nama sesi (opsional)
            
        Returns:
            Path ke file yang disimpan
        """
        if not self.messages:
            self.print_warning("Tidak ada pesan untuk disimpan.")
            return ""
            
        try:
            filepath = self.history.save_chat(self.messages, session_name)
            self.print_success(f"Chat disimpan di: {filepath}")
            return filepath
        except Exception as e:
            self.print_error(f"Gagal menyimpan chat: {str(e)}")
            return ""
    
    def load_chat_session(self, filepath: str) -> bool:
        """
        Memuat sesi chat dari file.
        
        Args:
            filepath: Path ke file yang akan dimuat
            
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            data = self.history.load_chat(filepath)
            self.messages = data.get('messages', [])
            
            # Reset chat dengan model baru
            self.chat = self.model.start_chat(history=[])
            for msg in self.messages[1:]:  # Lewati pesan sistem
                self.chat.send_message(msg["content"])
            return True
        except Exception as e:
            self.print_error(f"Gagal memuat chat: {str(e)}")
            return False
    
    def list_saved_sessions(self) -> List[Dict]:
        """Mendapatkan daftar sesi yang tersimpan."""
        return self.history.list_sessions()
    
    def export_chat(self, format_type: str = 'txt') -> str:
        """
        Mengekspor chat saat ini ke format yang ditentukan.
        
        Args:
            format_type: Format ekspor (txt atau pdf)
            
        Returns:
            Path ke file yang diekspor
        """
        if not self.messages:
            self.print_warning("Tidak ada pesan untuk diekspor.")
            return ""
            
        try:
            session_name = next((msg['content'] for msg in self.messages if msg['role'] == 'system'), None)
            
            if format_type.lower() == 'txt':
                filepath = self.history.export_to_txt(self.messages, session_name)
                self.print_success(f"Chat berhasil diekspor ke TXT: {filepath}")
            elif format_type.lower() == 'pdf':
                filepath = self.history.export_to_pdf(self.messages, session_name)
                self.print_success(f"Chat berhasil diekspor ke PDF: {filepath}")
            else:
                self.print_error("Format tidak didukung. Gunakan 'txt' atau 'pdf'.")
                return ""
                
            return filepath
        except Exception as e:
            self.print_error(f"Gagal mengekspor chat: {str(e)}")
            return ""
    
    def search_chat_history(self, query: str, session_file: str = None, case_sensitive: bool = False) -> List[Dict]:
        """
        Mencari pesan dalam riwayat chat.
        
        Args:
            query: Kata kunci pencarian
            session_file: Nama file sesi (opsional)
            case_sensitive: Pencarian case-sensitive
            
        Returns:
            List hasil pencarian
        """
        if not query:
            self.print_warning("Masukkan kata kunci pencarian.")
            return []
            
        try:
            results = self.history.search_messages(
                query=query,
                session_file=session_file,
                case_sensitive=case_sensitive
            )
            return results
            
        except Exception as e:
            self.print_error(f"Gagal melakukan pencarian: {str(e)}")
            return []
    
    def chat_loop(self):
        """Loop chat interaktif."""
        self.print_header("Selamat datang di AI Assistant", Icons.BOT)
        self.print_info(Messages.WELCOME)
        
        while True:
            try:
                # Tampilkan prompt input
                user_input = input(f"\n{Theme.PRIMARY}{Icons.USER} Anda: {Style.RESET_ALL}").strip()
                
                # Perintah khusus
                if not user_input:
                    continue
                    
                if user_input.lower() in ['keluar', 'quit', 'exit']:
                    if self.confirm_action("Apakah Anda yakin ingin keluar?"):
                        if self.messages and len(self.messages) > 1:  # Lebih dari sekedar pesan sistem
                            if self.confirm_action("Simpan chat sebelum keluar?"):
                                self.save_chat_session()
                        self.print_success("Terima kasih! Sampai jumpa!")
                        break
                    continue
                
                elif user_input.lower() == 'bantuan':
                    self.print_info(Messages.HELP)
                    continue
                
                elif user_input.lower() == 'simpan':
                    session_name = input(f"{Theme.INFO}Nama sesi (kosongkan untuk default): {Style.RESET_ALL}")
                    self.save_chat_session(session_name or None)
                    continue
                    
                elif user_input.lower() == 'daftar':
                    sessions = self.list_saved_sessions()
                    if not sessions:
                        self.print_warning("Tidak ada sesi yang tersimpan.")
                    else:
                        self.print_header("Daftar Sesi Tersimpan")
                        for i, session in enumerate(sessions, 1):
                            print(f"{i}. {session.get('session_name', 'Sesi Tanpa Nama')}")
                            print(f"   Dibuat: {session.get('created_at', 'Tidak Diketahui')}")
                            print(f"   Jumlah pesan: {session.get('message_count', 0)}")
                            print(f"   Lokasi: {session.get('filename', 'tidak_terdeteksi.json')}\n")
                            
                        load = input("Muat sesi? (nomor/enter untuk batal): ").strip()
                        if load.isdigit() and 1 <= int(load) <= len(sessions):
                            if self.load_chat_session(sessions[int(load)-1].get('filepath')):
                                self.print_success("Berhasil memuat sesi.")
                
                elif user_input.lower().startswith('export '):
                    export_cmd = user_input.split()
                    if len(export_cmd) == 2 and export_cmd[1].lower() in ['txt', 'pdf']:
                        self.export_chat(export_cmd[1])
                    else:
                        self.print_error("Format ekspor tidak valid. Gunakan 'export txt' atau 'export pdf'")
                
                elif user_input.lower().startswith('cari '):
                    # Parse perintah pencarian
                    parts = user_input[5:].strip().split()
                    if len(parts) >= 2 and parts[0].lower() == 'di':
                        # Format: cari di <file> <kata kunci>
                        if len(parts) < 3:
                            self.print_error("Format pencarian tidak valid. Gunakan: cari di <file> <kata kunci>")
                            continue
                        session_file = parts[1]
                        search_query = ' '.join(parts[2:])
                        results = self.search_chat_history(search_query, session_file)
                    else:
                        # Format: cari <kata kunci>
                        search_query = ' '.join(parts)
                        results = self.search_chat_history(search_query)
                    
                    # Tampilkan hasil pencarian
                    if not results:
                        self.print_warning(f"Tidak ditemukan hasil untuk '{search_query}'.")
                    else:
                        self.print_header(f"Hasil Pencarian: '{search_query}' ({len(results)} ditemukan)")
                        for i, result in enumerate(results, 1):
                            role = "Anda" if result.get('role') == 'user' else "Asisten"
                            session_name = result.get('session', 'Sesi Tanpa Nama')
                            self.print_info(f"\n{i}. [{session_name} - {role}]")
                            self.print_info(f"   {result.get('snippet', 'Tidak ada konten')}")
                            self.print_info(f"   File: {result.get('session_file', 'tidak_terdeteksi.json')}")
                
                # Jika bukan perintah khusus, proses sebagai pesan chat
                else:
                    # Lewati input kosong
                    if not user_input.strip():
                        continue
                        
                    # Tambahkan pesan pengguna ke riwayat
                    self.messages.append({"role": "user", "content": user_input})
                    
                    # Dapatkan dan tampilkan respons
                    self.print_info("Memproses...")
                    response = self.get_response(user_input)
                    self.print_info(f"Asisten: {response}")
                    
                    # Tambahkan respons ke riwayat
                    self.messages.append({"role": "assistant", "content": response})
                    
            except KeyboardInterrupt:
                self.print_warning("Interupsi pengguna. Gunakan 'keluar' untuk keluar dengan benar.")
            except Exception as e:
                self.print_error(f"Terjadi kesalahan: {str(e)}")
                continue
