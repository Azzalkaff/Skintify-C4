"""
models.py — SQLAlchemy ORM Models
Mendukung multi-platform: Tokopedia & Lazada
"""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Text,
    DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Toko(Base):
    __tablename__ = "toko"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    platform    = Column(String(20), nullable=False)          # 'tokopedia' | 'lazada'
    shop_id     = Column(String(100), nullable=False)         # seller_id / shop_id
    nama        = Column(String(255))
    kota        = Column(String(100))
    tier        = Column(Integer, nullable=True)               # Tokopedia: 0/1/2, Lazada: None
    is_official = Column(Boolean, default=False)              # official store / LazMall
    url         = Column(String(500), nullable=True)
    dibuat_pada = Column(DateTime, default=datetime.utcnow)

    produk = relationship("Produk", back_populates="toko", cascade="all, delete-orphan")

    # Unique per platform — shop_id bisa sama nilainya antar platform (collision)
    __table_args__ = (
        UniqueConstraint("platform", "shop_id", name="uq_toko_platform_shopid"),
    )

    def __repr__(self):
        return f"<Toko [{self.platform}] {self.nama} ({self.shop_id})>"


class Produk(Base):
    __tablename__ = "produk"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    platform            = Column(String(20), nullable=False)  # 'tokopedia' | 'lazada'
    product_id          = Column(String(100), nullable=False) # item_id / product_id
    keyword             = Column(String(500), nullable=False)
    nama                = Column(String(500))
    url                 = Column(String(500))
    gambar              = Column(String(500))

    # ── Harga ────────────────────────────────────────────────────────────────
    harga               = Column(Float)
    harga_teks          = Column(String(100))
    harga_asli          = Column(Float)          # harga sebelum diskon
    diskon_persen       = Column(Integer)

    # ── Performa ─────────────────────────────────────────────────────────────
    rating              = Column(Float)
    jumlah_review       = Column(Integer, default=0)
    terjual             = Column(Integer, default=0)  # Lazada: sold count

    # ── Metadata Tokopedia ───────────────────────────────────────────────────
    kategori            = Column(String(255), nullable=True)
    label_badge         = Column(String(255), nullable=True)  # "Mall", "Power Merchant"
    free_ongkir         = Column(Integer, nullable=True)      # 1=ada, 0=tidak (Tokopedia)

    # ── Metadata Lazada ──────────────────────────────────────────────────────
    in_stock            = Column(Boolean, nullable=True)
    is_sponsored        = Column(Boolean, nullable=True)

    dibuat_pada         = Column(DateTime, default=datetime.utcnow)

    toko_id = Column(Integer, ForeignKey("toko.id"))
    toko    = relationship("Toko", back_populates="produk")

    # Unique per platform + product_id + keyword
    __table_args__ = (
        UniqueConstraint("platform", "product_id", "keyword", name="uq_produk_platform_keyword"),
    )

    def __repr__(self):
        return f"<Produk [{self.platform}] {self.nama[:40]}... Rp{self.harga:,.0f}>"


class SociollaReferensi(Base):
    """Menyimpan produk Sociolla sebagai referensi sumber keyword."""
    __tablename__ = "sociolla_referensi"

    id                      = Column(Integer, primary_key=True, autoincrement=True)
    product_name            = Column(String(500), nullable=False)
    brand                   = Column(String(255), nullable=False)
    keyword_digunakan       = Column(String(500))   # keyword yang dikirim ke scraper
    category                = Column(String(255))
    min_price               = Column(Float)
    max_price               = Column(Float)
    harga_setelah_diskon    = Column(Float, nullable=True)
    diskon                  = Column(String(20), nullable=True)
    rating_sociolla         = Column(Float, default=0)
    total_reviews           = Column(Integer, default=0)
    url_sociolla            = Column(String(500))
    is_in_stock             = Column(Boolean, default=True)
    sudah_di_scrape         = Column(Boolean, default=False)
    dibuat_pada             = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("brand", "product_name", name="uq_sociolla_brand_product"),
    )

    def __repr__(self):
        return f"<SociollaReferensi {self.brand} — {self.product_name[:40]}>"


class HasilPencarian(Base):
    """Menyimpan metadata tiap sesi pencarian per platform."""
    __tablename__ = "hasil_pencarian"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    platform        = Column(String(20), nullable=False)  # 'tokopedia' | 'lazada'
    keyword         = Column(String(500), nullable=False)
    total_data      = Column(Integer)      # total produk di marketplace untuk keyword ini
    jumlah_produk   = Column(Integer)      # produk yang berhasil diambil
    jumlah_toko     = Column(Integer)      # toko unik yang ditemukan
    dicari_pada     = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Pencarian [{self.platform}] '{self.keyword}' — {self.jumlah_produk} produk>"