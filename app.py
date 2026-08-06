
# ==========================================================
# ScoutCore
# Smart Scout Administration
# Version : 0.5.4
# ==========================================================

import customtkinter as ctk
from tkinter import ttk, messagebox
from tkinter import filedialog
from PIL import Image
from database import (
    create_database,
    ambil_semua_siswa,
    daftar_nama_kelas,
    jumlah_siswa,
    tambah_siswa,
    update_siswa,
    hapus_siswa,
    cek_jumlah_siswa,
    ambil_siswa_by_nisn,

    ambil_semua_kelas,
    tambah_kelas,
    update_kelas,
    hapus_kelas,

    ambil_semua_golongan,
    daftar_nama_golongan,
    tambah_golongan,
    update_golongan,
    hapus_golongan,
    tentukan_golongan,
    ambil_administrator,
    simpan_administrator,

    cek_pertemuan_sudah_ada
)
from import_excel import import_excel

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
# ==========================================
# SCOUTCORE THEME
# ==========================================

SCOUT_GREEN = "#1B5E20"
SCOUT_GOLD = "#D4AF37"
SCOUT_WHITE = "#F7F7F7"
SCOUT_LIGHT = "#ECECEC"
SCOUT_TEXT = "#222222"


# ==========================================================
# Sprint v0.5.4
# TODO:
# - Search realtime
# - Filter kelas
# - Jumlah Data
# - Hasil Filter
# ==========================================================

create_database()

app = ctk.CTk()
app.title("ScoutCore - Smart Scout Administration v0.5.4")
app.geometry("1280x720")
app.iconbitmap("assets/scoutcore.ico")

tree = None
lbl_jumlah = None
lbl_filter = None
content = None

entry_search = None

tree_kelas = None

search_var = ctk.StringVar()
kelas_var = ctk.StringVar(value="Semua")


def refresh_treeview(data=None):
    global tree, lbl_jumlah

    if tree is None:
        return

    keyword = search_var.get().strip().lower()
    kelas_filter = kelas_var.get()

    if data is None:
        data = ambil_semua_siswa()

    hasil = []

    for row in data:
        id_siswa, nisn, no_induk, nama, jk, kelas_siswa, golongan, status = row

        cocok_search = (
            keyword == ""
            or keyword in str(nama).lower()
            or keyword in str(no_induk).lower()
            or keyword in str(nisn).lower()
        )

        cocok_kelas = (
            kelas_filter == "Semua"
            or kelas_siswa == kelas_filter
        )

        if cocok_search and cocok_kelas:
            hasil.append(row)

    tree.delete(*tree.get_children())

    for no, row in enumerate(hasil, start=1):
        id_siswa, nisn, no_induk, nama, jk, kelas_siswa, golongan, status = row

        tree.insert(
            "",
            "end",
            values=(
                no,
                no_induk,
                nisn,
                nama,
                jk,
                kelas_siswa,
                golongan,
                status
            )
        )

    lbl_jumlah.configure(text=f"Jumlah Data : {len(hasil)}")
def ambil_data_terpilih():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Peringatan",
            "Pilih data siswa terlebih dahulu."
        )
        return None

    id_siswa = selected[0]
    values = tree.item(selected[0], "values")

    return id_siswa, values

def aksi_import():
    import_excel()
    refresh_treeview()


