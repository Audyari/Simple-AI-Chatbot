#!/usr/bin/env python3
"""
Skrip untuk menjalankan pengujian dengan pytest.
"""
import sys
import pytest

def run_tests():
    """Jalankan pengujian dengan pytest."""
    # Tambahkan direktori src ke path Python
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
    
    # Jalankan pytest
    return pytest.main([
        '--cov=src',  # Aktifkan coverage
        '--cov-report=term-missing',  # Tampilkan baris yang tidak tercakup
        '--verbose',  # Output lebih detail
        'tests/'  # Direktori test
    ])

if __name__ == '__main__':
    sys.exit(run_tests())
