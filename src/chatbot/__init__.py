"""
Package untuk Simple AI Chatbot dengan Google Gemini.
"""

__version__ = '0.2.0'

from .core import Chatbot
from .config import Config
from . import storage

__all__ = ['Chatbot', 'Config', 'storage']