def form_siswa(id_siswa=None, data=None):

    win = ctk.CTkToplevel(app)
    if id_siswa is None:
     win.title("Tambah Data Siswa")
    else:
     win.title("Edit Data Siswa")
    win.geometry("420x560")
    win.grab_set()

    # NISN
    ctk.CTkLabel(win, text="NISN").pack(pady=(15, 0))
    ent_nisn = ctk.CTkEntry(win, width=250)
    ent_nisn.pack()

    # No Induk
    ctk.CTkLabel(win, text="No Induk").pack(pady=(10, 0))
    ent_no = ctk.CTkEntry(win, width=250)
    ent_no.pack()

    # Nama
    ctk.CTkLabel(win, text="Nama").pack(pady=(10, 0))
    ent_nama = ctk.CTkEntry(win, width=250)
    ent_nama.pack()

    # Jenis Kelamin
    ctk.CTkLabel(win, text="Jenis Kelamin").pack(pady=(10, 0))
    cmb_jk = ctk.CTkComboBox(
        win,
        values=["L", "P"],
        width=250
    )
    cmb_jk.pack()

    # Kelas
    ctk.CTkLabel(win, text="Kelas").pack(pady=(10, 0))
    cmb_kelas = ctk.CTkComboBox(
        win,
        width=250,
        values=daftar_nama_kelas()
    )
    cmb_kelas.pack()
    def kelas_berubah(pilihan):
        print("kelas_berubah dipanggil:", pilihan)
        golongan = tentukan_golongan(pilihan)

        ent_golongan.configure(state="normal")
        ent_golongan.delete(0, "end")
        ent_golongan.insert(0, golongan)
        ent_golongan.configure(state="disabled")
    
    # Golongan
    ctk.CTkLabel(win, text="Golongan").pack(pady=(10, 0))

    ent_golongan = ctk.CTkEntry(
        win,
        width=250,
        state="disabled"
    )
    ent_golongan.pack()
    cmb_kelas.configure(command=kelas_berubah)
    def simpan():
        try:
            print("JK =", cmb_jk.get())
            tambah_siswa(
                ent_nisn.get(),
                ent_no.get(),
                ent_nama.get(),
                cmb_jk.get(),
                cmb_kelas.get(),
                ent_golongan.get()
            )

            print("Jumlah siswa:", cek_jumlah_siswa())

            refresh_treeview()

            messagebox.showinfo(
                "Berhasil",
                "Data siswa berhasil ditambahkan."
            )

            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(
        win,
        text="Simpan",
        command=simpan,
        width=200
    ).pack(pady=20)
# ==========================================================
# MASTER KELAS
# ==========================================================

def refresh_tree_kelas():

    global tree_kelas

    if tree_kelas is None:
        return

    tree_kelas.delete(*tree_kelas.get_children())

    data = ambil_semua_kelas()

    for no, row in enumerate(data, start=1):

        id_kelas = row[0]
        nama_kelas = row[1]

        tree_kelas.insert(
            "",
            "end",
            iid=str(id_kelas),
            values=(
                no,
                nama_kelas
            )
        )
def ambil_kelas_terpilih():

    selected = tree_kelas.selection()

    if not selected:
        messagebox.showwarning(
            "Peringatan",
            "Pilih data kelas terlebih dahulu."
        )
        return None

    id_kelas = int(selected[0])

    nama_kelas = tree_kelas.item(
        selected[0],
        "values"
    )[1]

    return (
        id_kelas,
        nama_kelas
    )
def edit_kelas():

    data = ambil_kelas_terpilih()

    if data is None:
        return

    id_kelas = int(data[0])
    nama_kelas = data[1]

    nama_lama = nama_kelas

    win = ctk.CTkToplevel(app)
    win.title("Edit Kelas")
    win.geometry("350x180")
    win.grab_set()

    ctk.CTkLabel(
        win,
        text="Nama Kelas"
    ).pack(pady=(20,5))

    entry_kelas = ctk.CTkEntry(
        win,
        width=250
    )
    entry_kelas.pack()

    entry_kelas.insert(0, nama_kelas)
    def simpan_edit():

        nama_baru = entry_kelas.get().strip()

        if nama_baru == "":
            messagebox.showwarning(
                "Peringatan",
                "Nama kelas tidak boleh kosong."
            )
            return

        try:

            update_kelas(
                id_kelas,
                nama_baru
                )

            refresh_tree_kelas()

            win.destroy()

        except Exception as e:

            print(e)

            messagebox.showerror(
                "Gagal",
                str(e)
            )
    ctk.CTkButton(
    win,
    text="Simpan",
    width=120,
    command=simpan_edit
).pack(pady=20)
def form_tambah_kelas():

    win = ctk.CTkToplevel(app)
    win.title("Tambah Kelas")
    win.geometry("350x180")
    win.grab_set()

    ctk.CTkLabel(
        win,
        text="Nama Kelas"
    ).pack(pady=(20, 5))

    entry_kelas = ctk.CTkEntry(
        win,
        width=250
    )
    entry_kelas.pack()

    def simpan():

        nama = entry_kelas.get().strip()

        if nama == "":
            messagebox.showwarning(
                "Peringatan",
                "Nama kelas tidak boleh kosong."
            )
            return

        try:
            tambah_kelas(nama)
            refresh_tree_kelas()
            win.destroy()
        except Exception:
            print("ERROR :", e)
            
            messagebox.showerror(
                "Gagal",
                "Nama kelas sudah ada."
            )

    ctk.CTkButton(
        win,
        text="Simpan",
        width=120,
        command=simpan
    ).pack(pady=20)
