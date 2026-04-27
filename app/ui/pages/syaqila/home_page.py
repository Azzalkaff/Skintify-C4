from nicegui import ui
from app.context import data_mgr, state
from app.ui.components import UIComponents
from app.auth.auth import AuthManager


def show_page():

    # --- JANGAN DIUBAH (Wajib untuk Navigasi) ---
    auth_redirect = AuthManager.require_auth()
    if auth_redirect: return auth_redirect
    UIComponents.navbar()
    UIComponents.sidebar()
    # -------------------------------------------

    # --- SET DEFAULT CATEGORY ---
    if not hasattr(state, 'category'):
        state.category = 'Serum'

    # --- FUNCTION PILIH KATEGORI ---
    def pilih_kategori(kategori):
        state.category = kategori
        ui.notify(f'Pilih: {kategori}')
        ui.navigate.to('/')


    with ui.column().classes('w-full p-8'):

        # 📊 RINGKASAN DATA 
        ui.label('RINGKASAN DATA').classes('text-sm font-bold text-gray-500 mb-2')

        with ui.row().classes('w-full gap-4 mb-8'):

            with ui.card().classes('flex-1 items-center justify-center p-4 shadow-sm'):
                ui.label('Total produk').classes('text-xs text-gray-500')
                ui.label('312').classes('text-3xl font-black')
                ui.label('dari 3 sumber').classes('text-xs text-green-500')

            with ui.card().classes('flex-1 items-center justify-center p-4 shadow-sm'):
                ui.label('Jumlah merek').classes('text-xs text-gray-500')
                ui.label('48').classes('text-3xl font-black')
                ui.label('lokal & internasional').classes('text-xs text-green-500')

            with ui.card().classes('flex-1 items-center justify-center p-4 shadow-sm'):
                ui.label('Rating tertinggi').classes('text-xs text-gray-500')
                ui.label('4.9').classes('text-3xl font-black')
                ui.label('Somethinc Serum').classes('text-xs text-green-500')

            with ui.card().classes('flex-1 items-center justify-center p-4 shadow-sm'):
                ui.label('Harga terjangkau').classes('text-xs text-gray-500')
                ui.label('Rp12k').classes('text-3xl font-black')
                ui.label('harga/ml terendah').classes('text-xs text-green-500')


        # 🧴 PILIH KATEGORI 
        ui.label('PILIH KATEGORI').classes('text-sm font-bold text-gray-500 mb-2')

        with ui.row().classes('w-full justify-between gap-4 mb-8'):

            def card_kategori(nama, emoji):
                aktif = state.category == nama

                with ui.card().classes(
                    f'w-48 items-center cursor-pointer transition transform duration-150 '
                    f'active:scale-95 hover:shadow-md '
                    + ('bg-pink-50 border border-pink-200' if aktif else '')
                ).on('click', lambda: pilih_kategori(nama)):

                    ui.label(emoji).classes('text-2xl')
                    ui.label(nama).classes(
                        'text-xs font-bold text-pink-500'
                        if aktif else 'text-xs text-gray-500'
                    )

            # Daftar kategori
            card_kategori('Serum', '💧')
            card_kategori('Moisturizer', '🧴')
            card_kategori('Sunscreen', '☀️')
            card_kategori('Toner', '🌊')
            card_kategori('Cleanser', '🫧')

        with ui.row().classes('w-full gap-8 items-stretch'):
            
            # KOLOM KIRI (Produk Terakhir)
            with ui.card().classes('flex-[2] p-6 shadow-sm'):
                ui.label('Produk terakhir dilihat').classes('font-bold mb-4')
                # Produk 1
                with ui.row().classes('w-full items-center justify-between border-b pb-2'):
                    ui.label('💧').classes('text-3xl bg-pink-50 rounded-lg p-2')
                    with ui.column().classes('gap-0 flex-1 ml-4'):
                        ui.label('Niacinamide 10% + Zinc 1%').classes('font-bold text-sm')
                        ui.label('The Ordinary').classes('text-xs text-gray-500')
                    with ui.column().classes('items-end gap-0'):
                        ui.label('Rp145k').classes('text-pink-500 font-bold text-sm')
                        ui.label('★★★★★').classes('text-yellow-400 text-xs')

                with ui.row().classes('w-full items-center justify-between border-b pb-2'):
                    ui.label('🧴').classes('text-3xl bg-pink-50 rounded-lg p-2')
                    with ui.column().classes('gap-0 flex-1 ml-4'):
                        ui.label('Acne Squad Serum').classes('font-bold text-sm')
                        ui.label('Somethinc').classes('text-xs text-gray-500')
                    with ui.column().classes('items-end gap-0'):
                        ui.label('Rp189k').classes('text-pink-500 font-bold text-sm')
                        ui.label('★★★★').classes('text-yellow-400 text-xs')

                with ui.row().classes('w-full items-center justify-between border-b pb-2'):
                    ui.label('☀️').classes('text-3xl bg-pink-50 rounded-lg p-2')
                    with ui.column().classes('gap-0 flex-1 ml-4'):
                        ui.label('UV Shield SPF50+').classes('font-bold text-sm')
                        ui.label('Somethinc').classes('text-xs text-gray-500')
                    with ui.column().classes('items-end gap-0'):
                        ui.label('Rp78k').classes('text-pink-500 font-bold text-sm')
                        ui.label('★★★★★').classes('text-yellow-400 text-xs')
                        
            # KOLOM KANAN (Grafik Tipe Kulit)
            with ui.card().classes('flex-1 p-6 shadow-sm'):
                ui.label('Rating per tipe kulit (Serum)').classes('font-bold mb-4')
                # Baris Oily
                with ui.row().classes('w-full items-center justify-between mb-2'):
                    ui.label('Oily').classes('text-sm text-gray-600 w-20')
                    ui.linear_progress(value=0.88, color='pink').classes('w-20') # 4.4 dari 5 = 88%
                    ui.label('4.4').classes('text-sm font-bold')

                with ui.row().classes('w-full items-center justify-between mb-2'):
                    ui.label('Dry').classes('text-sm text-gray-600 w-20')
                    ui.linear_progress(value=0.81, color='pink').classes('w-20') # 4.4 dari 5 = 80%
                    ui.label('4.1').classes('text-sm font-bold')

                with ui.row().classes('w-full items-center justify-between mb-2'):
                    ui.label('Combination').classes('text-sm text-gray-600 w-20')
                    ui.linear_progress(value=0.91, color='pink').classes('w-20') # 4.4 dari 5 = 80%
                    ui.label('4.5').classes('text-sm font-bold')

                with ui.row().classes('w-full items-center justify-between mb-2'):
                    ui.label('Sensitive').classes('text-sm text-gray-600 w-20')
                    ui.linear_progress(value=0.78, color='pink').classes('w-20') # 4.4 dari 5 = 80%
                    ui.label('3.7').classes('text-sm font-bold')

                with ui.row().classes('w-full items-center justify-between mb-2'):
                    ui.label('Normal').classes('text-sm text-gray-600 w-20')
                    ui.linear_progress(value=0.85, color='pink').classes('w-20') # 4.4 dari 5 = 80%
                    ui.label('4.3').classes('text-sm font-bold')

