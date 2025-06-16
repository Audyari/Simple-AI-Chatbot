import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

class ChatHistory:
    """Kelas untuk menangani penyimpanan dan pemuatan riwayat chat."""
    
    def __init__(self, storage_dir: str = "chat_history"):
        """
        Inisialisasi penyimpanan riwayat chat.
        
        Args:
            storage_dir: Direktori untuk menyimpan file riwayat
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
    
    def _get_filename(self) -> str:
        """Membuat nama file berdasarkan timestamp saat ini."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"chat_{timestamp}.json"
    
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
        
        filename = self._get_filename()
        filepath = self.storage_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        return str(filepath)
    
    def load_chat(self, filepath: str) -> Dict:
        """
        Memuat riwayat chat dari file.
        
        Args:
            filepath: Path ke file riwayat chat
            
        Returns:
            Data riwayat chat
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"File tidak ditemukan: {filepath}")
            
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_sessions(self) -> List[Dict]:
        """
        Mendapatkan daftar semua sesi chat yang tersimpan.
        
        Returns:
            Daftar dictionary berisi info sesi
        """
        sessions = []
        for file in self.storage_dir.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    sessions.append({
                        "filepath": str(file),
                        "session_name": data.get("session_name", "Unnamed"),
                        "created_at": data.get("created_at", "Unknown"),
                        "message_count": len(data.get("messages", []))
                    })
            except (json.JSONDecodeError, KeyError):
                continue
                
        # Urutkan berdasarkan waktu pembuatan (terbaru dulu)
        sessions.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return sessions
