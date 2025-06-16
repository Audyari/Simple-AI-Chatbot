from __future__ import annotations
import os
import sys
import time
import json
import threading
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
from datetime import datetime

import google.generativeai as genai
from colorama import Fore, Style, init as init_colorama

from .config import Config, Theme, Messages, Icons
from .storage import ChatHistory

class Chatbot:
    def __init__(self, model: Optional[str] = None):
        """Inisialisasi chatbot dengan model yang ditentukan."""
        init_colorama()
        self.model_name = model or Config.DEFAULT_MODEL
        self.model = None
        self.chat = None
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": Config.BOT_NAME}
        ]
        self.storage = ChatHistory()
        self._init_model()
    
    def _init_model(self) -> None:
        """Inisialisasi model Gemini."""
        try:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(self.model_name)
            self.chat = self.model.start_chat(history=[])
            print(f"{Theme.SUCCESS}{Icons.SUCCESS} Model {self.model_name} berhasil diinisialisasi{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Theme.ERROR}{Icons.ERROR} Gagal menginisialisasi model: {e}{Style.RESET_ALL}")
            sys.exit(1)
    
    def get_response(self, message: str) -> str:
        """Mendapatkan respons dari model untuk pesan yang diberikan."""
        if not self.chat:
            return f"{Theme.ERROR}Error: Model tidak terinisialisasi dengan benar.{Style.RESET_ALL}"
        
        try:
            # Tampilkan indikator loading
            loading = threading.Thread(target=self._show_loading, args=("Memproses...",))
            loading.daemon = True
            self.loading = True
            loading.start()
            
            # Dapatkan respons dari model
            response = self.chat.send_message(message)
            
            # Hentikan loading
            self.loading = False
            loading.join(timeout=0.1)
            
            return response.text
            
        except Exception as e:
            self.loading = False
            return f"{Theme.ERROR}Error: Gagal mendapatkan respons dari model: {e}{Style.RESET_ALL}"
    
    def _show_loading(self, message: str = "Memproses...") -> None:
        """Menampilkan indikator loading."""
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        i = 0
        while getattr(self, 'loading', False):
            sys.stdout.write(f"\r{Theme.INFO}{chars[i % len(chars)]} {message}{Style.RESET_ALL}")
            sys.stdout.flush()
            i += 1
            time.sleep(0.1)
        # Hapus baris loading
        sys.stdout.write("\r" + " " * (len(message) + 2) + "\r")
        sys.stdout.flush()
    
    def save_chat_session(self, session_name: Optional[str] = None) -> str:
        """Menyimpan sesi chat saat ini ke file."""
        if not self.messages:
            raise ValueError("Tidak ada pesan untuk disimpan")
        
        try:
            filepath = self.storage.save_chat(self.messages, session_name)
            return filepath
        except Exception as e:
            raise RuntimeError(f"Gagal menyimpan sesi chat: {e}")
    
    def load_chat_session(self, filepath: str) -> str:
        """Memuat sesi chat dari file."""
        try:
            data = self.storage.load_chat(filepath)
            self.messages = data.get('messages', [])
            return f"Sesi chat dimuat: {data.get('session_name', 'Tanpa Judul')}"
        except Exception as e:
            raise RuntimeError(f"Gagal memuat sesi chat: {e}")
    
    def search_chat_history(self, query: str) -> List[Dict[str, Any]]:
        """Mencari pesan dalam riwayat chat yang disimpan."""
        return self.storage.search_messages(query)
    
    def export_chat(self, format_type: str = 'pdf', session_name: Optional[str] = None) -> str:
        """Mengekspor chat ke format PDF.
        
        Args:
            format_type: Format ekspor (hanya 'pdf' yang didukung)
            session_name: Nama sesi (opsional)
            
        Returns:
            str: Path ke file yang diekspor
            
        Raises:
            ValueError: Jika tidak ada pesan untuk diekspor
            RuntimeError: Jika gagal mengekspor chat
        """
        if not self.messages:
            raise ValueError("Tidak ada pesan untuk diekspor")
        
        format_type = format_type.lower()
        if format_type != 'pdf':
            raise ValueError("Hanya format 'pdf' yang didukung untuk ekspor")
        
        try:
            return self.storage.export_to_pdf(self.messages, session_name)
        except Exception as e:
            raise RuntimeError(f"Gagal mengekspor chat: {e}")
    
    def list_saved_sessions(self) -> List[Dict[str, str]]:
        """Mendapatkan daftar sesi yang tersimpan."""
        sessions = []
        for filepath in self.storage.storage_dir.glob('*.json'):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    sessions.append({
                        'name': data.get('session_name', 'Tanpa Judul'),
                        'filepath': str(filepath),
                        'created_at': data.get('created_at', 'Tidak Diketahui'),
                        'message_count': len(data.get('messages', []))
                    })
            except (json.JSONDecodeError, KeyError):
                continue
        return sessions