def hapus_kelas_data():

    data = ambil_kelas_terpilih()

    if data is None:
        return

    id_kelas = int(data[0])
    nama_kelas = data[1]

    jawab = messagebox.askyesno(
        "Konfirmasi",
        f"Yakin ingin menghapus kelas\n\n{nama_kelas} ?"
    )

    if not jawab:
        return

    hapus_kelas(id_kelas)

    refresh_tree_kelas()

    messagebox.showinfo(
        "Berhasil",
        "Data kelas berhasil dihapus."
    )
def tampil_master_kelas():

    global tree_kelas

    for w in content.winfo_children():
        w.destroy()

    ctk.CTkLabel(
        content,
        text="MASTER KELAS",
        font=("Segoe UI",28,"bold")
    ).pack(pady=15)
    toolbar = ctk.CTkFrame(content)
    toolbar.pack(fill="x", padx=20, pady=5)
    ctk.CTkButton(
    toolbar,
    text="Tambah",
    width=100,
    command=form_tambah_kelas
).pack(side="left", padx=5)

    ctk.CTkButton(
    toolbar,
    text="Edit",
    width=100,
    command=edit_kelas
).pack(side="left", padx=5)
    
    ctk.CTkButton(
    toolbar,
    text="Hapus",
    width=100,
    command=hapus_kelas_data
).pack(side="left", padx=5)

    frame = ctk.CTkFrame(content)
    frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )
    cols = ("No", "Nama Kelas")

    tree_kelas = ttk.Treeview(
        frame,
        columns=cols,
        show="headings"
    )
    tree_kelas.heading("No", text="No")
    tree_kelas.heading("Nama Kelas", text="Nama Kelas")
    tree_kelas.column(
        "No",
        width=70,
        anchor="center"
    )

    tree_kelas.column(
        "Nama Kelas",
        width=350,
        anchor="w"
    )
    tree_kelas.pack(
        fill="both",
        expand=True
    )
    refresh_tree_kelas()
# ==================================================
# MASTER GOLONGAN
# ==================================================
def refresh_tree_golongan():

    tree_golongan.delete(*tree_golongan.get_children())

    data = ambil_semua_golongan()

    for no, row in enumerate(data, start=1):

        id_golongan = row[0]
        nama_golongan = row[1]

        tree_golongan.insert(
            "",
            "end",
            iid=str(id_golongan),
            values=(
                no,
                nama_golongan
            )
        )
def ambil_golongan_terpilih():

    selected = tree_golongan.selection()

    if not selected:
        messagebox.showwarning(
            "Peringatan",
            "Pilih data golongan terlebih dahulu."
        )
        return None

    id_golongan = int(selected[0])

    nama_golongan = tree_golongan.item(
        selected[0],
        "values"
    )[1]

    return (
        id_golongan,
        nama_golongan
    )
def edit_golongan():

    data = ambil_golongan_terpilih()

    if data is None:
        return

    id_golongan = int(data[0])
    nama_golongan = data[1]

    win = ctk.CTkToplevel(app)
    win.title("Edit Golongan")
    win.geometry("350x180")
    win.grab_set()

    ctk.CTkLabel(
        win,
        text="Nama Golongan"
    ).pack(pady=(20, 5))

    entry_golongan = ctk.CTkEntry(
        win,
        width=250
    )
    entry_golongan.pack()

    entry_golongan.insert(0, nama_golongan)

    def simpan_edit():

        nama_baru = entry_golongan.get().strip()

        if nama_baru == "":
            messagebox.showwarning(
                "Peringatan",
                "Nama golongan tidak boleh kosong."
            )
            return

        try:

            update_golongan(
                id_golongan,
                nama_baru
            )

            refresh_tree_golongan()

            win.destroy()

        except Exception:

            messagebox.showerror(
                "Gagal",
                "Nama golongan sudah ada."
            )

    ctk.CTkButton(
        win,
        text="Simpan",
        width=120,
        command=simpan_edit
    ).pack(pady=20)
