import sqlite3

class BasisData:
    """Manajer Database SQLite sederhana untuk pemula (Separation of Concerns)."""
    
    DB_NAMA = "data_skintify.db"

    @staticmethod
    def inisialisasi():
        """Membuat file database dan tabel jika belum ada."""
        with sqlite3.connect(BasisData.DB_NAMA) as koneksi:
            kursor = koneksi.cursor()
            # Tabel utama pengguna
            kursor.execute('''
                CREATE TABLE IF NOT EXISTS pengguna (
                    email             TEXT PRIMARY KEY,
                    username          TEXT UNIQUE,
                    password          TEXT NOT NULL,
                    skin_type         TEXT DEFAULT '',
                    avoid_ingredients TEXT DEFAULT '',
                    skin_issues       TEXT DEFAULT ''
                )
            ''')
            # Kalau tabel sudah ada tapi belum punya kolom baru (upgrade DB lama),
            # tambahkan kolomnya satu per satu — tidak akan error kalau sudah ada
            for kolom in ['skin_type', 'avoid_ingredients', 'skin_issues']:
                try:
                    kursor.execute(f"ALTER TABLE pengguna ADD COLUMN {kolom} TEXT DEFAULT ''")
                except Exception:
                    pass  # Kolom sudah ada, lewati
            koneksi.commit()

    @staticmethod
    def cek_identifier_terdaftar(identifier: str) -> bool:
        """Mengembalikan True jika email atau username sudah ada di database."""
        with sqlite3.connect(BasisData.DB_NAMA) as koneksi:
            kursor = koneksi.cursor()
            kursor.execute(
                'SELECT email FROM pengguna WHERE email = ? OR username = ?',
                (identifier, identifier)
            )
            return kursor.fetchone() is not None

    @staticmethod
    def tambah_pengguna(email: str, username: str, password: str) -> bool:
        """Memasukkan pengguna baru ke database permanen."""
        try:
            with sqlite3.connect(BasisData.DB_NAMA) as koneksi:
                kursor = koneksi.cursor()
                kursor.execute(
                    'INSERT INTO pengguna (email, username, password) VALUES (?, ?, ?)',
                    (email, username, password)
                )
                koneksi.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    @staticmethod
    def verifikasi_login(identifier: str, password: str) -> bool:
        """Mengecek apakah kombinasi email/username dan password cocok di database."""
        with sqlite3.connect(BasisData.DB_NAMA) as koneksi:
            kursor = koneksi.cursor()
            kursor.execute(
                'SELECT password FROM pengguna WHERE email = ? OR username = ?',
                (identifier, identifier)
            )
            hasil = kursor.fetchone()
            if hasil and hasil[0] == password:
                return True
            return False

    # ── TAMBAHAN FALISHA ──────────────────────────────────────────────────────

    @staticmethod
    def ambil_pengguna_by_identifier(identifier: str) -> dict:
        """
        Mengambil data lengkap user berdasarkan email atau username.
        Return: dict lengkap atau {} kalau tidak ditemukan.
        """
        with sqlite3.connect(BasisData.DB_NAMA) as koneksi:
            koneksi.row_factory = sqlite3.Row
            kursor = koneksi.cursor()
            kursor.execute(
                '''SELECT email, username, skin_type, avoid_ingredients, skin_issues
                   FROM pengguna WHERE email = ? OR username = ?''',
                (identifier, identifier)
            )
            hasil = kursor.fetchone()
            if hasil:
                # avoid_ingredients dan skin_issues disimpan sebagai string dipisah koma
                # ubah balik ke list saat dibaca
                avoid = [x.strip() for x in hasil['avoid_ingredients'].split(',') if x.strip()]
                issues = [x.strip() for x in hasil['skin_issues'].split(',') if x.strip()]
                return {
                    'email':             hasil['email'],
                    'username':          hasil['username'],
                    'skin_type':         hasil['skin_type'] or '',
                    'avoid_ingredients': avoid,
                    'skin_issues':       issues,
                }
            return {}

    @staticmethod
    def simpan_profil_kulit(email: str, skin_type: str,
                            avoid_ingredients: list, skin_issues: list) -> bool:
        """
        Menyimpan data kulit user ke database.
        Dipanggil oleh onboarding_page setelah user mengisi survey.
        """
        try:
            with sqlite3.connect(BasisData.DB_NAMA) as koneksi:
                kursor = koneksi.cursor()
                kursor.execute(
                    '''UPDATE pengguna
                       SET skin_type = ?, avoid_ingredients = ?, skin_issues = ?
                       WHERE email = ?''',
                    (
                        skin_type,
                        ', '.join(avoid_ingredients),   # list → string
                        ', '.join(skin_issues),         # list → string
                        email
                    )
                )
                koneksi.commit()
            return True
        except Exception as e:
            print(f"[DB] Gagal simpan profil kulit: {e}")
            return False