"""
Konfigurasi pytest untuk test suite.
"""
import warnings
import sys
import pytest

# Atur filter peringatan sebelum import lainnya
warnings.filterwarnings("ignore", category=DeprecationWarning, module='google._upb._message')
warnings.filterwarnings("ignore", message=r"Type google\\._upb\\._.* uses PyType_Spec", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=r"The parameter \"txt\" has been renamed to \"text\"", category=DeprecationWarning)

# Nonaktifkan semua peringatan DeprecationWarning untuk modul google
warnings.filterwarnings("ignore", category=DeprecationWarning, module='google')

# Atur PYTHONWARNINGS environment variable untuk menangkap peringatan lebih awal
import os
os.environ['PYTHONWARNINGS'] = 'ignore::DeprecationWarning:google._upb._message*'

# Konfigurasi pytest
def pytest_configure():
    # Nonaktifkan peringatan spesifik di level pytest
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning, module='google._upb._message')
    warnings.filterwarnings("ignore", message=r"Type google\\._upb\\._.* uses PyType_Spec")
    warnings.filterwarnings("ignore", message=r"The parameter \"txt\" has been renamed to \"text\"")