def form_tambah_golongan():

    win = ctk.CTkToplevel(app)
    win.title("Tambah Golongan")
    win.geometry("350x180")
    win.grab_set()

    ctk.CTkLabel(
        win,
        text="Nama Golongan"
    ).pack(pady=(20, 5))

    entry_golongan = ctk.CTkEntry(
        win,
        width=250
    )
    entry_golongan.pack()

    def simpan():

        nama = entry_golongan.get().strip()

        if nama == "":
            messagebox.showwarning(
                "Peringatan",
                "Nama golongan tidak boleh kosong."
            )
            return

        try:

            tambah_golongan(nama)

            refresh_tree_golongan()

            win.destroy()

        except Exception:

            messagebox.showerror(
                "Gagal",
                "Nama golongan sudah ada."
            )

    ctk.CTkButton(
        win,
        text="Simpan",
        width=120,
        command=simpan
    ).pack(pady=20)
def hapus_golongan_data():

    data = ambil_golongan_terpilih()

    if data is None:
        return

    id_golongan = int(data[0])
    nama_golongan = data[1]

    jawab = messagebox.askyesno(
        "Konfirmasi",
        f"Yakin ingin menghapus golongan\n\n{nama_golongan} ?"
    )

    if not jawab:
        return

    hapus_golongan(id_golongan)

    refresh_tree_golongan()

    messagebox.showinfo(
        "Berhasil",
        "Data golongan berhasil dihapus."
    )
def tampil_master_golongan():

    for w in content.winfo_children():
        w.destroy()

    ctk.CTkLabel(
        content,
        text="MASTER GOLONGAN",
        font=("Segoe UI", 28, "bold")
    ).pack(pady=15)
    toolbar = ctk.CTkFrame(content)
    toolbar.pack(fill="x", padx=20, pady=5)

    ctk.CTkButton(
        toolbar,
        text="Tambah",
        width=100,
        command=form_tambah_golongan
    ).pack(side="left", padx=5)

    ctk.CTkButton(
    toolbar,
    text="Edit",
    width=100,
    command=edit_golongan
    ).pack(side="left", padx=5)

    ctk.CTkButton(
    toolbar,
    text="Hapus",
    width=100,
    command=hapus_golongan_data
).pack(side="left", padx=5)
    frame = ctk.CTkFrame(content)

    frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    cols = ("No", "Nama Golongan")

    global tree_golongan

    tree_golongan = ttk.Treeview(
        frame,
        columns=cols,
        show="headings"
    )

    tree_golongan.heading("No", text="No")
    tree_golongan.heading("Nama Golongan", text="Nama Golongan")

    tree_golongan.column(
        "No",
        width=60,
        anchor="center"
    )

    tree_golongan.column(
        "Nama Golongan",
        anchor="center"
    )

    tree_golongan.pack(
        fill="both",
        expand=True
    )
    refresh_tree_golongan()
def tampil_dashboard():
    for w in content.winfo_children():
        w.destroy()
    data_admin = ambil_administrator()
    nomor_gudep = ""
    nama_pangkalan = ""
    tahun_ajaran = ""
    nama_pembina = ""

    if data_admin:

        nomor_gudep = data_admin[2]
        nama_pangkalan = data_admin[3]
        tahun_ajaran = data_admin[4]
        nama_pembina = data_admin[5]

    ctk.CTkLabel(
        content,
        text="ScoutCore",
        font=("Segoe UI", 22, "bold")
    ).pack(pady=(25, 5))

    ctk.CTkLabel(
        content,
        text="Smart Scout Administration",
        font=("Segoe UI", 16),
        text_color="gray40"
    ).pack()
    ctk.CTkLabel(
        content,
        text=f"Gudep {nomor_gudep}",
        font=("Segoe UI", 15, "bold")
    ).pack(pady=(10,0))

    ctk.CTkLabel(
        content,
        text=f"Pangkalan {nama_pangkalan}",
        font=("Segoe UI", 14)
    ).pack()

    ctk.CTkLabel(
        content,
        text=f"Tahun Ajaran {tahun_ajaran}",
        font=("Segoe UI", 13),
        text_color="gray40"
    ).pack(pady=(0,15))
    ctk.CTkFrame(
        content,
        height=2,
        fg_color="#D0D0D0"
    ).pack(fill="x", padx=40, pady=(10,20))

    ctk.CTkLabel(
        content,
        text=f"Selamat Datang, Kak {nama_pembina}",
        font=("Segoe UI",18,"bold"),
        text_color=SCOUT_GREEN
    ).pack(pady=(0,25))
    cards = ctk.CTkFrame(
        content,
        fg_color="transparent"
    )

    cards.pack(
        fill="x",
        padx=40,
        pady=(15,30)
    )

    stats = [
        ("Total Siswa", str(jumlah_siswa())),
        ("Anggota Aktif", "0"),
        ("Pertemuan", "0"),
        ("Kehadiran", "0%")
    ]

    # Membuat kolom otomatis berada di tengah
    for i in range(4):
        cards.grid_columnconfigure(i, weight=1)

    for col, (title, value) in enumerate(stats):

        box = ctk.CTkFrame(
            cards,
            width=180,
            height=120,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#D8D8D8"
        )

        box.grid(
            row=0,
            column=col,
            padx=15,
            pady=10,
            sticky=""
        )

        box.pack_propagate(False)

        ctk.CTkLabel(
            box,
            text=value,
            font=("Segoe UI",26,"bold")
        ).pack(pady=(18,4))

        ctk.CTkLabel(
            box,
            text=title
        ).pack()


