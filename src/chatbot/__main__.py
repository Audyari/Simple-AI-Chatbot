#!/usr/bin/env python3
"""
Modul utama untuk menjalankan chatbot dari command line.
"""
import sys
from colorama import Fore, Style, init as init_colorama

from .core import Chatbot, main as core_main

def main():
    """Fungsi utama untuk menjalankan chatbot."""
    init_colorama()  # Inisialisasi colorama
    
    try:
        # Jalankan fungsi main dari core.py
        core_main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operasi dibatalkan oleh pengguna.{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}Terjadi kesalahan: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
