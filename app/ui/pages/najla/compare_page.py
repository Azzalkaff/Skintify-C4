from nicegui import ui
from app.context import data_mgr, state
from app.ui.components import UIComponents
from app.auth.auth import AuthManager

def show_page():
    """MISI NAJLA: Membuat Logika Perbandingan Produk"""
    
    # --- JANGAN DIUBAH (Wajib untuk Navigasi) ---
    auth_redirect = AuthManager.require_auth()
    if auth_redirect: return auth_redirect
    UIComponents.navbar()
    UIComponents.sidebar()
    # -------------------------------------------

    # --- 🚀 MULAI KERJAKAN DI SINI (AREA BELAJAR NAJLA) ---
    
    with ui.column().classes('w-full p-8'):
        ui.label('Misi Najla: Perbandingan Produk').classes('text-3xl font-black text-gray-300')
        
        # Cobalah ambil 2 produk dari state.routine dan bandingkan harganya
        pass

    # --- AKHIR AREA BELAJAR ---