def tampil_data_siswa():
    global tree, lbl_jumlah
    for w in content.winfo_children():
        w.destroy()

    ctk.CTkLabel(content, text="DATA SISWA",
                 font=("Segoe UI", 28, "bold")).pack(pady=15)

    tb = ctk.CTkFrame(content)
    tb.pack(fill="x", padx=20, pady=5)

    # Tombol
    ctk.CTkButton(
    tb,
    text="Tambah",
    width=100,
    command=lambda: form_siswa()
).pack(side="left", padx=5)
    ctk.CTkButton(
    tb,
    text="Edit",
    width=100,
    command=test_edit
).pack(side="left", padx=5)    
    ctk.CTkButton(
    tb,
    text="Hapus",
    width=100,
    command=hapus_data_siswa
).pack(side="left", padx=5)

    # Search
    ctk.CTkLabel(tb, text="Search :").pack(side="left", padx=(25,5))

    entry_search = ctk.CTkEntry(
        tb,
        width=220,
        placeholder_text="Nama / No Induk / NISN",
        textvariable=search_var
    )
    entry_search.pack(side="left", padx=5)

    entry_search.bind("<KeyRelease>", lambda e: refresh_treeview())

    ctk.CTkLabel(tb, text="Kelas :").pack(side="left", padx=(20,5))

    combo_kelas = ctk.CTkComboBox(
        tb,
        width=90,
        values=["Semua"] + daftar_nama_kelas(),
        variable=kelas_var,
        command=lambda x: refresh_treeview()
    )
    combo_kelas.pack(side="left", padx=5)

    # Import Excel
    ctk.CTkButton(
        tb,
        text="Import Excel",
        command=aksi_import,
        width=150
    ).pack(side="right", padx=5)

    frame = ctk.CTkFrame(content)
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    cols=("No","No Induk","NISN","Nama","JK","Kelas","Golongan","Status")
    tree=ttk.Treeview(frame, columns=cols, show="headings")

    widths={
    "No":60,
    "No Induk":110,
    "NISN":150,
    "Nama":330,
    "JK":60,
    "Kelas":90,
    "Golongan":120,
    "Status":90
    }
    for c in cols:
        tree.heading(c,text=c)
        tree.column(c,width=widths[c],anchor="w" if c=="Nama" else "center")

    y=ttk.Scrollbar(frame,orient="vertical",command=tree.yview)
    tree.configure(yscrollcommand=y.set)
    tree.pack(side="left",fill="both",expand=True)
    y.pack(side="right",fill="y")

    lbl_jumlah=ctk.CTkLabel(content,text="")
    lbl_jumlah.pack(pady=(0,10))
    refresh_treeview()

sidebar=ctk.CTkFrame(app,width=240)
sidebar.pack(side="left",fill="y")

content=ctk.CTkFrame(app)
content.pack(side="right",fill="both",expand=True,padx=10,pady=10)
logo = ctk.CTkImage(
    light_image=Image.open("assets/scoutcore_logo.png"),
    dark_image=Image.open("assets/scoutcore_logo.png"),
    size=(95,95)
)
ctk.CTkLabel(
    sidebar,
    image=logo,
    text=""
).pack(pady=(15,5))
ctk.CTkLabel(
    sidebar,
    text="ScoutCore",
    font=("Segoe UI",20,"bold")
).pack()

