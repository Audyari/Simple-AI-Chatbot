import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Union
from pathlib import Path
from fpdf import FPDF  # Untuk ekspor PDF

class ChatHistory:
    """Kelas untuk menangani penyimpanan dan ekspor riwayat chat."""
    
    def __init__(self, storage_dir: str = "chat_history"):
        """
        Inisialisasi penyimpanan riwayat chat.
        
        Args:
            storage_dir: Direktori untuk menyimpan file riwayat
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
    
    def _get_filename(self, extension: str = "json") -> str:
        """Membuat nama file berdasarkan timestamp saat ini."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"chat_{timestamp}.{extension}"
    
    def save_chat(self, messages: List[Dict[str, str]], session_name: str = None) -> str:
        """
        Menyimpan riwayat chat ke file JSON.
        
        Args:
            messages: Daftar pesan dalam format [{"role": "user", "content": "..."}, ...]
            session_name: Nama sesi (opsional)
            
        Returns:
            Path ke file yang disimpan
        """
        if not messages:
            raise ValueError("Tidak ada pesan untuk disimpan")
            
        data = {
            "session_name": session_name or "Unnamed Session",
            "created_at": datetime.now().isoformat(),
            "messages": messages
        }
        
        filename = self._get_filename("json")
        filepath = self.storage_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        return str(filepath)
    
    def export_to_txt(self, messages: List[Dict[str, str]], session_name: str = None) -> str:
        """
        Ekspor chat ke file teks.
        
        Args:
            messages: Daftar pesan
            session_name: Nama sesi
            
        Returns:
            Path ke file TXT yang dihasilkan
        """
        if not messages:
            raise ValueError("Tidak ada pesan untuk diekspor")
            
        filename = self._get_filename("txt")
        filepath = self.storage_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"=== {session_name or 'Chat Export'} ===\n")
            f.write(f"Dibuat pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 40 + "\n\n")
            
            for msg in messages:
                role = "Anda" if msg["role"] == "user" else "Asisten"
                f.write(f"{role}: {msg['content']}\n\n")
                
        return str(filepath)
    
    def export_to_pdf(self, messages: List[Dict[str, str]], session_name: str = None) -> str:
        """
        Ekspor chat ke file PDF.
        
        Args:
            messages: Daftar pesan
            session_name: Nama sesi
            
        Returns:
            Path ke file PDF yang dihasilkan
        """
        if not messages:
            raise ValueError("Tidak ada pesan untuk diekspor")
            
        filename = self._get_filename("pdf")
        filepath = self.storage_dir / filename
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Set font
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, session_name or "Chat Export", 0, 1, 'C')
        
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 8, f"Dibuat pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'C')
        pdf.ln(10)
        
        # Atur style untuk pesan
        pdf.set_font("Arial", 'B', 12)
        
        for msg in messages:
            role = "Anda" if msg["role"] == "user" else "Asisten"
            
            # Header pesan
            pdf.set_fill_color(240, 240, 240)
            pdf.cell(0, 8, f"{role}:", 0, 1, 'L', 1)
            
            # Isi pesan
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 7, msg["content"])
            pdf.ln(3)
        
        pdf.output(str(filepath))
        return str(filepath)
    
    def load_chat(self, filepath: str) -> Dict:
        """Memuat riwayat chat dari file."""
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"File tidak ditemukan: {filepath}")
            
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_sessions(self, file_type: str = "json") -> List[Dict]:
        """
        Mendapatkan daftar semua sesi chat yang tersimpan.
        
        Args:
            file_type: Jenis file yang akan dicari (json/txt/pdf)
            
        Returns:
            Daftar dictionary berisi info sesi
        """
        sessions = []
        for file in self.storage_dir.glob(f"*.{file_type}"):
            try:
                file_stat = file.stat()
                sessions.append({
                    "filepath": str(file),
                    "filename": file.name,
                    "created_at": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                    "size_kb": file_stat.st_size / 1024,
                    "type": file_type.upper()
                })
            except Exception as e:
                print(f"Error processing {file}: {e}")
                continue
                
        # Urutkan berdasarkan waktu pembuatan (terbaru dulu)
        sessions.sort(key=lambda x: x["created_at"], reverse=True)
        return sessions
