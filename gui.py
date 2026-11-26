"""
PDF to JPG Converter - GUI Version
====================================
Antarmuka grafis untuk mengubah file PDF menjadi gambar JPG.

Penggunaan:
    python gui.py
"""

import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from converter import pdf_to_jpg  # noqa: E402


class PDFtoJPGApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PDF to JPG Converter")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Variabel
        self.pdf_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.dpi = tk.IntVar(value=200)
        self.quality = tk.IntVar(value=90)
        self.is_converting = False

        self._build_ui()

    def _build_ui(self):
        # Style
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Info.TLabel", font=("Segoe UI", 9))

        # Main frame
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill=tk.BOTH, expand=True)

        # Judul
        ttk.Label(main, text="📄 PDF to JPG Converter", style="Title.TLabel").pack(
            pady=(0, 15)
        )

        # === File PDF ===
        frame_pdf = ttk.LabelFrame(main, text="File PDF", padding=10)
        frame_pdf.pack(fill=tk.X, pady=(0, 10))

        row_pdf = ttk.Frame(frame_pdf)
        row_pdf.pack(fill=tk.X)

        ttk.Entry(row_pdf, textvariable=self.pdf_path, state="readonly").pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10)
        )
        ttk.Button(row_pdf, text="Pilih PDF...", command=self._browse_pdf).pack(
            side=tk.RIGHT
        )

        # === Output ===
        frame_out = ttk.LabelFrame(main, text="Folder Output (opsional)", padding=10)
        frame_out.pack(fill=tk.X, pady=(0, 10))

        row_out = ttk.Frame(frame_out)
        row_out.pack(fill=tk.X)

        ttk.Entry(row_out, textvariable=self.output_dir, state="readonly").pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10)
        )
        ttk.Button(row_out, text="Pilih Folder...", command=self._browse_output).pack(
            side=tk.RIGHT
        )

        # === Pengaturan ===
        frame_settings = ttk.LabelFrame(main, text="Pengaturan", padding=10)
        frame_settings.pack(fill=tk.X, pady=(0, 10))

        # DPI
        row_dpi = ttk.Frame(frame_settings)
        row_dpi.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(row_dpi, text="Resolusi (DPI):").pack(side=tk.LEFT)
        ttk.Label(row_dpi, textvariable=self.dpi, width=5).pack(side=tk.RIGHT)
        ttk.Scale(
            row_dpi, from_=72, to=600, variable=self.dpi, orient=tk.HORIZONTAL
        ).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=10)

        # Kualitas
        row_quality = ttk.Frame(frame_settings)
        row_quality.pack(fill=tk.X)

        ttk.Label(row_quality, text="Kualitas JPG:").pack(side=tk.LEFT)
        ttk.Label(row_quality, textvariable=self.quality, width=5).pack(side=tk.RIGHT)
        ttk.Scale(
            row_quality,
            from_=10,
            to=100,
            variable=self.quality,
            orient=tk.HORIZONTAL,
        ).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=10)

        # === Progress ===
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main, variable=self.progress_var, maximum=100
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))

        self.status_label = ttk.Label(main, text="Siap", style="Info.TLabel")
        self.status_label.pack()

        # === Tombol Konversi ===
        self.convert_btn = ttk.Button(
            main, text="🚀 Konversi Sekarang!", command=self._start_conversion
        )
        self.convert_btn.pack(pady=(10, 0), ipadx=20, ipady=5)

    def _browse_pdf(self):
        path = filedialog.askopenfilename(
            title="Pilih File PDF",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")],
        )
        if path:
            self.pdf_path.set(path)

    def _browse_output(self):
        path = filedialog.askdirectory(title="Pilih Folder Output")
        if path:
            self.output_dir.set(path)

    def _start_conversion(self):
        if self.is_converting:
            return

        pdf = self.pdf_path.get()
        if not pdf:
            messagebox.showwarning("Peringatan", "Silakan pilih file PDF terlebih dahulu!")
            return

        if not Path(pdf).exists():
            messagebox.showerror("Error", "File PDF tidak ditemukan!")
            return

        self.is_converting = True
        self.convert_btn.configure(state="disabled")
        self.progress_var.set(0)
        self.status_label.configure(text="Mengkonversi...")

        # Jalankan konversi di thread terpisah agar GUI tidak freeze
        thread = threading.Thread(target=self._do_conversion, daemon=True)
        thread.start()

    def _do_conversion(self):
        try:
            output = self.output_dir.get() or None
            results = pdf_to_jpg(
                pdf_path=self.pdf_path.get(),
                output_dir=output,
                dpi=self.dpi.get(),
                quality=self.quality.get(),
            )

            self.root.after(0, self._on_success, results)

        except Exception as e:
            self.root.after(0, self._on_error, str(e))

    def _on_success(self, results: list[str]):
        self.progress_var.set(100)
        self.is_converting = False
        self.convert_btn.configure(state="normal")

        output_folder = Path(results[0]).parent
        self.status_label.configure(text=f"✅ {len(results)} gambar disimpan!")

        answer = messagebox.askyesno(
            "Selesai!",
            f"Berhasil mengkonversi {len(results)} halaman!\n\n"
            f"Lokasi: {output_folder}\n\n"
            f"Buka folder output?",
        )
        if answer:
            import os
            os.startfile(str(output_folder))

    def _on_error(self, error_msg: str):
        self.progress_var.set(0)
        self.is_converting = False
        self.convert_btn.configure(state="normal")
        self.status_label.configure(text="❌ Gagal")
        messagebox.showerror("Error", f"Konversi gagal:\n{error_msg}")


def main():
    root = tk.Tk()
    app = PDFtoJPGApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