ctk.CTkLabel(
    sidebar,
    text="Smart Scout Administration",
    font=("Segoe UI",11)
).pack(pady=(0,15))
ctk.CTkLabel(
    sidebar,
    text="Version 0.5.4",
    font=("Segoe UI",10),
    text_color="gray50"
).pack(pady=(2,12))
ctk.CTkFrame(
    sidebar,
    height=2,
    fg_color="#D0D0D0"
).pack(fill="x", padx=15, pady=(5,15))

def test_edit():

    data = ambil_data_terpilih()

    if data is None:
        return

    _, values = data

    nisn = values[2]

    siswa = ambil_siswa_by_nisn(nisn)

    print(siswa)

    form_edit_siswa(siswa)
def hapus_data_siswa():

    data = ambil_data_terpilih()

    if data is None:
        messagebox.showwarning(
            "Peringatan",
            "Pilih data siswa terlebih dahulu."
        )
        return

    item, values = data

    nisn = values[2]

    siswa = ambil_siswa_by_nisn(nisn)

    if siswa is None:
        messagebox.showerror(
            "Error",
            "Data siswa tidak ditemukan."
        )
        return

    id_siswa = siswa[0]
    nama = siswa[3]

    jawab = messagebox.askyesno(
        "Konfirmasi Hapus",
        f"Yakin ingin menghapus siswa:\n\n{nama}?"
    )

    if not jawab:
        return

    print("ID yang akan dihapus =", id_siswa)

    hapus_siswa(id_siswa)

    print("DELETE selesai")

    refresh_treeview()

    messagebox.showinfo(
        "Berhasil",
        "Data siswa berhasil dihapus."
    )
def form_edit_siswa(siswa):
    id_siswa, nisn, no_induk, nama, jk, kelas, golongan, status = siswa

    win = ctk.CTkToplevel(app)
    win.title("Edit Data Siswa")
    win.geometry("500x620")
    win.resizable(False, False)
    win.grab_set()

    ctk.CTkLabel(win, text="EDIT DATA SISWA", font=("Segoe UI",20,"bold")).pack(pady=15)

    ctk.CTkLabel(win,text="NISN").pack(anchor="w",padx=40)
    entry_nisn=ctk.CTkEntry(win,width=420); entry_nisn.pack(pady=(0,10)); entry_nisn.insert(0,nisn)

    ctk.CTkLabel(win,text="No Induk").pack(anchor="w",padx=40)
    entry_no_induk=ctk.CTkEntry(win,width=420); entry_no_induk.pack(pady=(0,10)); entry_no_induk.insert(0,no_induk)

    ctk.CTkLabel(win,text="Nama Lengkap").pack(anchor="w",padx=40)
    entry_nama=ctk.CTkEntry(win,width=420); entry_nama.pack(pady=(0,10)); entry_nama.insert(0,nama)

    ctk.CTkLabel(win,text="Jenis Kelamin").pack(anchor="w",padx=40)
    combo_jk=ctk.CTkComboBox(win,values=["L","P"],width=420)
    combo_jk.pack(pady=(0,10)); combo_jk.set(jk)

    ctk.CTkLabel(win,text="Kelas").pack(anchor="w",padx=40)
    combo_kelas=ctk.CTkComboBox(win,values=daftar_nama_kelas(),width=420)
    combo_kelas.pack(pady=(0,10))

    ctk.CTkLabel(win,text="Golongan").pack(anchor="w",padx=40)
    entry_golongan=ctk.CTkEntry(win,width=420)
    entry_golongan.pack(pady=(0,10))

    def kelas_berubah(pilihan):
        g=tentukan_golongan(pilihan)
        entry_golongan.configure(state="normal")
        entry_golongan.delete(0,"end")
        entry_golongan.insert(0,g)
        entry_golongan.configure(state="disabled")

    combo_kelas.configure(command=kelas_berubah)
    combo_kelas.set(kelas)
    kelas_berubah(kelas)

    ctk.CTkLabel(win,text="Status").pack(anchor="w",padx=40)
    combo_status=ctk.CTkComboBox(win,values=["Aktif","Nonaktif"],width=420)
    combo_status.pack(pady=(0,20)); combo_status.set(status)

    def simpan_edit():
        update_siswa(
            id_siswa,
            entry_nisn.get(),
            entry_no_induk.get(),
            entry_nama.get(),
            combo_jk.get(),
            combo_kelas.get(),
            entry_golongan.get()
        )
        refresh_treeview()
        messagebox.showinfo("Berhasil","Data siswa berhasil diperbarui.")
        win.destroy()

    ctk.CTkButton(win,text="💾 Simpan",command=simpan_edit,width=200,height=40).pack(pady=20)

