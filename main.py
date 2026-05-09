import importlib
import logging
from nicegui import ui, app
from app.database.database_manager import BasisData
from app.ui.components import UIComponents

# Konfigurasi Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Inisialisasi Database
BasisData.inisialisasi()

# 2. Konfigurasi Static Files & Head
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
style_dir = os.path.join(base_dir, 'app', 'ui', 'style')
ui.add_head_html('<link href="/static/style.css" rel="stylesheet">', shared=True)

app.add_static_files('/static', style_dir)

# 3. Daftar Halaman (Kontrak Kerja Tim)
# Syaqila: home, wishlist
# Najla: compare, stats
# Falisha: profile, onboarding
PAGES = {
    '/': 'syaqila.home_page',
    '/search': 'syhid.search_page',
    '/compare': 'najla.compare_page',
    '/wishlist': 'syaqila.wishlist_page',
    '/stats': 'najla.stats_page',
    '/profile': 'falisha.profile_page',
    '/onboarding': 'falisha.onboarding_page',
    '/login': 'login_page',
}

@ui.page('/')
def index():
    if not app.storage.user.get('authenticated'):
        return ui.navigate.to('/login')
    
    if not app.storage.user.get('skin_type'):
        return ui.navigate.to('/onboarding')
    
    from app.ui.pages.syaqila.home_page import show_page
    return show_page()

def create_safe_route(path, module_name):
    """Fungsi pembungkus agar error di satu file tidak merusak seluruh aplikasi"""
    @ui.page(path)
    def _page_wrapper(): 
        is_standalone = path in ['/login', '/onboarding']
        try:
            # B. Proteksi Login: Jika belum login & bukan mau ke /login, lempar ke /login
            if path != '/login' and not app.storage.user.get('authenticated'):
                return ui.navigate.to('/login')
            
            # C. Proteksi Onboarding: Jika sudah login tapi belum isi data kulit (dan bukan di /onboarding)
            if path not in ['/login', '/onboarding'] and not app.storage.user.get('skin_type'):
                return ui.navigate.to('/onboarding')

            # D. Import modul secara dinamis
            module = importlib.import_module(f'app.ui.pages.{module_name}')
            importlib.reload(module)
            
            if not is_standalone:
                UIComponents.navbar()
                UIComponents.sidebar()
            
            return module.show_page()
        
        except Exception as e:
            logger.error(f"Error pada {module_name}: {e}")
            # Jika error terjadi di halaman dashboard, tetap tampilkan sidebar agar user bisa navigasi balik
            if not is_standalone:
                UIComponents.navbar()
                UIComponents.sidebar()
            
            with ui.column().classes('w-full h-screen items-center justify-center p-10'):
                ui.icon('report_problem', size='100px', color='red-200')
                ui.label('Terjadi Kesalahan Teknis').classes('text-3xl font-black text-red-600')
                ui.label(f'Gagal memuat {module_name}').classes('text-gray-500')
                with ui.expansion('Detail Error').classes('w-full max-w-2xl mt-4'):
                    ui.code(str(e)).classes('w-full bg-red-50 p-4 rounded')

# 4. Registrasi Semua Halaman
for path, module in PAGES.items():
    create_safe_route(path, module)

# 5. Jalankan Aplikasi
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="Skintify Desktop - Team Lab", 
        storage_secret='skintify-secret-key-2026',
        port=8081,
        native=True,
        window_size=(1280, 800),
        reload=True
    )
