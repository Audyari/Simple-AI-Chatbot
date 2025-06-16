import json
import os
from datetime import datetime
from typing import List, Dict
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
    
    def _get_filename(self, extension: str = "json") -> str:
        """Membuat nama file berdasarkan timestamp saat ini."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"chat_{timestamp}.{extension}"
    
    def save_chat(self, messages: List[Dict], session_name: str = None) -> str:
        """
        Menyimpan riwayat chat ke file JSON.
        
        Args:
            messages: Daftar pesan untuk disimpan
            session_name: Nama sesi (opsional)
            
        Returns:
            Path ke file yang disimpan
        """
        try:
            # Buat direktori jika belum ada
            self.storage_dir.mkdir(parents=True, exist_ok=True)
            
            # Buat nama file default jika tidak disediakan
            if not session_name:
                session_name = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Pastikan nama file aman
            safe_name = "".join(c if c.isalnum() or c in ' _-.' else '_' for c in session_name)
            safe_name = safe_name.strip()
            
            # Jika nama file sudah ada, tambahkan timestamp
            file_path = self.storage_dir / f"{safe_name}.json"
            counter = 1
            while file_path.exists():
                file_path = self.storage_dir / f"{safe_name}_{counter}.json"
                counter += 1
            
            # Siapkan data untuk disimpan
            chat_data = {
                'session_name': safe_name,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'messages': messages
            }
            
            # Simpan ke file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(chat_data, f, ensure_ascii=False, indent=2)
                
            return str(file_path)
            
        except Exception as e:
            print(f"Error saving chat: {e}")
            return ""
    
    def export_to_txt(self, messages: List[Dict], session_name: str = None) -> str:
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
    
    def export_to_pdf(self, messages: List[Dict], session_name: str = None) -> str:
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
    
    def list_sessions(self) -> List[Dict]:
        """
        Mendapatkan daftar sesi chat yang tersimpan.
        
        Returns:
            Daftar kamus berisi informasi sesi
        """
        sessions = []
        for file_path in self.storage_dir.glob('*.json'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                sessions.append({
                    'session_name': data.get('session_name', 'Sesi Tanpa Nama'),
                    'created_at': data.get('created_at', 'Tidak Diketahui'),
                    'filepath': str(file_path),
                    'message_count': len(data.get('messages', []))
                })
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error reading {file_path}: {e}")
                continue
        
        # Urutkan berdasarkan waktu pembuatan (terbaru dulu)
        sessions.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return sessions
    
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
                session_name = data.get('session_name', 'Unnamed Session')
                created_at = data.get('created_at', 'Unknown')
                
                # Cari di setiap pesan
                for msg in data.get('messages', []):
                    content = msg.get('content', '')
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
                            'snippet': self._get_snippet(content, query, case_sensitive)
                        })
                        
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error processing {file_path}: {e}")
                continue
                
        return results
    
    def _get_snippet(self, content: str, query: str, case_sensitive: bool = False, context_words: int = 10) -> str:
        """
        Mendapatkan potongan teks di sekitar kata kunci.
        
        Args:
            content: Teks lengkap
            query: Kata kunci yang dicari
            case_sensitive: Pencarian case-sensitive
            context_words: Jumlah kata di sekitar kata kunci
            
        Returns:
            Potongan teks dengan kata kunci yang disorot
        """
        if not content or not query:
            return ""
            
        content_search = content if case_sensitive else content.lower()
        query_search = query if case_sensitive else query.lower()
        
        idx = content_search.find(query_search)
        if idx == -1:
            return ""
            
        # Temukan awal dan akhir potongan teks
        start = max(0, content.rfind(' ', 0, idx - 1) + 1)
        end = len(content)
        
        # Potong teks
        snippet = content[start:end]
        
        # Potong ke jumlah kata yang diinginkan
        words = snippet.split()
        if len(words) > context_words * 2:
            words = words[:context_words] + ['...'] + words[-context_words:]
            snippet = ' '.join(words)
        
        # Sorot kata kunci
        snippet = snippet.replace(query, f"**{query}**")
        
        return snippet
