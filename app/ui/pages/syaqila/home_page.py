from nicegui import ui
from app.context import data_mgr, state
from app.ui.components import UIComponents
from app.auth.auth import AuthManager

def show_page():
    """MISI SYAQILA: Membuat Dashboard Utama (Home)"""
    
    # --- JANGAN DIUBAH (Wajib untuk Navigasi) ---
    auth_redirect = AuthManager.require_auth()
    if auth_redirect: return auth_redirect
    UIComponents.navbar()
    UIComponents.sidebar()
    # -------------------------------------------

    # --- 🚀 MULAI KERJAKAN DI SINI (AREA BELAJAR SYAQILA) ---
    
    with ui.column().classes('w-full p-8'):
        ui.label('Misi Syaqila: Dashboard Home').classes('text-3xl font-black text-gray-300')
        ui.label('Gunakan file GUIDE.md dan CONTOH_KODE.py sebagai panduan!').classes('text-gray-400')
        
        # Cobalah membuat ui.card() untuk menampilkan ringkasan state.routine
        pass

    # --- AKHIR AREA BELAJAR ---
