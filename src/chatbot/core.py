import os
import google.generativeai as genai
from typing import List, Dict
from colorama import Fore, Style, init
from .config import Config

# Inisialisasi colorama
init(autoreset=True)

class Chatbot:
    def __init__(self, model: str = "gemini-pro"):
        """Inisialisasi chatbot dengan model Gemini."""
        self.model_name = model
        self.chat = None
        self.setup_gemini()
    
    def setup_gemini(self):
        """Setup Google Gemini API."""
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY tidak ditemukan di file .env")
            
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(self.model_name)
        self.chat = self.model.start_chat(history=[])
        print(f"{Fore.GREEN}Menggunakan Google Gemini: {self.model_name}{Style.RESET_ALL}")
    
    def get_response(self, user_input: str) -> str:
        """Mendapatkan respons dari Gemini."""
        try:
            response = self.chat.send_message(user_input)
            return response.text
        except Exception as e:
            error_msg = f"Error saat memproses permintaan: {str(e)}"
            print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")
            return "Maaf, terjadi kesalahan saat memproses permintaan Anda."
    
    def chat_loop(self):
        """Loop chat interaktif."""
        print(f"\n{Fore.CYAN}=== Selamat datang di AI Assistant (Gemini) ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Ketik 'keluar' atau 'quit' untuk mengakhiri.{Style.RESET_ALL}")
        
        while True:
            try:
                # Input pengguna
                user_input = input(f"\n{Fore.BLUE}Anda: {Style.RESET_ALL}")
                
                # Cek perintah keluar
                if user_input.lower() in ['keluar', 'quit', 'exit']:
                    print(f"\n{Fore.CYAN}Terima kasih! Sampai jumpa!{Style.RESET_ALL}")
                    break
                
                # Lewati input kosong
                if not user_input.strip():
                    continue
                
                # Dapatkan dan tampilkan respons
                print(f"{Fore.YELLOW}Memproses...{Style.RESET_ALL}")
                response = self.get_response(user_input)
                print(f"\n{Fore.GREEN}Asisten: {Style.RESET_ALL}{response}")
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.RED}Interupsi pengguna. Keluar...{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                continue
