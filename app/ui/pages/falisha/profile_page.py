from nicegui import ui
from app.context import data_mgr, state
from app.ui.components import UIComponents
from app.auth.auth import AuthManager

def show_page():
    """MISI FALISHA: Membuat Pengaturan Profil"""
    
    # --- JANGAN DIUBAH (Wajib untuk Navigasi) ---
    auth_redirect = AuthManager.require_auth()
    if auth_redirect: return auth_redirect
    UIComponents.navbar()
    UIComponents.sidebar()
    # -------------------------------------------

    # --- 🚀 MULAI KERJAKAN DI SINI (AREA BELAJAR FALISHA) ---
    
    with ui.column().classes('w-full p-8'):
        ui.label('Misi Falisha: Pengaturan Profil').classes('text-3xl font-black text-gray-300')
        
        # Cobalah buat ui.input() dan ui.select() untuk biodata user
        pass

    # --- AKHIR AREA BELAJAR ---
