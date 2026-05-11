from nicegui import ui, app
from app.context import data_mgr, state
from app.ui.components import UIComponents
from app.auth.auth import AuthManager


def show_page():
    """MISI FALISHA: Halaman Profil Lengkap"""

    # --- JANGAN DIUBAH (Wajib untuk Navigasi) ---
    auth_redirect = AuthManager.require_auth()
    if auth_redirect: return auth_redirect
    UIComponents.navbar()
    UIComponents.sidebar()
    # -------------------------------------------

    # --- 🚀 MULAI KERJAKAN DI SINI ---

    # ── Ambil semua data dari app.storage.user ────────────────────────────────
    email    = app.storage.user.get('email', 'user@skintify.com')
    username = app.storage.user.get('username', '')

    # Kalau username kosong di storage, coba ambil dari DB
    if not username:
        try:
            from app.database.database_manager import BasisData
            data_user = BasisData.ambil_pengguna_by_identifier(email)
            if data_user:
                username = data_user.get('username', '')
                if username:
                    app.storage.user['username'] = username
        except Exception:
            pass

    # Fallback terakhir
    if not username:
        username = email.split('@')[0].capitalize()

    skin_type    = app.storage.user.get('skin_type', 'Belum diisi')
    hindari_list = app.storage.user.get('avoid_ingredients', [])
    masalah_list = app.storage.user.get('skin_issues', [])
    activity_log = app.storage.user.get('activity_log', [])

    hindari_text = ', '.join(hindari_list) if hindari_list else 'Tidak ada'
    masalah_text = ', '.join(masalah_list) if masalah_list else 'Belum diisi'

    # ── LAYOUT UTAMA ─────────────────────────────────────────────────────────
    # Pakai height penuh layar tanpa scroll di level halaman
    with ui.column().classes('w-full p-6 gap-4').style(
        'height: calc(100vh - 60px); overflow: hidden;'
    ):

        # ════════════════════════════════════════════════════════════════════
        #  BAGIAN 1: KARTU IDENTITAS (ATAS) — vertikal seperti semula tapi compact
        # ════════════════════════════════════════════════════════════════════
        with ui.card().classes('w-full shadow-sm rounded-2xl py-4 px-8'):
            with ui.column().classes('w-full items-center gap-2'):

                # Avatar lebih kecil dari semula
                ui.icon('person', size='3rem').classes(
                    'bg-pink-100 text-pink-600 rounded-full p-2'
                )

                # Nama & gelar — font sedikit lebih kecil
                ui.label(username).classes('text-xl font-bold text-gray-800')
                ui.label('Pengguna Skintify').classes('text-xs text-gray-400')

                # Badge tetap di bawah nama
                with ui.row().classes('gap-2 flex-wrap justify-center mt-1'):
                    ui.badge(f'Kulit: {skin_type}', color='pink-100').classes(
                        'text-pink-600 px-3 py-1 font-bold text-xs'
                    )
                    for masalah in masalah_list[:3]:
                        ui.badge(masalah, color='pink-100').classes(
                            'text-pink-600 px-3 py-1 font-bold text-xs'
                        )
                    for bahan in hindari_list[:2]:
                        ui.badge(f'Hindari: {bahan}', color='red-100').classes(
                            'text-red-500 px-3 py-1 font-bold text-xs'
                        )
                    sisa = max(0, len(masalah_list) - 3) + max(0, len(hindari_list) - 2)
                    if sisa > 0:
                        ui.badge(f'+{sisa} lagi', color='gray-100').classes(
                            'text-gray-500 px-3 py-1 text-xs'
                        )

        # ════════════════════════════════════════════════════════════════════
        #  BAGIAN 2: DATA PROFIL (KIRI) + RIWAYAT AKTIVITAS (KANAN)
        #  flex-1 agar mengisi sisa tinggi layar, overflow-auto di dalam kartu
        # ════════════════════════════════════════════════════════════════════
        with ui.row().classes('w-full gap-4 flex-1').style('overflow: hidden; min-height: 0;'):

            # ── KARTU KIRI: Data Profil ───────────────────────────────────
            with ui.card().classes('flex-1 p-6 shadow-sm rounded-2xl').style('overflow-y: auto;'):
                ui.label('Data Profil').classes('font-bold text-xl mb-4 text-pink-500')

                with ui.column().classes('w-full gap-3'):
                    _baris_data('Nama',            username)
                    _baris_data('Email',           email)
                    _baris_data('Tipe Kulit',      skin_type)
                    _baris_data('Bahan Dihindari', hindari_text)
                    _baris_data('Masalah Kulit',   masalah_text)

                ui.separator().classes('my-3')

                # ── Tombol Edit Profil (PINK) ─────────────────────────────
                def ke_edit_profil():
                    app.storage.user['onboarding_mode'] = 'edit'
                    ui.navigate.to('/onboarding')

                ui.button('✏️  Edit Profil', on_click=ke_edit_profil).classes(
                    'w-full text-white font-bold py-3 rounded-xl mt-1'
                ).style('background: #E91E8C;')

                # ── Tombol Logout ─────────────────────────────────────────
                def do_logout():
                    AuthManager.logout()
                    state.routine = []
                    ui.notify('Berhasil logout. Sampai jumpa! 👋', color='positive')
                    ui.navigate.to('/login')

                with ui.dialog() as confirm_dialog, ui.card().classes('p-6 gap-4'):
                    ui.label('Yakin mau logout?').classes('text-lg font-bold')
                    ui.label('Kamu akan keluar dari akun Skintify-mu.').classes(
                        'text-sm text-gray-500'
                    )
                    with ui.row().classes('gap-3 mt-2'):
                        ui.button('Batal', on_click=confirm_dialog.close).props('flat')
                        ui.button('Ya, Logout', on_click=do_logout).classes(
                            'text-white px-4 bg-red-500 rounded-lg'
                        )

                ui.button('🚪  Logout', on_click=confirm_dialog.open).classes(
                    'w-full border border-red-200 text-red-500 font-bold py-3 rounded-xl mt-2'
                ).props('flat')

            # ── KARTU KANAN: Riwayat Aktivitas ───────────────────────────
            with ui.card().classes('flex-1 p-6 shadow-sm rounded-2xl').style('overflow-y: auto;'):
                ui.label('Riwayat Aktivitas').classes('font-bold text-xl mb-4 text-gray-800')

                if activity_log:
                    for act in activity_log:
                        _baris_riwayat(
                            icon     = act.get('icon', 'circle'),
                            color    = act.get('color', 'pink'),
                            judul    = act.get('judul', ''),
                            subjudul = act.get('subjudul', ''),
                            waktu    = act.get('waktu', ''),
                        )
                else:
                    with ui.column().classes('items-center justify-center w-full py-10 gap-2'):
                        ui.icon('history', size='3rem').classes('text-gray-300')
                        ui.label('Belum ada aktivitas').classes('text-gray-400 font-bold')
                        ui.label(
                            'Cari produk, bandingkan, atau tambah wishlist\n'
                            'untuk melihat riwayatmu di sini!'
                        ).classes('text-xs text-gray-400 text-center whitespace-pre-line')

    # --- AKHIR AREA BELAJAR ---


# ── Helper UI ─────────────────────────────────────────────────────────────────

def _baris_data(label: str, nilai: str):
    """Satu baris tabel data profil: label kiri, nilai kanan."""
    with ui.row().classes('w-full justify-between border-b pb-2'):
        ui.label(label).classes('text-gray-500 text-sm')
        ui.label(nilai).classes('font-bold text-right text-sm')


def _baris_riwayat(icon: str, color: str, judul: str, subjudul: str, waktu: str):
    """Satu entri riwayat aktivitas."""
    with ui.row().classes('w-full items-start gap-3 mb-3 border-b pb-3'):
        ui.icon(icon, color=color).classes('mt-1 text-xl')
        with ui.column().classes('gap-0 flex-1'):
            ui.label(judul).classes('font-bold text-sm text-gray-800')
            ui.label(subjudul).classes('text-xs text-gray-500')
        ui.label(waktu).classes('text-xs text-gray-400 whitespace-nowrap')