import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Union
from fpdf import FPDF

from .config import Theme, Icons

class ChatHistory:
    """Kelas untuk menangani penyimpanan dan ekspor riwayat chat."""
    
    def __init__(self, storage_dir: str = "chat_history"):
        """
        Inisialisasi penyimpanan riwayat chat.
        
        Args:
            storage_dir: Direktori untuk menyimpan file riwayat
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_filename(self, extension: str = "json") -> str:
        """Membuat nama file berdasarkan timestamp saat ini."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"chat_{timestamp}.{extension}"
    
    def _sanitize_filename(self, name: str) -> str:
        """Membersihkan nama file dari karakter yang tidak valid."""
        invalid_chars = '<>:"/\\|?*' + ''.join(chr(i) for i in range(32))
        for char in invalid_chars:
            name = name.replace(char, '_')
        return name.strip()
    
    def save_chat(self, messages: List[Dict], session_name: str = None) -> str:
        """
        Menyimpan riwayat chat ke file JSON.
        
        Args:
            messages: Daftar pesan untuk disimpan
            session_name: Nama sesi (opsional)
            
        Returns:
            Path ke file yang disimpan
        """
        if not messages:
            raise ValueError("Tidak ada pesan untuk disimpan")
        
        # Buat nama file yang aman
        safe_name = self._sanitize_filename(session_name) if session_name else ""
        filename = f"{safe_name}_{self._get_filename()}" if safe_name else self._get_filename()
        filepath = self.storage_dir / filename
        
        # Pastikan nama file unik
        counter = 1
        while filepath.exists():
            filename = f"{safe_name}_{counter}_{self._get_filename()}" if safe_name else f"chat_{counter}_{self._get_filename()}"
            filepath = self.storage_dir / filename
            counter += 1
        
        # Siapkan data untuk disimpan
        chat_data = {
            "session_name": session_name or "Sesi Tanpa Nama",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_count": len(messages),
            "messages": messages
        }
        
        # Simpan ke file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(chat_data, f, ensure_ascii=False, indent=2)
            return str(filepath)
        except Exception as e:
            raise Exception(f"Gagal menyimpan chat: {str(e)}")
    
    def load_chat(self, filepath: Union[str, Path]) -> Dict:
        """
        Memuat riwayat chat dari file.
        
        Args:
            filepath: Path ke file yang akan dimuat
            
        Returns:
            Data chat yang dimuat
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise ValueError("File tidak valid atau korup")
        except Exception as e:
            raise Exception(f"Gagal memuat chat: {str(e)}")
    
    def list_sessions(self) -> List[Dict]:
        """
        Mendapatkan daftar sesi chat yang tersimpan.
        
        Returns:
            Daftar dictionary berisi informasi sesi
        """
        sessions = []
        
        for filepath in self.storage_dir.glob("*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                sessions.append({
                    "session_name": data.get("session_name", "Sesi Tanpa Nama"),
                    "created_at": data.get("created_at", "Tidak Diketahui"),
                    "message_count": data.get("message_count", 0),
                    "filepath": str(filepath),
                    "filename": filepath.name
                })
            except (json.JSONDecodeError, KeyError):
                continue
        
        # Urutkan berdasarkan waktu pembuatan (terbaru dulu)
        sessions.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return sessions
    
    def export_to_txt(self, messages: List[Dict], session_name: str = None) -> str:
        """
        Mengekspor chat ke file teks.
        
        Args:
            messages: Daftar pesan untuk diekspor
            session_name: Nama sesi (opsional)
            
        Returns:
            Path ke file yang diekspor
        """
        safe_name = self._sanitize_filename(session_name) if session_name else "export"
        filename = f"{safe_name}_{self._get_filename('txt')}"
        filepath = self.storage_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"=== Ekspor Chat ===\n")
            f.write(f"Sesi: {session_name or 'Tidak Diketahui'}\n")
            f.write(f"Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 40 + "\n\n")
            
            for msg in messages:
                role = "Anda" if msg.get('role') == 'user' else "Asisten"
                content = msg.get('content', '').replace('\n', '\n    ')
                f.write(f"{role}:\n    {content}\n\n")
        
        return str(filepath)
    
    def export_to_pdf(self, messages: List[Dict], session_name: str = None) -> str:
        """
        Mengekspor chat ke file PDF.
        
        Args:
            messages: Daftar pesan untuk diekspor
            session_name: Nama sesi (opsional)
            
        Returns:
            Path ke file PDF yang dihasilkan
        """
        safe_name = self._sanitize_filename(session_name) if session_name else "export"
        filename = f"{safe_name}_{self._get_filename('pdf')}"
        filepath = self.storage_dir / filename
        
        pdf = FPDF()
        pdf.add_page()
        
        # Tambahkan judul
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Ekspor Chat', 0, 1, 'C')
        
        # Tambahkan metadata
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 10, f'Sesi: {session_name or "Tidak Diketahui"}', 0, 1)
        pdf.cell(0, 10, f'Tanggal: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1)
        pdf.ln(10)
        
        # Tambahkan isi chat
        pdf.set_font('Arial', '', 12)
        for msg in messages:
            role = "Anda" if msg.get('role') == 'user' else "Asisten"
            content = msg.get('content', '')
            
            # Tambahkan peran dengan tebal
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, f"{role}:", 0, 1)
            
            # Tambahkan konten dengan format normal
            pdf.set_font('Arial', '', 12)
            pdf.multi_cell(0, 10, content)
            pdf.ln(5)
        
        # Simpan file
        pdf.output(str(filepath))
        return str(filepath)
    
    def search_messages(self, query: str, session_file: str = None, case_sensitive: bool = False) -> List[Dict]:
        """
        Mencari pesan yang mengandung teks tertentu.
        
        Args:
            query: Teks yang ingin dicari
            session_file: File sesi spesifik (opsional)
            case_sensitive: Pencarian case-sensitive
            
        Returns:
            List pesan yang cocok dengan query
        """
        results = []
        files_to_search = []
        
        # Pastikan direktori ada
        if not self.storage_dir.exists():
            return results
        
        # Tentukan file yang akan dicari
        if session_file:
            if not session_file.endswith('.json'):
                session_file += '.json'
            file_path = self.storage_dir / session_file
            if file_path.exists():
                files_to_search.append(file_path)
        else:
            # Cari di semua file JSON
            files_to_search = list(self.storage_dir.glob('*.json'))
        
        # Lakukan pencarian
        for file_path in files_to_search:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Dapatkan nama sesi
                session_name = data.get('session_name', 'Sesi Tanpa Nama')
                created_at = data.get('created_at', 'Tidak Diketahui')
                
                # Cari di setiap pesan
                for msg in data.get('messages', []):
                    content = msg.get('content', '')
                    if not isinstance(content, str):
                        content = str(content)
                        
                    role = msg.get('role', 'unknown')
                    
                    # Lakukan pencarian
                    search_content = content if case_sensitive else content.lower()
                    search_query = query if case_sensitive else query.lower()
                    
                    if search_query in search_content:
                        results.append({
                            'session': session_name,
                            'session_file': str(file_path.name),
                            'created_at': created_at,
                            'role': role,
                            'content': content,
                            'snippet': self._get_snippet(content, query, case_sensitive) or content[:100] + '...'
                        })
                        
            except (json.JSONDecodeError, KeyError, IOError) as e:
                print(f"{Theme.ERROR}Error processing {file_path}: {e}{Style.RESET_ALL}" if 'Theme' in globals() else f"Error processing {file_path}: {e}")
                continue
                
        return results
    
    def _get_snippet(self, content: str, query: str, case_sensitive: bool = False, context_words: int = 10) -> str:
        """
        Menghasilkan potongan teks dengan kata kunci yang disorot.
        
        Args:
            content: Teks lengkap
            query: Kata kunci yang dicari
            case_sensitive: Pencarian case-sensitive
            context_words: Jumlah kata di sekitar kata kunci yang akan ditampilkan
            
        Returns:
            Potongan teks dengan kata kunci yang disorot
        """
        if not content or not query:
            return content or ""
            
        # Normalisasi teks dan query untuk pencarian
        text = content if case_sensitive else content.lower()
        search_term = query if case_sensitive else query.lower()
        
        # Cari posisi pertama kemunculan query
        pos = text.find(search_term)
        if pos == -1:
            return content[:100] + '...' if len(content) > 100 else content
            
        # Hitung batas awal dan akhir
        start = max(0, content.rfind(' ', 0, pos - 1) + 1)
        end = min(len(content), content.find(' ', pos + len(query)) + 1)
        
        # Ambil konteks sekitar
        words = content.split()
        query_words = query.split()
        
        # Cari semua kemunculan query
        matches = []
        for i in range(len(words) - len(query_words) + 1):
            match = True
            for j in range(len(query_words)):
                word = words[i + j].lower() if not case_sensitive else words[i + j]
                if word != (query_words[j].lower() if not case_sensitive else query_words[j]):
                    match = False
                    break
            if match:
                matches.append(i)
        
        if not matches:
            return content[:100] + '...' if len(content) > 100 else content
        
        # Ambil konteks sekitar setiap kemunculan
        snippets = []
        for idx in matches:
            start_idx = max(0, idx - context_words)
            end_idx = min(len(words), idx + len(query_words) + context_words)
            snippet = ' '.join(words[start_idx:end_idx])
            
            # Sorot query dalam snippet
            for i in range(idx, idx + len(query_words)):
                if i < len(words):
                    words[i] = f"**{words[i]}**"
            
            snippets.append(snippet)
        
        # Gabungkan semua snippet dengan elipsis
        return "... " + " ... ".join(snippets) + " ..."
