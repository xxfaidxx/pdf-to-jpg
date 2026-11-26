"""
PDF to JPG Converter
====================
Mengubah file PDF menjadi gambar JPG per halaman.

Penggunaan:
    python converter.py <file.pdf>                  # Konversi semua halaman
    python converter.py <file.pdf> --pages 1 3 5    # Konversi halaman tertentu
    python converter.py <file.pdf> --dpi 300        # Atur resolusi (default: 200)
    python converter.py <file.pdf> --quality 95     # Atur kualitas JPG (default: 90)
    python converter.py <file.pdf> --output folder  # Simpan ke folder tertentu
"""

import argparse
import sys
from pathlib import Path

import pymupdf
from PIL import Image


def pdf_to_jpg(
    pdf_path: str,
    output_dir: str | None = None,
    dpi: int = 200,
    quality: int = 90,
    pages: list[int] | None = None,
) -> list[str]:
    """
    Konversi file PDF menjadi gambar JPG.

    Args:
        pdf_path: Path ke file PDF.
        output_dir: Direktori output. Default: folder yang sama dengan PDF.
        dpi: Resolusi gambar (dots per inch). Default: 200.
        quality: Kualitas JPG (1-100). Default: 90.
        pages: List nomor halaman (1-based). None = semua halaman.

    Returns:
        List path file JPG yang dihasilkan.
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {pdf_path}")

    if not pdf_path.suffix.lower() == ".pdf":
        raise ValueError(f"File bukan PDF: {pdf_path}")

    # Tentukan direktori output
    if output_dir:
        out_dir = Path(output_dir)
    else:
        out_dir = Path(__file__).parent / "hasil konversi"

    out_dir.mkdir(parents=True, exist_ok=True)

    # Buka PDF
    doc = pymupdf.open(str(pdf_path))
    total_pages = len(doc)

    # Tentukan halaman yang akan dikonversi
    if pages:
        page_indices = [p - 1 for p in pages if 1 <= p <= total_pages]
        if not page_indices:
            raise ValueError(
                f"Halaman tidak valid. PDF memiliki {total_pages} halaman."
            )
    else:
        page_indices = range(total_pages)

    # Hitung zoom factor dari DPI (default PDF = 72 DPI)
    zoom = dpi / 72
    matrix = pymupdf.Matrix(zoom, zoom)

    output_files = []

    for i, page_idx in enumerate(page_indices):
        page = doc[page_idx]
        page_num = page_idx + 1

        # Render halaman ke pixmap
        pix = page.get_pixmap(matrix=matrix)

        # Konversi ke PIL Image
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

        # Simpan sebagai JPG
        filename = f"{pdf_path.stem}_halaman_{page_num:03d}.jpg"
        output_path = out_dir / filename
        img.save(str(output_path), "JPEG", quality=quality)

        output_files.append(str(output_path))

        # Progress
        progress = (i + 1) / len(page_indices) * 100
        print(f"  [{progress:5.1f}%] Halaman {page_num}/{total_pages} -> {filename}")

    doc.close()

    return output_files


def main():
    parser = argparse.ArgumentParser(
        description="Konversi file PDF menjadi gambar JPG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  python converter.py dokumen.pdf
  python converter.py dokumen.pdf --dpi 300 --quality 95
  python converter.py dokumen.pdf --pages 1 2 3
  python converter.py dokumen.pdf --output hasil/
        """,
    )

    parser.add_argument("pdf", help="Path ke file PDF yang akan dikonversi")
    parser.add_argument(
        "--output", "-o", help="Direktori output (default: <nama_pdf>_jpg/)"
    )
    parser.add_argument(
        "--dpi",
        "-d",
        type=int,
        default=200,
        help="Resolusi gambar dalam DPI (default: 200)",
    )
    parser.add_argument(
        "--quality",
        "-q",
        type=int,
        default=90,
        help="Kualitas JPG, 1-100 (default: 90)",
    )
    parser.add_argument(
        "--pages",
        "-p",
        type=int,
        nargs="+",
        help="Nomor halaman yang akan dikonversi (default: semua)",
    )

    args = parser.parse_args()

    # Validasi parameter
    if not 1 <= args.quality <= 100:
        print("Error: Kualitas harus antara 1-100")
        sys.exit(1)

    if args.dpi < 72:
        print("Error: DPI minimal 72")
        sys.exit(1)

    print(f"📄 Mengkonversi: {args.pdf}")
    print(f"   DPI: {args.dpi} | Kualitas: {args.quality}")

    if args.pages:
        print(f"   Halaman: {args.pages}")

    print()

    try:
        results = pdf_to_jpg(
            pdf_path=args.pdf,
            output_dir=args.output,
            dpi=args.dpi,
            quality=args.quality,
            pages=args.pages,
        )

        print(f"\n✅ Selesai! {len(results)} gambar disimpan.")
        print(f"📁 Lokasi: {Path(results[0]).parent}")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error tidak terduga: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
