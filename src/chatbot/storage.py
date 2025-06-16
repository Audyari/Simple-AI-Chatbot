from __future__ import annotations
from pathlib import Path
import json
import re
import os
from typing import List, Dict, Any, Optional, TypedDict, Union
from datetime import datetime
from fpdf import FPDF

class SearchResult(TypedDict):
    session: str
    content: str
    role: str
    snippet: str
    filepath: str

class ChatHistory:
    def __init__(self, storage_dir: Union[str, Path] = 'chat_history'):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True, parents=True)
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize nama file untuk menghindari karakter yang tidak valid."""
        # Hapus karakter yang tidak valid dan ganti dengan underscore
        safe_name = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', filename)
        # Hapus spasi di awal dan akhir
        safe_name = safe_name.strip()
        # Ganti multiple underscores dengan satu underscore
        safe_name = re.sub(r'_{2,}', '_', safe_name)
        # Pastikan nama file tidak kosong
        if not safe_name:
            safe_name = 'chat'
        return safe_name
    
    def _get_filename(self, session_name: Optional[str] = None, extension: str = 'json') -> str:
        """Generate nama file dengan timestamp dan nama sesi."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = self._sanitize_filename(session_name) if session_name else 'chat'
        return f"{safe_name}_{timestamp}.{extension}"
    
    def save_chat(
        self, 
        messages: List[Dict[str, str]], 
        session_name: Optional[str] = None
    ) -> str:
        """Simpan riwayat chat ke file JSON.
        
        Args:
            messages: Daftar pesan chat
            session_name: Nama sesi (opsional)
            
        Returns:
            str: Path lengkap ke file yang disimpan
            
        Raises:
            IOError: Jika gagal menulis ke file
        """
        if not messages:
            raise ValueError("Tidak ada pesan untuk disimpan")
            
        # Pastikan direktori ada
        self.storage_dir.mkdir(exist_ok=True, parents=True)
        
        # Generate nama file yang aman
        filename = self._get_filename(session_name, 'json')
        filepath = self.storage_dir / filename
        
        data = {
            "session_name": session_name,
            "messages": messages,
            "created_at": datetime.now().isoformat(),
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return str(filepath.resolve())
        except (IOError, OSError) as e:
            raise IOError(f"Gagal menyimpan chat ke {filepath}: {e}")
    
    def load_chat(self, filepath: Union[str, Path]) -> Dict[str, Any]:
        """Muat riwayat chat dari file JSON."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def export_to_pdf(
        self, 
        messages: List[Dict[str, str]], 
        session_name: Optional[str] = None
    ) -> str:
        """Ekspor riwayat chat ke file PDF.
        
        Args:
            messages: Daftar pesan chat
            session_name: Nama sesi (opsional)
            
        Returns:
            str: Path lengkap ke file yang diekspor
            
        Raises:
            ValueError: Jika tidak ada pesan untuk diekspor
            IOError: Jika gagal membuat PDF
        """
        if not messages:
            raise ValueError("Tidak ada pesan untuk diekspor")
            
        # Dapatkan nama sesi dari pesan sistem atau gunakan default
        session_title = next(
            (msg['content'] for msg in messages if msg.get('role') == 'system'),
            session_name or "Riwayat Chat"
        )
            
        # Generate nama file yang aman
        safe_name = self._sanitize_filename(session_name or "export")
        filename = f"{safe_name}_{self._get_filename()}.pdf"
        filepath = self.storage_dir / filename
        
        try:
            # Pastikan direktori ada
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            pdf = FPDF()
            pdf.add_page()
            
            # Set font default
            pdf.set_font("helvetica", size=12)
            
            # Tambahkan judul
            pdf.set_font("helvetica", 'B', 16)
            pdf.cell(0, 10, text=session_title, new_x="LMARGIN", new_y="NEXT", align='C')
            pdf.ln(10)
            
            # Tambahkan konten
            for msg in messages:
                if msg['role'] == 'system':
                    continue
                    
                role = msg.get('role', '').capitalize()
                if role == 'User':
                    role = "Anda"
                elif role == 'Assistant':
                    role = "Asisten"
                
                content = msg.get('content', '').strip()
                if not content:
                    continue
                
                # Tambahkan peran (bold)
                pdf.set_font("helvetica", 'B', 12)
                pdf.cell(0, 10, text=f"{role}:", new_x="LMARGIN", new_y="NEXT")
                
                # Tambahkan konten (normal)
                pdf.set_font("helvetica", size=12)
                pdf.multi_cell(0, 10, text=content)
                pdf.ln(5)
            
            # Simpan file
            pdf.output(str(filepath))
            return str(filepath)
            
        except Exception as e:
            raise IOError(f"Gagal membuat file PDF: {str(e)}")
    
    def search_messages(self, query: str) -> List[SearchResult]:
        """Cari pesan dalam semua file chat."""
        if not query:
            return []
            
        results: List[SearchResult] = []
        
        for filepath in self.storage_dir.glob('*.json'):
            try:
                data = self.load_chat(filepath)
                session_name = data.get('session_name', 'Tanpa Judul')
                
                for msg in data.get('messages', []):
                    content = msg.get('content', '')
                    if query.lower() in content.lower():
                        snippet = content[:100] + '...' if len(content) > 100 else content
                        results.append({
                            'session': session_name,
                            'content': content,
                            'role': msg.get('role', 'unknown'),
                            'snippet': snippet,
                            'filepath': str(filepath)
                        })
                        
            except (json.JSONDecodeError, KeyError):
                continue
                
        return results
