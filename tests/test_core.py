import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock
from pathlib import Path

# Tambahkan direktori root ke path Python
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.chatbot.core import Chatbot
from src.chatbot.config import Config

class TestChatbot(unittest.TestCase):
    def setUp(self):
        """Menyiapkan environment pengujian."""
        # Setup konfigurasi untuk testing
        self.temp_dir = tempfile.TemporaryDirectory()
        Config.GEMINI_API_KEY = "test_api_key"
        Config.DEFAULT_MODEL = "test-model"
        
        # Inisialisasi chatbot dengan mock
        self.chatbot = Chatbot()
        
        # Mock model Gemini
        self.chatbot.model = MagicMock()
        self.chatbot.chat = MagicMock()
        
        # Mock response dari model
        self.mock_response = MagicMock()
        self.mock_response.text = "Ini adalah respons dari AI"
        self.chatbot.chat.send_message.return_value = self.mock_response
    
    def tearDown(self):
        """Bersihkan setelah pengujian."""
        self.temp_dir.cleanup()
    
    def test_get_response(self):
        """Test mendapatkan respons dari model."""
        with patch('builtins.print'):  # Menekan output ke console
            response = self.chatbot.get_response("Halo")
            
        # Verifikasi respons
        self.assertEqual(response, "Ini adalah respons dari AI")
        self.chatbot.chat.send_message.assert_called_once_with("Halo")
    
    def test_save_chat_session(self):
        """Test menyimpan sesi chat."""
        # Setup
        self.chatbot.messages = [
            {"role": "system", "content": "Test system message"},
            {"role": "user", "content": "Test user message"}
        ]
        
        # Simpan chat
        with patch('builtins.print'):  # Menekan output ke console
            filepath = self.chatbot.save_chat_session("test_session")
        
        # Verifikasi
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(filepath.endswith('.json'))
    
    def test_export_chat(self):
        """Test ekspor chat ke PDF."""
        # Setup
        self.chatbot.messages = [
            {"role": "system", "content": "Test system message"},
            {"role": "user", "content": "Test user message"}
        ]
        
        # Test ekspor ke PDF
        with patch('builtins.print'):  # Menekan output ke console
            filepath = self.chatbot.export_chat("pdf")
        
        # Verifikasi
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(filepath.endswith('.pdf'))
        
        # Test error untuk format tidak didukung
        with self.assertRaises(ValueError):
            self.chatbot.export_chat("txt")
    
    def test_search_chat_history(self):
        """Test pencarian riwayat chat."""
        # Mock hasil pencarian
        mock_results = [
            {
                "session": "test_session",
                "content": "Ini adalah pesan uji",
                "role": "user",
                "snippet": "...Ini adalah pesan uji..."
            }
        ]
        
        # Mock method search_messages
        with patch('src.chatbot.storage.ChatHistory.search_messages', 
                  return_value=mock_results) as mock_search:
            results = self.chatbot.search_chat_history("test")
            
            # Verifikasi
            mock_search.assert_called_once()
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["content"], "Ini adalah pesan uji")

if __name__ == "__main__":
    unittest.main()