def tampil_administrator():

    for w in content.winfo_children():
        w.destroy()

    ctk.CTkLabel(
        content,
        text="ADMINISTRATOR",
        font=("Segoe UI", 28, "bold")
    ).pack(pady=20)

    ctk.CTkLabel(
        content,
        text="Pengaturan Identitas ScoutCore",
        font=("Segoe UI", 15)
    ).pack()

    # ==========================
    # Nama Aplikasi
    # ==========================

    ctk.CTkLabel(
        content,
        text="Nama Aplikasi"
    ).pack(pady=(20,5))

    entry_nama_aplikasi = ctk.CTkEntry(
        content,
        width=350
    )
    entry_nama_aplikasi.pack()

    entry_nama_aplikasi.insert(
        0,
        "ScoutCore"
    )
    # ==========================
    # Nomor Gugusdepan
    # ==========================

    ctk.CTkLabel(
        content,
        text="Nomor Gugusdepan"
    ).pack(pady=(15,5))

    entry_nomor_gudep = ctk.CTkEntry(
        content,
        width=350
    )
    entry_nomor_gudep.pack()

    # ==========================
    # Nama Pangkalan
    # ==========================

    ctk.CTkLabel(
        content,
        text="Nama Pangkalan"
    ).pack(pady=(15,5))

    entry_nama_pangkalan = ctk.CTkEntry(
        content,
        width=350
    )
    entry_nama_pangkalan.pack()
    # ==========================
    # Tahun Ajaran
    # ==========================

    ctk.CTkLabel(
        content,
        text="Tahun Ajaran"
    ).pack(pady=(15,5))

    entry_tahun_ajaran = ctk.CTkEntry(
        content,
        width=350
    )
    entry_tahun_ajaran.pack()

    # ==========================
    # Nama Pembina
    # ==========================

    ctk.CTkLabel(
        content,
        text="Nama Pembina"
    ).pack(pady=(15,5))

    entry_nama_pembina = ctk.CTkEntry(
        content,
        width=350
    )
    entry_nama_pembina.pack()

    # ==========================
    # Logo Gugusdepan
    # ==========================

    ctk.CTkLabel(
        content,
        text="Logo Gugusdepan"
    ).pack(pady=(15,5))

    label_logo = ctk.CTkLabel(
        content,
        text="Belum ada logo dipilih"
    )
    label_logo.pack()


    def pilih_logo():

        file = filedialog.askopenfilename(

            title="Pilih Logo Gugusdepan",

            filetypes=[
                ("Image", "*.png *.jpg *.jpeg")
            ]

        )

        if file:
            label_logo.configure(text=file)


    ctk.CTkButton(
        content,
        text="Pilih Logo",
        width=180,
        command=pilih_logo
    ).pack(pady=10)
    # ==========================
    # Ambil Data Administrator
    # ==========================

    data = ambil_administrator()

    if data:

        entry_nama_aplikasi.delete(0, "end")
        entry_nama_aplikasi.insert(0, data[1])

        entry_nomor_gudep.delete(0, "end")
        entry_nomor_gudep.insert(0, data[2])

        entry_nama_pangkalan.delete(0, "end")
        entry_nama_pangkalan.insert(0, data[3])

        entry_tahun_ajaran.delete(0, "end")
        entry_tahun_ajaran.insert(0, data[4])

        entry_nama_pembina.delete(0, "end")
        entry_nama_pembina.insert(0, data[5])
    def simpan():

        simpan_administrator(

            entry_nama_aplikasi.get(),

            entry_nomor_gudep.get(),

            entry_nama_pangkalan.get(),

            entry_tahun_ajaran.get(),

            entry_nama_pembina.get(),

            "",

            76,
            51,
            26,
            0

        )

        messagebox.showinfo(
            "Berhasil",
            "Data Administrator berhasil disimpan."
        )
    # ==========================
    # Tombol Simpan
    # ==========================

    ctk.CTkButton(
        content,
        text="Simpan",
        width=180,
        height=40,
        command=simpan
    ).pack(pady=25)
