#!/usr/bin/env python3
"""
Simple AI Chatbot dengan Google Gemini
"""

import sys
import argparse
from chatbot import Chatbot, Config

def main():
    """Fungsi utama untuk menjalankan chatbot."""
    # Parse argumen command line
    parser = argparse.ArgumentParser(description='Simple AI Chatbot dengan Google Gemini')
    parser.add_argument('--model', type=str, default=Config.DEFAULT_MODEL,
                      help=f'Model yang akan digunakan (default: {Config.DEFAULT_MODEL})')
    args = parser.parse_args()
    
    try:
        # Validasi konfigurasi
        Config.validate_config()
        
        # Inisialisasi dan jalankan chatbot
        bot = Chatbot(model=args.model)
        bot.chat_loop()
        
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
