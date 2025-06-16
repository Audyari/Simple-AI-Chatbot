import os
import google.generativeai as genai
from typing import List, Dict, Optional
from colorama import Fore, Style, init
from .config import Config
from .storage import ChatHistory

# Inisialisasi colorama
init(autoreset=True)

class Chatbot:
    def __init__(self, model: str = None):
        """Inisialisasi chatbot dengan model Gemini."""
        self.model_name = model or Config.DEFAULT_MODEL
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": "Anda adalah asisten AI yang ramah dan membantu."}
        ]
        self.chat = None
        self.history = ChatHistory()
        self.setup_gemini()
    
    def setup_gemini(self):
        """Setup Google Gemini API."""
        if not Config.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY tidak ditemukan di file .env\n"
                "Silakan dapatkan API key dari https://aistudio.google.com/app/apikey"
            )
            
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(self.model_name)
        self.chat = self.model.start_chat(history=[])
        print(f"{Fore.GREEN}Menggunakan model: {self.model_name}{Style.RESET_ALL}")
    
    def get_response(self, user_input: str) -> str:
        """Mendapatkan respons dari model AI."""
        try:
            response = self.chat.send_message(user_input)
            return response.text
        except Exception as e:
            error_msg = f"Error saat memproses permintaan: {str(e)}"
            print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")
            return "Maaf, terjadi kesalahan saat memproses permintaan Anda."
    
    def save_chat_session(self, session_name: str = None) -> str:
        """
        Menyimpan sesi chat saat ini.
        
        Args:
            session_name: Nama untuk sesi ini (opsional)
            
        Returns:
            Path ke file yang disimpan
        """
        if not self.messages:
            print(f"{Fore.YELLOW}Tidak ada pesan untuk disimpan{Style.RESET_ALL}")
            return ""
            
        try:
            filepath = self.history.save_chat(self.messages, session_name)
            print(f"{Fore.GREEN}Chat disimpan di: {filepath}{Style.RESET_ALL}")
            return filepath
        except Exception as e:
            print(f"{Fore.RED}Gagal menyimpan chat: {str(e)}{Style.RESET_ALL}")
            return ""
    
    def list_saved_sessions(self) -> List[Dict]:
        """Mendapatkan daftar sesi yang tersimpan."""
        return self.history.list_sessions()
    
    def load_chat_session(self, filepath: str) -> bool:
        """
        Memuat sesi chat yang tersimpan.
        
        Args:
            filepath: Path ke file sesi yang akan dimuat
            
        Returns:
            bool: True jika berhasil, False jika gagal
        """
        try:
            data = self.history.load_chat(filepath)
            self.messages = data.get("messages", [])
            # Perbarui chat Gemini dengan riwayat yang dimuat
            self.chat = self.model.start_chat(history=[])
            for msg in self.messages:
                if msg["role"] == "user":
                    self.chat.send_message(msg["content"])
            return True
        except Exception as e:
            print(f"{Fore.RED}Gagal memuat chat: {str(e)}{Style.RESET_ALL}")
            return False
    
    def chat_loop(self):
        """Loop chat interaktif."""
        print(f"\n{Fore.CYAN}=== Selamat datang di AI Assistant ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Ketik 'keluar' atau 'quit' untuk mengakhiri.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Ketik 'simpan' untuk menyimpan chat.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Ketik 'daftar' untuk melihat sesi yang tersimpan.{Style.RESET_ALL}")
        
        while True:
            try:
                # Input pengguna
                user_input = input(f"\n{Fore.BLUE}Anda: {Style.RESET_ALL}")
                
                # Perintah khusus
                if user_input.lower() in ['keluar', 'quit', 'exit']:
                    save = input("Simpan chat sebelum keluar? (y/n): ").lower()
                    if save == 'y':
                        session_name = input("Nama sesi (kosongkan untuk default): ")
                        self.save_chat_session(session_name or None)
                    print(f"\n{Fore.CYAN}Terima kasih! Sampai jumpa!{Style.RESET_ALL}")
                    break
                    
                elif user_input.lower() == 'simpan':
                    session_name = input("Nama sesi (kosongkan untuk default): ")
                    self.save_chat_session(session_name or None)
                    continue
                    
                elif user_input.lower() == 'daftar':
                    sessions = self.list_saved_sessions()
                    if not sessions:
                        print(f"{Fore.YELLOW}Tidak ada sesi yang tersimpan.{Style.RESET_ALL}")
                    else:
                        print(f"\n{Fore.CYAN}=== Daftar Sesi Tersimpan ==={Style.RESET_ALL}")
                        for i, session in enumerate(sessions, 1):
                            print(f"{i}. {session['session_name']}")
                            print(f"   Dibuat: {session['created_at']}")
                            print(f"   Jumlah pesan: {session['message_count']}")
                            print(f"   Lokasi: {session['filepath']}\n")
                            
                        load = input("Muat sesi? (nomor/enter untuk batal): ").strip()
                        if load.isdigit() and 1 <= int(load) <= len(sessions):
                            if self.load_chat_session(sessions[int(load)-1]['filepath']):
                                print(f"{Fore.GREEN}Berhasil memuat sesi.{Style.RESET_ALL}")
                    continue
                
                # Lewati input kosong
                if not user_input.strip():
                    continue
                
                # Tambahkan pesan user ke riwayat
                self.messages.append({"role": "user", "content": user_input})
                
                # Dapatkan dan tampilkan respons
                print(f"{Fore.YELLOW}Memproses...{Style.RESET_ALL}")
                response = self.get_response(user_input)
                print(f"\n{Fore.GREEN}Asisten: {Style.RESET_ALL}{response}")
                
                # Tambahkan respons ke riwayat
                self.messages.append({"role": "assistant", "content": response})
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.RED}Interupsi pengguna. Keluar...{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                continue