def tampil_absensi():

    # Bersihkan area content
    for w in content.winfo_children():
        w.destroy()

    data_admin = ambil_administrator()

    # ==========================
    # Judul
    # ==========================

    ctk.CTkLabel(
        content,
        text="ABSENSI LATIHAN",
        font=("Segoe UI", 28, "bold")
    ).pack(pady=20)

    ctk.CTkLabel(
        content,
        text="Persiapan Pertemuan Latihan",
        font=("Segoe UI", 15)
    ).pack()

    # ==========================
    # Tanggal
    # ==========================

    ctk.CTkLabel(
        content,
        text="Tanggal Latihan"
    ).pack(pady=(25, 5))

    entry_tanggal = ctk.CTkEntry(
        content,
        width=250
    )
    entry_tanggal.pack()

    # ==========================
    # Semester
    # ==========================

    ctk.CTkLabel(
        content,
        text="Semester"
    ).pack(pady=(15, 5))

    cmb_semester = ctk.CTkComboBox(
        content,
        width=250,
        values=["Ganjil", "Genap"]
    )
    cmb_semester.pack()

    # ==========================
    # Pertemuan
    # ==========================

    ctk.CTkLabel(
        content,
        text="Pertemuan"
    ).pack(pady=(15, 5))

    entry_pertemuan = ctk.CTkEntry(
        content,
        width=250
    )
    entry_pertemuan.pack()

    # ==========================
    # Kegiatan
    # ==========================

    ctk.CTkLabel(
        content,
        text="Kegiatan"
    ).pack(pady=(15, 5))

    cmb_kegiatan = ctk.CTkComboBox(
        content,
        width=250,
        values=["Latihan Rutin"]
    )
    cmb_kegiatan.pack()

    # ==========================
    # Nama Pembina
    # ==========================

    ctk.CTkLabel(
        content,
        text="Nama Pembina"
    ).pack(pady=(15, 5))

    entry_pembina = ctk.CTkEntry(
        content,
        width=250
    )
    entry_pembina.pack()

    if data_admin:
        entry_pembina.insert(0, data_admin[5])

    # ==========================
    # Tombol Buat Absensi
    # ==========================

    def buat_absensi():

        # Validasi tanggal
        if entry_tanggal.get().strip() == "":
            messagebox.showwarning(
                "Peringatan",
                "Tanggal Latihan harus diisi."
            )
            return

        # Validasi semester
        if cmb_semester.get().strip() == "":
            messagebox.showwarning(
                "Peringatan",
                "Semester harus dipilih."
            )
            return

        # Validasi pertemuan
        if entry_pertemuan.get().strip() == "":
            messagebox.showwarning(
                "Peringatan",
                "Pertemuan harus diisi."
            )
            return

        # Validasi kegiatan
        if cmb_kegiatan.get().strip() == "":
            messagebox.showwarning(
                "Peringatan",
                "Kegiatan harus dipilih."
            )
            return

        # Cek pertemuan ganda
        if cek_pertemuan_sudah_ada(
            cmb_semester.get(),
            entry_pertemuan.get()
        ):
            messagebox.showwarning(
                "Peringatan",
                f"Pertemuan {entry_pertemuan.get()} Semester {cmb_semester.get()} sudah pernah dibuat."
            )
            return

        # Lolos semua validasi
        messagebox.showinfo(
            "ScoutCore",
            "Data valid dan siap membuat absensi."
        )

    ctk.CTkButton(
        content,
        text="BUAT ABSENSI",
        width=220,
        height=45,
        command=buat_absensi
    ).pack(pady=30)
    
menus = [

("Dashboard", tampil_dashboard),

("Data Anggota", tampil_data_siswa),

("Master Kelas", tampil_master_kelas),

("Master Golongan", tampil_master_golongan),

("Absensi", tampil_absensi),

("Nilai", lambda: messagebox.showinfo("Info", "Segera hadir")),

("Administrator", tampil_administrator)

]
for t,cmd in menus:
    ctk.CTkButton(sidebar,text=t,width=190,height=38,fg_color=SCOUT_GREEN,command=cmd).pack(pady=5)

tampil_dashboard()
app.mainloop()
