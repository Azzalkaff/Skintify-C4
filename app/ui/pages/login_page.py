from nicegui import ui, app
import asyncio
from app.auth.auth import AuthManager


def show_page():
    """Antarmuka Login & Daftar dengan State Binding dan Loading Animation."""

    if AuthManager.is_authenticated():
        ui.navigate.to('/')
        return

    # State UI
    state = {
        "mode": "login",   # login | register | otp
        "email": "",
        "username": "",
        "password": "",
        "otp": "",
        "is_loading": False
    }

    # --- ELEMENT LOADING GLOBAL ---
    loading_overlay = ui.column().classes(
        'absolute inset-0 bg-white/70 backdrop-blur-[2px] z-50 flex items-center justify-center'
    ).bind_visibility_from(state, 'is_loading')
    with loading_overlay:
        ui.spinner('dots', size='lg', color='#A84A62')
        ui.label('Mohon tunggu sebentar...').classes('text-[#A84A62] font-bold mt-2 text-sm')

    @ui.refreshable
    def form_kontainer():
        with ui.column().classes(
            'w-[400px] glass-panel rounded-[2rem] p-10 z-10 items-center '
            'shadow-2xl border border-white/40 relative overflow-hidden'
        ):
            ui.icon('auto_awesome', size='48px').style('color: var(--primary);').classes('mb-2')
            ui.label('Skintify').classes('text-3xl font-black text-[#A84A62] tracking-tight')

            # --- TAMPILAN OTP ---
            if state["mode"] == "otp":
                ui.label('Verifikasi Email').classes('text-lg font-bold text-gray-700 mt-4')
                ui.label(f'Masukkan kode yang dikirim ke {state["email"]}').classes(
                    'text-[11px] text-gray-500 mb-2 text-center'
                )
                ui.label('(Lihat kode OTP di terminal/console)').classes(
                    'text-[11px] text-pink-400 mb-6 text-center font-bold'
                )

                ui.input('Kode OTP 6-Digit').bind_value(state, 'otp') \
                    .props('outlined rounded bg-white/70 text-center tracking-[10px] font-bold') \
                    .classes('w-full mb-6')

                with ui.row().classes('w-full gap-2'):
                    ui.button('Verifikasi', on_click=proses_verifikasi) \
                        .classes('flex-1 btn-primary text-white rounded-xl py-3')

                    def batal():
                        state["mode"] = "register"
                        form_kontainer.refresh()

                    ui.button('Batal', on_click=batal).props('flat').classes('text-gray-400')

            # --- TAMPILAN LOGIN / DAFTAR ---
            else:
                with ui.tabs().classes('w-full mb-6 bg-transparent') as tabs:
                    ui.tab('Masuk')
                    ui.tab('Daftar')

                def ganti_tab(e):
                    mode_baru = "login" if e.value == "Masuk" else "register"
                    if state["mode"] != mode_baru:
                        state["mode"] = mode_baru
                        form_kontainer.refresh()

                tabs.on_value_change(ganti_tab)
                tabs.set_value('Masuk' if state["mode"] == "login" else 'Daftar')

                if state["mode"] == "register":
                    ui.input('Username').bind_value(state, 'username') \
                        .props('outlined rounded bg-white/70').classes('w-full mb-4')
                    ui.input('Email').bind_value(state, 'email') \
                        .props('outlined rounded bg-white/70').classes('w-full mb-4')
                else:
                    ui.input('Username / Email').bind_value(state, 'email') \
                        .props('outlined rounded bg-white/70').classes('w-full mb-4')

                ui.input('Password', password=True, password_toggle_button=True) \
                    .bind_value(state, 'password') \
                    .props('outlined rounded bg-white/70').classes('w-full mb-6')

                if state["mode"] == "login":
                    ui.button('Masuk Aplikasi', on_click=proses_login) \
                        .classes('w-full btn-primary text-white rounded-xl py-3 shadow-lg')
                else:
                    ui.button('Daftar & Kirim OTP', on_click=proses_daftar) \
                        .classes('w-full btn-primary text-white rounded-xl py-3 shadow-lg')

    # --- LOGIKA AKSI ---

    async def proses_login():
        """Login → ambil username dari DB → langsung ke Home."""
        state["is_loading"] = True
        success, message = await AuthManager.login(state["email"], state["password"])

        if success:
            # Setelah login, muat SELURUH profil dari DB ke storage sekaligus.
            # Ini mencegah redirect ke onboarding karena skin_type sudah tersedia.
            try:
                from main import muat_profil_ke_storage
                muat_profil_ke_storage(state["email"])
            except Exception as e:
                print(f'[login] Gagal muat profil dari DB: {e}')
            ui.navigate.to("/")
        else:
            ui.notify(message, color="negative")
        state["is_loading"] = False

    async def proses_daftar():
        """Daftar → kirim OTP → tampilkan form OTP."""
        if not state["username"]:
            ui.notify('Username wajib diisi!', color='warning')
            return
        if not state["email"] or "@" not in state["email"]:
            ui.notify('Masukkan alamat email yang valid!', color='warning')
            return
        if len(state["password"]) < 6:
            ui.notify('Password minimal 6 karakter!', color='warning')
            return

        state["is_loading"] = True
        success, message = await AuthManager.kirim_otp_pendaftaran(
            state["email"], state["username"], state["password"]
        )
        state["is_loading"] = False

        if success:
            ui.notify(message, color='positive')
            state["mode"] = "otp"
            form_kontainer.refresh()
        else:
            ui.notify(message, color='warning')

    async def proses_verifikasi():
        """Verifikasi OTP → simpan username ke storage → ke Onboarding (BUKAN login)."""
        state["is_loading"] = True
        success, message = await AuthManager.verifikasi_dan_daftar(state["email"], state["otp"])
        state["is_loading"] = False

        if success:
            ui.notify(message, color='positive')

            # ── Langsung login otomatis setelah daftar berhasil ──────────────
            # Tidak perlu input password lagi — langsung set storage
            app.storage.user['authenticated'] = True
            app.storage.user['email']         = state["email"]
            app.storage.user['username']      = state["username"]

            # ── ALUR DAFTAR: setelah OTP → Onboarding (bukan Home) ──────────
            # Pastikan mode onboarding bukan 'edit' (ini user baru)
            app.storage.user['onboarding_mode'] = None

            ui.navigate.to('/onboarding')   # ← PERBEDAAN UTAMA dari login biasa
        else:
            ui.notify(message, color='negative')

    # Layout Utama Halaman
    with ui.column().classes('w-full h-screen items-center justify-center relative bg-[#F9F5F6]'):
        form_kontainer()