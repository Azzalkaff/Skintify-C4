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
base_dir  = os.path.dirname(os.path.abspath(__file__))
style_dir = os.path.join(base_dir, 'app', 'ui', 'style')
ui.add_head_html('<link href="/static/style.css" rel="stylesheet">', shared=True)
app.add_static_files('/static', style_dir)

# 3. Daftar Halaman (Kontrak Kerja Tim)
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


def muat_profil_ke_storage(email: str):
    """
    Load data profil user dari DB ke app.storage.user.
    Dipanggil setelah login agar skin_type dll langsung tersedia
    tanpa perlu isi onboarding lagi.
    """
    try:
        data_user = BasisData.ambil_pengguna_by_identifier(email)
        if data_user:
            app.storage.user['email']             = data_user.get('email', email)
            app.storage.user['username']          = data_user.get('username', '')
            app.storage.user['skin_type']         = data_user.get('skin_type', '')
            app.storage.user['avoid_ingredients'] = data_user.get('avoid_ingredients', [])
            app.storage.user['skin_issues']       = data_user.get('skin_issues', [])
    except Exception as e:
        logger.error(f"[muat_profil] Gagal load profil dari DB: {e}")


# ─────────────────────────────────────────────────────────────────────────────
#  HELPER RIWAYAT AKTIVITAS
#  Contoh pemakaian di halaman lain:
#    from main import tambah_riwayat
#    tambah_riwayat('compare_arrows', 'blue', 'Membandingkan 2 produk', 'Wardah vs The Ordinary')
# ─────────────────────────────────────────────────────────────────────────────
def tambah_riwayat(icon: str, color: str, judul: str, subjudul: str = ''):
    """Tambah satu entri ke riwayat aktivitas user di app.storage."""
    import datetime
    riwayat = app.storage.user.get('activity_log', [])
    riwayat.insert(0, {
        'icon':     icon,
        'color':    color,
        'judul':    judul,
        'subjudul': subjudul,
        'waktu':    datetime.datetime.now().strftime('%d %b %Y, %H:%M'),
    })
    app.storage.user['activity_log'] = riwayat[:20]


# 4. Route Khusus: Halaman Utama (/)
@ui.page('/')
def index():
    if not app.storage.user.get('authenticated'):
        return ui.navigate.to('/login')
    # Langsung ke home — tidak ada cek skin_type di sini
    # skin_type sudah dimuat dari DB oleh login_page saat login
    from app.ui.pages.syaqila.home_page import show_page
    return show_page()


# 5. Fungsi Pembungkus Route yang Aman
def create_safe_route(path, module_name):
    """Membungkus setiap halaman agar error di satu file tidak crash seluruh app."""

    @ui.page(path)
    def _page_wrapper():
        is_standalone = path in ['/login', '/onboarding']

        try:
            # Proteksi Login: semua halaman kecuali /login butuh autentikasi
            if path != '/login' and not app.storage.user.get('authenticated'):
                return ui.navigate.to('/login')

            # ── TIDAK ADA cek skin_type di sini ──────────────────────────────
            # skin_type dimuat dari DB oleh login_page → tidak perlu redirect
            # ke onboarding setiap kali user buka halaman baru

            module = importlib.import_module(f'app.ui.pages.{module_name}')
            importlib.reload(module)

            if not is_standalone:
                UIComponents.navbar()
                UIComponents.sidebar()

            return module.show_page()

        except Exception as e:
            logger.error(f"Error pada {module_name}: {e}")
            if not is_standalone:
                UIComponents.navbar()
                UIComponents.sidebar()

            with ui.column().classes('w-full h-screen items-center justify-center p-10'):
                ui.icon('report_problem', size='100px', color='red-200')
                ui.label('Ups! Terjadi Kesalahan Teknis').classes(
                    'text-3xl font-black text-red-600'
                )
                ui.label(f'Halaman {module_name} sedang diperbaiki oleh rekan tim Anda.').classes(
                    'text-gray-500'
                )
                with ui.expansion('Detail Error untuk Developer').classes('w-full max-w-2xl mt-4'):
                    ui.code(str(e)).classes('w-full bg-red-50 p-4 rounded')


# 6. Registrasi Semua Halaman
for path, module in PAGES.items():
    create_safe_route(path, module)


# 7. Jalankan Aplikasi
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title='Skintify Desktop - Team Lab',
        storage_secret='skintify-secret-key-2026',
        port=8081,
        native=True,
        window_size=(1280, 800),
        reload=True,
    )