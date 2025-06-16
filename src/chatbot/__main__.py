#!/usr/bin/env python3
"""
Simple AI Chatbot - Aplikasi Chatbot dengan Google Gemini API
"""

import os
import sys
import argparse
from colorama import init as colorama_init

# Inisialisasi colorama
colorama_init(autoreset=True)

def main():
    """Fungsi utama untuk menjalankan chatbot."""
    try:
        from .core import Chatbot
        from .config import Messages, Theme, Icons
        
        # Setup argument parser
        parser = argparse.ArgumentParser(description='Simple AI Chatbot dengan Google Gemini API')
        parser.add_argument('--model', type=str, help='Nama model yang akan digunakan')
        args = parser.parse_args()
        
        # Inisialisasi dan jalankan chatbot
        chatbot = Chatbot(model=args.model)
        chatbot.chat_loop()
        
    except KeyboardInterrupt:
        print(f"\n{Theme.WARNING}Program dihentikan oleh pengguna.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Theme.ERROR}Terjadi kesalahan: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
