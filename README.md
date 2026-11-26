# 📄 PDF to JPG Converter

Aplikasi Python untuk mengubah file PDF menjadi gambar JPG, tersedia dalam versi **Command Line (CLI)** dan **GUI (Graphical User Interface)**.

## ✨ Fitur

- Konversi semua halaman PDF ke JPG
- Pilih halaman tertentu untuk dikonversi
- Atur resolusi (DPI) dan kualitas gambar
- Versi CLI dan GUI
- Tidak butuh instalasi Poppler (menggunakan PyMuPDF)

## 📦 Instalasi

```bash
# Install dependencies
pip install -r requirements.txt
```

## 🚀 Penggunaan

### Versi CLI (Command Line)

```bash
# Konversi semua halaman
python converter.py dokumen.pdf

# Atur resolusi tinggi (300 DPI) dan kualitas maksimal
python converter.py dokumen.pdf --dpi 300 --quality 95

# Konversi halaman tertentu saja
python converter.py dokumen.pdf --pages 1 3 5

# Simpan ke folder tertentu
python converter.py dokumen.pdf --output hasil/
```

**Parameter:**

| Parameter       | Singkat | Default | Keterangan                        |
|-----------------|---------|---------|-----------------------------------|
| `pdf`           | -       | -       | Path file PDF (wajib)             |
| `--output`      | `-o`    | auto    | Folder output                     |
| `--dpi`         | `-d`    | 200     | Resolusi gambar (72-600)          |
| `--quality`     | `-q`    | 90      | Kualitas JPG (1-100)              |
| `--pages`       | `-p`    | semua   | Nomor halaman yang dikonversi     |

### Versi GUI

```bash
python gui.py
```

Akan muncul jendela aplikasi dengan fitur:
- Pilih file PDF
- Pilih folder output
- Atur DPI dan kualitas via slider
- Tombol konversi dengan progress bar

## 📁 Struktur Project

```
pdf to jpg/
├── converter.py       # Modul utama & CLI
├── gui.py             # Antarmuka grafis (GUI)
├── requirements.txt   # Dependencies
└── README.md          # Dokumentasi
```

## 🛠️ Dependencies

- **PyMuPDF** - Membaca dan merender halaman PDF
- **Pillow** - Menyimpan gambar dalam format JPG
