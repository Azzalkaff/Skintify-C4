from nicegui import ui

# 💡 CHEAT SHEET: CONTOH KOMPONEN UNTUK REKAN TIM
# Gunakan file ini sebagai referensi (copy-paste) ke halaman kalian!

def contoh_semua_komponen():
    # 1. Judul & Teks
    ui.label('Ini Judul Besar').classes('text-3xl font-black text-pink-600')
    ui.label('Ini teks keterangan kecil').classes('text-gray-400')

    # 2. Tombol (Button)
    ui.button('Klik Saya', on_click=lambda: ui.notify('Tombol diklik!'))
    ui.button('Tombol Mewah', icon='favorite').classes('btn-primary')

    # 3. Kotak Input (Input & Select)
    nama = ui.input(label='Masukkan Nama')
    tipe = ui.select(['Kering', 'Berminyak'], label='Pilih Tipe Kulit')

    # 4. Kotak/Panel (Card)
    with ui.card().classes('glass-card p-6'):
        ui.label('Teks di dalam kotak transparan')
        ui.icon('info', size='24px')

    # 5. Baris & Kolom (Layout)
    with ui.row().classes('gap-4 items-center'):
        ui.label('Kiri')
        ui.label('Tengah')
        ui.label('Kanan')

    with ui.column().classes('w-full items-center'):
        ui.label('Atas')
        ui.label('Bawah')

    # 6. Menampilkan Data Produk (Looping)
    daftar_contoh = [{'nama': 'Produk 1'}, {'nama': 'Produk 2'}]
    for item in daftar_contoh:
        ui.label(item['nama'])
