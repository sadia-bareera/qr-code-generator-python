import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageTk


def build_qr(data, size=280, fill="#000000", back="#ffffff", logo_path=None):
    """Return a PIL image of the QR code (optionally with a logo in the middle)."""
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill, back_color=back).convert("RGB")
    img = img.resize((size, size), Image.LANCZOS)

    if logo_path:
        logo = Image.open(logo_path).convert("RGBA")
        logo_size = int(size * 0.22)
        logo.thumbnail((logo_size, logo_size), Image.LANCZOS)
        pad = 6
        box = Image.new("RGB", (logo.width + pad * 2, logo.height + pad * 2), back)
        pos = ((size - box.width) // 2, (size - box.height) // 2)
        img.paste(box, pos)
        img.paste(logo, (pos[0] + pad, pos[1] + pad), logo)
    return img


class QRApp:
    def __init__(self, root):
        self.root = root
        root.title("QR Code Generator")
        root.geometry("520x840")

        self.qr_img = None
        self.fill = "#000000"
        self.back = "#ffffff"
        self.logo_path = None

        tk.Label(root, text="QR Code App", font=("Arial", 16, "bold")).pack(pady=12)

        self.entry = tk.Entry(root, width=40, font=("Arial", 12))
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda e: self.generate())

        # colors
        row = tk.Frame(root)
        row.pack(pady=8)
        self.btn_fill = tk.Button(row, text="QR color", width=12,
                                  command=self.pick_fill)
        self.btn_fill.grid(row=0, column=0, padx=5)
        self.btn_back = tk.Button(row, text="Background", width=12,
                                  command=self.pick_back)
        self.btn_back.grid(row=0, column=1, padx=5)

        # size slider
        tk.Label(root, text="Size (pixels)").pack()
        self.size_var = tk.IntVar(value=280)
        tk.Scale(root, from_=150, to=400, orient="horizontal", length=260,
                 variable=self.size_var).pack()

        # logo
        row2 = tk.Frame(root)
        row2.pack(pady=8)
        tk.Button(row2, text="Add logo", width=12, command=self.pick_logo).grid(
            row=0, column=0, padx=5)
        tk.Button(row2, text="Remove logo", width=12, command=self.clear_logo).grid(
            row=0, column=1, padx=5)
        self.lbl_logo = tk.Label(root, text="No logo", fg="gray")
        self.lbl_logo.pack()

        tk.Button(root, text="Generate QR", bg="#2f7de1", fg="white",
                  width=20, command=self.generate).pack(pady=10)

        self.lbl_qr = tk.Label(root, text="Your QR will appear here",
                               bg="#e0e0e0", width=36, height=12)
        self.lbl_qr.pack(pady=8)

        tk.Button(root, text="Save as PNG", width=20, command=self.save).pack(pady=5)

    def pick_fill(self):
        c = colorchooser.askcolor(color=self.fill, title="QR color")[1]
        if c:
            self.fill = c
            self.btn_fill.config(bg=c, fg=self._text_on(c))

    def pick_back(self):
        c = colorchooser.askcolor(color=self.back, title="Background color")[1]
        if c:
            self.back = c
            self.btn_back.config(bg=c, fg=self._text_on(c))

    @staticmethod
    def _text_on(hex_color):
        r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
        return "black" if (r * 299 + g * 587 + b * 114) / 1000 > 128 else "white"

    def pick_logo(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if path:
            self.logo_path = path
            self.lbl_logo.config(text=path.split("/")[-1].split("\\")[-1], fg="black")

    def clear_logo(self):
        self.logo_path = None
        self.lbl_logo.config(text="No logo", fg="gray")

    def generate(self):
        data = self.entry.get().strip()
        if not data:
            messagebox.showwarning("Empty", "Please type some text or a link first.")
            return
        if self.fill.lower() == self.back.lower():
            messagebox.showwarning("Colors", "QR color and background are the same.")
            return
        try:
            self.qr_img = build_qr(data, self.size_var.get(), self.fill,
                                   self.back, self.logo_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate QR:\n{e}")
            return
        photo = ImageTk.PhotoImage(self.qr_img)
        s = self.size_var.get()
        self.lbl_qr.config(image=photo, text="", width=s, height=s)
        self.lbl_qr.image = photo  # keeps the image from vanishing

    def save(self):
        if self.qr_img is None:
            messagebox.showwarning("Nothing to save", "Generate a QR code first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG image", "*.png")])
        if path:
            self.qr_img.save(path)
            messagebox.showinfo("Saved", "QR code saved!")


if __name__ == "__main__":
    root = tk.Tk()
    QRApp(root)
    root.mainloop()
