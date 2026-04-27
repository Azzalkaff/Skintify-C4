from nicegui import ui
from app.context import data_mgr, state
from app.ui.components import UIComponents
from app.auth.auth import AuthManager

def show_page():
    """MISI SYAQILA: Membuat Galeri Wishlist"""
    
    # --- JANGAN DIUBAH (Wajib untuk Navigasi) ---
    auth_redirect = AuthManager.require_auth()
    if auth_redirect: return auth_redirect
    UIComponents.navbar()
    UIComponents.sidebar()
    # -------------------------------------------

    # --- 🚀 MULAI KERJAKAN DI SINI (AREA BELAJAR SYAQILA) ---
    
    # Data produk wishlist (nanti bisa diganti dari data_mgr)
    wishlist_products = [
        {
            'name': 'Niacinamide 10% + Zinc 1%',
            'brand': 'The Ordinary',
            'category': 'Serum',
            'price': 'Rp145.000',
            'rating': '4.9',
            'icon': '💧',
            'bg_color': 'bg-blue-50',
        },
        {
            'name': 'UV Shield SPF50+ PA++++',
            'brand': 'Skin Aqua',
            'category': 'Sunscreen',
            'price': 'Rp78.000',
            'rating': '4.7',
            'icon': '☀️',
            'bg_color': 'bg-orange-50',
        },
        {
            'name': 'Hydrating Toner pH 5.5',
            'brand': 'Emina',
            'category': 'Toner',
            'price': 'Rp52.000',
            'rating': '4.5',
            'icon': '🌊',
            'bg_color': 'bg-sky-50',
        },
    ]
    
    def hapus_produk(product_name: str):
        """Handler untuk tombol Hapus"""
        ui.notify(f'Produk "{product_name}" dihapus dari wishlist', type='warning')
        # TODO: panggil data_mgr untuk update wishlist asli
    
    # Container utama dengan background soft
    with ui.column().classes('w-full p-8 bg-rose-50/30 min-h-screen gap-4'):
        
        # Header: Judul + Badge Tipe Kulit
        with ui.row().classes('w-full items-center justify-between pb-2 border-b border-gray-200'):
            ui.label('Wishlist').classes('text-2xl font-bold text-gray-800')
            with ui.element('div').classes('bg-pink-100 px-4 py-1.5 rounded-full'):
                ui.label('Kulit: Oily').classes('text-pink-600 text-sm font-medium')
        
        # Sub-header: jumlah produk
        ui.label(f'{len(wishlist_products)} PRODUK TERSIMPAN').classes(
            'text-xs font-semibold text-gray-500 tracking-wider mt-2'
        )
        
        # Grid daftar produk
        with ui.grid(columns=1).classes('w-full gap-3'):
            for product in wishlist_products:
                with ui.card().classes(
                    'w-full p-4 rounded-xl shadow-none border border-gray-100 '
                    'hover:shadow-md transition-shadow bg-white'
                ):
                    with ui.row().classes('w-full items-center justify-between no-wrap'):
                        
                        # KIRI: Icon + Info Produk
                        with ui.row().classes('items-center gap-4 no-wrap flex-1'):
                            # Icon box
                            with ui.element('div').classes(
                                f'{product["bg_color"]} w-14 h-14 rounded-xl '
                                'flex items-center justify-center text-2xl'
                            ):
                                ui.label(product['icon']).classes('text-2xl')
                            
                            # Nama + brand
                            with ui.column().classes('gap-0'):
                                ui.label(product['name']).classes(
                                    'text-base font-bold text-gray-800'
                                )
                                ui.label(
                                    f'{product["brand"]} · {product["category"]}'
                                ).classes('text-sm text-gray-500')
                        
                        # TENGAH: Harga + Rating
                        with ui.column().classes('items-end gap-0 mr-4'):
                            ui.label(product['price']).classes(
                                'text-base font-bold text-pink-500'
                            )
                            ui.label(f'★ {product["rating"]}').classes(
                                'text-sm text-yellow-500 font-medium'
                            )
                        
                        # KANAN: Tombol Hapus
                        ui.button(
                            'Hapus',
                            on_click=lambda p=product: hapus_produk(p['name'])
                        ).props('outline no-caps').classes(
                            'text-pink-500 border-pink-300 rounded-lg px-6'
                        )

