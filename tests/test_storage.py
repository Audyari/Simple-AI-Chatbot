import os
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Tambahkan direktori root ke path Python
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.chatbot.storage import ChatHistory

class TestChatHistory(unittest.TestCase):    
    def setUp(self):
        """Menyiapkan environment pengujian."""
        # Buat direktori sementara untuk pengujian
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = ChatHistory(storage_dir=self.temp_dir.name)
        
        # Data contoh untuk pengujian
        self.sample_messages = [
            {"role": "system", "content": "Anda adalah asisten AI yang ramah."},
            {"role": "user", "content": "Halo, apa kabar?"},
            {"role": "assistant", "content": "Halo! Saya baik, terima kasih! Ada yang bisa saya bantu?"}
        ]
    
    def tearDown(self):
        """Bersihkan setelah pengujian."""
        self.temp_dir.cleanup()
    
    def test_save_and_load_chat(self):
        """Test menyimpan dan memuat chat."""
        # Simpan chat
        filepath = self.storage.save_chat(self.sample_messages, "test_session")
        
        # Verifikasi file dibuat
        self.assertTrue(os.path.exists(filepath))
        
        # Muat chat
        loaded_data = self.storage.load_chat(filepath)
        
        # Verifikasi data yang dimuat
        self.assertEqual(loaded_data["messages"], self.sample_messages)
        self.assertEqual(loaded_data["session_name"], "test_session")
    
    def test_export_to_pdf(self):
        """Test ekspor ke format PDF."""
        # Ekspor ke PDF
        filepath = self.storage.export_to_pdf(self.sample_messages, "test_export")
        
        # Verifikasi file dibuat
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(filepath.endswith('.pdf'))
    
    def test_search_messages(self):
        """Test pencarian pesan."""
        # Simpan beberapa chat terlebih dahulu
        self.storage.save_chat(self.sample_messages, "test_search")
        
        # Lakukan pencarian
        results = self.storage.search_messages("Halo")
        
        # Verifikasi hasil pencarian
        self.assertGreater(len(results), 0)
        self.assertIn("Halo", results[0]["content"])

if __name__ == "__main__":
    unittest.main()