def main():
    """Fungsi utama untuk menjalankan chatbot."""
    # Validasi konfigurasi
    try:
        Config.validate_config()
    except ValueError as e:
        print(f"{Theme.ERROR}{Icons.ERROR} {e}{Style.RESET_ALL}")
        sys.exit(1)
    
    # Tampilkan pesan selamat datang
    print(f"\n{Theme.PRIMARY}{Theme.BOLD}=== {Config.BOT_NAME} ==={Style.RESET_ALL}")
    print(Messages.WELCOME)
    
    # Inisialisasi chatbot
    bot = Chatbot()
    
    while True:
        try:
            user_input = input(f"{Theme.PRIMARY}{Icons.USER} {Config.USER_NAME}: {Style.RESET_ALL}").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == 'keluar':
                # Tawarkan untuk menyimpan sebelum keluar
                if len(bot.messages) > 1:  # Lebih dari sekedar pesan sistem
                    save = input(f"{Theme.WARNING}{Icons.WARNING} Simpan chat sebelum keluar? (y/n): {Style.RESET_ALL}").strip().lower()
                    if save in ('y', 'ya'):
                        session_name = input(f"{Theme.INFO}Nama sesi (kosongkan untuk nama default): {Style.RESET_ALL}")
                        try:
                            filepath = bot.save_chat_session(session_name or None)
                            print(f"{Theme.SUCCESS}{Icons.SUCCESS} Chat disimpan di: {filepath}{Style.RESET_ALL}")
                        except Exception as e:
                            print(f"{Theme.ERROR}{Icons.ERROR} Gagal menyimpan chat: {e}{Style.RESET_ALL}")
                print(f"\n{Theme.INFO}{Icons.INFO} Sampai jumpa!{Style.RESET_ALL}")
                break
                
            if user_input.lower() == 'bantuan':
                print(Messages.HELP)
                continue
                
            if user_input.lower() == 'simpan':
                session_name = input(f"{Theme.INFO}Nama sesi (kosongkan untuk nama default): {Style.RESET_ALL}")
                try:
                    filepath = bot.save_chat_session(session_name or None)
                    print(f"{Theme.SUCCESS}{Icons.SUCCESS} Chat disimpan di: {filepath}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Theme.ERROR}{Icons.ERROR} Gagal menyimpan chat: {e}{Style.RESET_ALL}")
                continue
                
            if user_input.lower() == 'daftar':
                sessions = bot.list_saved_sessions()
                if not sessions:
                    print(f"{Theme.WARNING}{Icons.INFO} Tidak ada sesi yang tersimpan.{Style.RESET_ALL}")
                else:
                    print(f"\n{Theme.PRIMARY}{Theme.BOLD}=== Daftar Sesi Tersimpan ==={Style.RESET_ALL}")
                    for i, session in enumerate(sessions, 1):
                        print(f"{Theme.PRIMARY}{i}. {session.get('name', 'Tanpa Judul')}{Style.RESET_ALL}")
                        print(f"   {Theme.TEXT_SECONDARY}Dibuat: {session.get('created_at', 'Tidak Diketahui')}")
                        print(f"   {Theme.TEXT_SECONDARY}Jumlah pesan: {session.get('message_count', 0)}")
                        print(f"   {Theme.TEXT_SECONDARY}Lokasi: {session.get('filepath', 'tidak_terdeteksi.json')}\n{Style.RESET_ALL}")
                continue
                
            if user_input.lower().startswith('muat '):
                try:
                    session_num = int(user_input.split()[1])
                    sessions = bot.list_saved_sessions()
                    if 1 <= session_num <= len(sessions):
                        filepath = sessions[session_num-1].get('filepath')
                        if filepath:
                            try:
                                result = bot.load_chat_session(filepath)
                                print(f"{Theme.SUCCESS}{Icons.SUCCESS} {result}{Style.RESET_ALL}")
                            except Exception as e:
                                print(f"{Theme.ERROR}{Icons.ERROR} Gagal memuat sesi: {e}{Style.RESET_ALL}")
                    else:
                        print(f"{Theme.ERROR}{Icons.ERROR} Nomor sesi tidak valid.{Style.RESET_ALL}")
                except (ValueError, IndexError):
                    print(f"{Theme.ERROR}{Icons.ERROR} Format perintah tidak valid. Gunakan: muat <nomor>{Style.RESET_ALL}")
                continue
                
            if user_input.lower().startswith('export '):
                export_cmd = user_input.split()
                if len(export_cmd) == 2 and export_cmd[1].lower() in ['txt', 'pdf']:
                    try:
                        filepath = bot.export_chat(export_cmd[1])
                        print(f"{Theme.SUCCESS}{Icons.SUCCESS} Chat berhasil diekspor ke: {filepath}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Theme.ERROR}{Icons.ERROR} Gagal mengekspor chat: {e}{Style.RESET_ALL}")
                else:
                    print(f"{Theme.WARNING}{Icons.INFO} Format ekspor tidak valid. Gunakan 'export txt' atau 'export pdf'{Style.RESET_ALL}")
                continue
                
            if user_input.lower().startswith('cari '):
                search_query = user_input[5:].strip()
                if not search_query:
                    print(f"{Theme.WARNING}{Icons.INFO} Masukkan kata kunci pencarian.{Style.RESET_ALL}")
                    continue
                    
                try:
                    results = bot.search_chat_history(search_query)
                    if not results:
                        print(f"{Theme.WARNING}{Icons.INFO} Tidak ditemukan hasil untuk '{search_query}'.{Style.RESET_ALL}")
                    else:
                        print(f"\n{Theme.PRIMARY}{Theme.BOLD}=== Hasil Pencarian: '{search_query}' ==={Style.RESET_ALL}")
                        for i, result in enumerate(results, 1):
                            role = Config.USER_NAME if result.get('role') == 'user' else Config.BOT_NAME
                            print(f"\n{Theme.SECONDARY}{i}. [{role}]{Style.RESET_ALL}")
                            print(f"   {result.get('content', '')}")
                except Exception as e:
                    print(f"{Theme.ERROR}{Icons.ERROR} Gagal melakukan pencarian: {e}{Style.RESET_ALL}")
                continue
                
            # Jika bukan perintah khusus, proses sebagai pesan chat
            if user_input:
                # Tambahkan pesan pengguna ke riwayat
                bot.messages.append({"role": "user", "content": user_input})
                
                # Dapatkan respons dari model
                response = bot.get_response(user_input)
                
                # Tampilkan respons
                print(f"\n{Theme.SECONDARY}{Icons.BOT} {Config.BOT_NAME}: {response}{Style.RESET_ALL}")
                
                # Tambahkan respons asisten ke riwayat
                bot.messages.append({"role": "assistant", "content": response})
                
        except KeyboardInterrupt:
            print(f"\n{Theme.WARNING}{Icons.WARNING} Gunakan 'keluar' untuk keluar dengan benar.{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Theme.ERROR}{Icons.ERROR} Terjadi kesalahan: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
