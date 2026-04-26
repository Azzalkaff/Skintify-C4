"""
lihat_hasil.py — Tampilkan hasil scraping multi-platform dari database.
Jalankan: python lihat_hasil.py
"""

from database import SessionLocal, init_db
from models import Toko, Produk, HasilPencarian, SociollaReferensi
from sqlalchemy import func


def tampilkan_ringkasan():
    init_db()
    with SessionLocal() as s:

        # ── Statistik Global ──────────────────────────────────────────────────
        total_toko_tokopedia = (
            s.query(func.count(Toko.id)).filter_by(platform="tokopedia").scalar()
        )
        total_toko_lazada = (
            s.query(func.count(Toko.id)).filter_by(platform="lazada").scalar()
        )
        total_produk_tokopedia = (
            s.query(func.count(Produk.id)).filter_by(platform="tokopedia").scalar()
        )
        total_produk_lazada = (
            s.query(func.count(Produk.id)).filter_by(platform="lazada").scalar()
        )
        total_referensi = s.query(func.count(SociollaReferensi.id)).scalar()
        sudah_scrape    = (
            s.query(func.count(SociollaReferensi.id))
            .filter_by(sudah_di_scrape=True)
            .scalar()
        )

        print("\n" + "=" * 65)
        print("  Multi-Platform Price Scraper — Ringkasan Database")
        print("=" * 65)

        print(f"\n  Referensi Sociolla : {total_referensi} produk "
              f"({sudah_scrape} sudah di-scrape)")

        print(f"\n  {'Platform':<15} {'Toko':>8} {'Produk':>10}")
        print(f"  {'-'*15} {'-'*8} {'-'*10}")
        print(f"  {'Tokopedia':<15} {total_toko_tokopedia:>8} {total_produk_tokopedia:>10}")
        print(f"  {'Lazada':<15} {total_toko_lazada:>8} {total_produk_lazada:>10}")
        print(f"  {'TOTAL':<15} {total_toko_tokopedia+total_toko_lazada:>8} "
              f"{total_produk_tokopedia+total_produk_lazada:>10}")

        # ── Riwayat Pencarian ─────────────────────────────────────────────────
        sesi_list = (
            s.query(HasilPencarian)
            .order_by(HasilPencarian.dicari_pada.desc())
            .limit(30)
            .all()
        )

        if sesi_list:
            print(f"\n  Riwayat Pencarian Terakhir (30):")
            print(f"  {'Platform':<12} {'Keyword':<38} {'Produk':>7} {'Toko':>5} {'Waktu'}")
            print(f"  {'-'*12} {'-'*38} {'-'*7} {'-'*5} {'-'*16}")
            for ses in sesi_list:
                kw = ses.keyword[:36] + ".." if len(ses.keyword) > 38 else ses.keyword
                print(
                    f"  {ses.platform:<12} "
                    f"{kw:<38} "
                    f"{ses.jumlah_produk:>7} "
                    f"{ses.jumlah_toko:>5}  "
                    f"{ses.dicari_pada.strftime('%m-%d %H:%M')}"
                )

        # ── Perbandingan Harga Per Keyword ────────────────────────────────────
        # Ambil keyword unik yang punya data di KEDUA platform
        keywords_tokopedia = {
            r[0] for r in s.query(Produk.keyword).filter_by(platform="tokopedia").distinct()
        }
        keywords_lazada = {
            r[0] for r in s.query(Produk.keyword).filter_by(platform="lazada").distinct()
        }
        keywords_berdua = keywords_tokopedia & keywords_lazada

        if keywords_berdua:
            print(f"\n  Perbandingan Harga (keyword ada di kedua platform): "
                  f"{len(keywords_berdua)} keyword")
            print(f"\n  {'Keyword':<38} {'Toko':<22} {'Harga Min':>12} {'Platform':<12}")
            print(f"  {'-'*38} {'-'*22} {'-'*12} {'-'*12}")

            for kw in sorted(keywords_berdua)[:10]:    # tampilkan 10 pertama
                for platform in ["tokopedia", "lazada"]:
                    produk_termurah = (
                        s.query(Produk)
                        .join(Toko)
                        .filter(Produk.platform == platform, Produk.keyword == kw)
                        .filter(Produk.harga > 0)
                        .order_by(Produk.harga.asc())
                        .first()
                    )
                    if produk_termurah:
                        kw_display = kw[:36] + ".." if len(kw) > 38 else kw
                        toko_nama  = (produk_termurah.toko.nama[:20]
                                      if produk_termurah.toko else "-")
                        print(
                            f"  {kw_display:<38} "
                            f"{toko_nama:<22} "
                            f"Rp{produk_termurah.harga:>10,.0f} "
                            f"{platform:<12}"
                        )

        # ── Produk Sociolla yang Belum Di-scrape ──────────────────────────────
        belum = (
            s.query(SociollaReferensi)
            .filter_by(sudah_di_scrape=False)
            .all()
        )
        if belum:
            print(f"\n  ⚠️  Produk Sociolla belum di-scrape: {len(belum)}")
            for ref in belum[:5]:
                print(f"     - {ref.brand} — {ref.product_name[:50]}")
            if len(belum) > 5:
                print(f"     ... dan {len(belum) - 5} lainnya")

        print()


if __name__ == "__main__":
    tampilkan_ringkasan()