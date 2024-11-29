import sqlite3
from tkinter import Tk, Label, Entry, Button, ttk, messagebox, Frame
from tkinter.font import Font


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Perpustakaan Modern")
        self.root.geometry("1000x600")
        self.root.configure(bg="#e8f4f8")

        # Database
        self.conn = sqlite3.connect("library.db")
        self.create_table()

        # Atribut
        self.selected_id = None

        # Font Desain
        self.header_font = Font(family="Arial", size=16, weight="bold")
        self.label_font = Font(family="Arial", size=12)

        # GUI Components
        self.create_widgets()

    def create_table(self):
        with self.conn:
            self.conn.execute(
                """CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER,
                    category TEXT
                )"""
            )

    def create_widgets(self):
        # Header
        Label(
            self.root, text="Aplikasi Daftar Kehadiran Siswa", font=self.header_font, bg="#e8f4f8", fg="#3a7bd5"
        ).pack(pady=20)

# Tabel untuk Menampilkan Data
        table_frame = Frame(self.root, bg="#e8f4f8")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("id", "title", "author", "year", "category"), show="headings")
        self.tree.heading("id", text="No")
        self.tree.heading("title", text="Nama Siswa")
        self.tree.heading("author", text="Kelas")
        self.tree.heading("year", text="Nomer absen")
        self.tree.heading("category", text="Absensi")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("title", width=250)
        self.tree.column("author", width=150)
        self.tree.column("year", width=100, anchor="center")
        self.tree.column("category", width=150)

        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<Double-1>", self.fill_form)

        # Frame untuk Form Input
        form_frame = Frame(self.root, bg="#e8f4f8")
        form_frame.pack(pady=10, padx=20, fill="x")

        Label(form_frame, text="Nama Siswa", font=self.label_font, bg="#e8f4f8").grid(row=0, column=0, padx=10, pady=5)
        Label(form_frame, text="Kelas", font=self.label_font, bg="#e8f4f8").grid(row=1, column=0, padx=10, pady=5)
        Label(form_frame, text="Nomor Absen", font=self.label_font, bg="#e8f4f8").grid(row=0, column=2, padx=10, pady=5)
        Label(form_frame, text="Absensi", font=self.label_font, bg="#e8f4f8").grid(row=1, column=2, padx=10, pady=5)

        self.title_entry = Entry(form_frame, width=30, font=("Arial", 11))
        self.author_entry = Entry(form_frame, width=30, font=("Arial", 11))
        self.year_entry = Entry(form_frame, width=30, font=("Arial", 11))
        self.category_entry = Entry(form_frame, width=30, font=("Arial", 11))

        self.title_entry.grid(row=0, column=1, padx=10, pady=5)
        self.author_entry.grid(row=1, column=1, padx=10, pady=5)
        self.year_entry.grid(row=0, column=3, padx=10, pady=5)
        self.category_entry.grid(row=1, column=3, padx=10, pady=5)

        # Tombol CRUD
        button_frame = Frame(self.root, bg="#e8f4f8")
        button_frame.pack(pady=10)

        Button(button_frame, text="Tambah", command=self.add_data, bg="#4caf50", fg="white", width=15).grid(row=0, column=0, padx=5)
        Button(button_frame, text="Ubah", command=self.change_data, bg="#2196f3", fg="white", width=15).grid(row=0, column=1, padx=5)
        Button(button_frame, text="Hapus", command=self.hapus_data, bg="#f44336", fg="white", width=15).grid(row=0, column=2, padx=5)
        Button(button_frame, text="Cari", command=self.cari_data, bg="#ff9800", fg="white", width=15).grid(row=0, column=3, padx=5)

        

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.load_books()

    def add_data(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()
        category = self.category_entry.get()

        if title and author and year and category:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO books (title, author, year, category) VALUES (?, ?, ?, ?)",
                    (title, author, year, category),
                )
            self.clear_form()
            self.load_books()
            messagebox.showinfo("Berhasil", "Data berhasil ditambahkan!")
        else:
            messagebox.showwarning("Input Error", "Semua field harus diisi!")

    def load_books(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM books")
        for book in cursor.fetchall():
            self.tree.insert("", "end", values=book)

    def fill_form(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")

        self.title_entry.delete(0, "end")
        self.author_entry.delete(0, "end")
        self.year_entry.delete(0, "end")
        self.category_entry.delete(0, "end")

        self.title_entry.insert(0, values[1])
        self.author_entry.insert(0, values[2])
        self.year_entry.insert(0, values[3])
        self.category_entry.insert(0, values[4])

        self.selected_id = values[0]

    def change_data(self):
        if not self.selected_id:
            messagebox.showwarning("Update Error", "Pilih data yang ingin diperbarui!")
            return

        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()
        category = self.category_entry.get()

        if title and author and year and category:
            with self.conn:
                self.conn.execute(
                    "UPDATE books SET title = ?, author = ?, year = ?, category = ? WHERE id = ?",
                    (title, author, year, category, self.selected_id),
                )
            self.clear_form()
            self.load_books()
            messagebox.showinfo("Berhasil", "Data berhasil diperbarui!")
        else:
            messagebox.showwarning("Input Error", "Semua field harus diisi!")

    def hapus_data(self):
        if not self.selected_id:
            messagebox.showwarning("Delete Error", "Pilih data yang ingin dihapus!")
            return

        with self.conn:
            self.conn.execute("DELETE FROM books WHERE id = ?", (self.selected_id,))
        self.clear_form()
        self.load_books()
        messagebox.showinfo("Berhasil", "Data berhasil dihapus!")

    def cari_data(self):
        query = self.title_entry.get()
        for row in self.tree.get_children():
            self.tree.delete(row)

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR category LIKE ?",
            (f"%{query}%", f"%{query}%", f"%{query}%"),
        )
        for book in cursor.fetchall():
            self.tree.insert("", "end", values=book)

    def clear_form(self):
        self.title_entry.delete(0, "end")
        self.author_entry.delete(0, "end")
        self.year_entry.delete(0, "end")
        self.category_entry.delete(0, "end")
        self.selected_id = None


if __name__ == "__main__":
    root = Tk()
    app = LibraryApp(root)
    root.mainloop()
