
# ==========================================================
# ScoutCore
# Pramuka Information System
# Version : 0.5.4
# ==========================================================

import customtkinter as ctk
from tkinter import ttk, messagebox

from database import (
    create_database,
    ambil_semua_siswa,
    jumlah_siswa,
    tambah_siswa,
    update_siswa,
    hapus_siswa,
    cek_jumlah_siswa,
    ambil_siswa_by_nisn,

    ambil_semua_kelas,
    tambah_kelas,
    update_kelas,
    hapus_kelas
)
from import_excel import import_excel

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")



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
app.title("ScoutCore - Pramuka Information System v0.5.4")
app.geometry("1280x720")

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
        id_siswa, nisn, no_induk, nama, jk, kelas_siswa, status = row

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
        id_siswa, nisn, no_induk, nama, jk, kelas_siswa, status = row

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
        values=[
            "4 A",
            "4 B",
            "5 A",
            "5 B",
            "6 A",
            "6 B"
        ]
    )
    cmb_kelas.pack()

    def simpan():
        try:
            print("JK =", cmb_jk.get())
            tambah_siswa(
                ent_nisn.get(),
                ent_no.get(),
                ent_nama.get(),
                cmb_jk.get(),
                cmb_kelas.get()
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

        tree_kelas.insert(
            "",
            "end",
            values=(
                no,
                row[1]
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

    values = tree_kelas.item(selected[0], "values")

    return values
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
def tampil_dashboard():
    for w in content.winfo_children():
        w.destroy()

    ctk.CTkLabel(
        content,
        text="ScoutCore",
        font=("Segoe UI", 34, "bold")
    ).pack(pady=(25, 5))

    ctk.CTkLabel(
        content,
        text="Pramuka Information System",
        font=("Segoe UI", 18)
    ).pack()

    cards = ctk.CTkFrame(content)
    cards.pack(pady=30)

    stats = [
        ("Total Siswa", str(jumlah_siswa())),
        ("Anggota Pramuka", "0"),
        ("Pertemuan", "0"),
        ("Kehadiran", "0%")
    ]

    for title, value in stats:
        box = ctk.CTkFrame(cards, width=180, height=110)
        box.pack(side="left", padx=12)
        box.pack_propagate(False)
        ctk.CTkLabel(box, text=value, font=("Segoe UI", 26, "bold")).pack(pady=(18,4))
        ctk.CTkLabel(box, text=title).pack()


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
        values=["Semua", "4 A", "4 B", "5 A", "5 B", "6 A", "6 B"],
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

    cols=("No","No Induk","NISN","Nama","JK","Kelas","Status")
    tree=ttk.Treeview(frame, columns=cols, show="headings")

    widths={"No":60,"No Induk":110,"NISN":150,"Nama":330,"JK":60,"Kelas":90,"Status":90}
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

ctk.CTkLabel(sidebar,text="⚜",font=("Segoe UI Emoji",36)).pack(pady=(20,5))
ctk.CTkLabel(sidebar,
             text="ScoutCore\nPramuka Information\nSystem",
             font=("Segoe UI",18,"bold"),
             justify="center").pack()

ctk.CTkLabel(sidebar,text="Version 0.5.4").pack(pady=(5,20))
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

    # ==========================
    # Ambil data dari database
    # ==========================
    id_siswa, nisn, no_induk, nama, jk, kelas, status = siswa

    # ==========================
    # Window
    # ==========================
    win = ctk.CTkToplevel(app)
    win.title("Edit Data Siswa")
    win.geometry("500x520")
    win.resizable(False, False)
    win.grab_set()

    # ==========================
    # Judul
    # ==========================
    lbl_judul = ctk.CTkLabel(
        win,
        text="EDIT DATA SISWA",
        font=("Segoe UI", 20, "bold")
    )
    lbl_judul.pack(pady=15)

    # ==========================
    # NISN
    # ==========================
    ctk.CTkLabel(win, text="NISN").pack(anchor="w", padx=40)

    entry_nisn = ctk.CTkEntry(win, width=420)
    entry_nisn.pack(pady=(0,10))
    entry_nisn.insert(0, nisn)

    # ==========================
    # No Induk
    # ==========================
    ctk.CTkLabel(win, text="No Induk").pack(anchor="w", padx=40)

    entry_no_induk = ctk.CTkEntry(win, width=420)
    entry_no_induk.pack(pady=(0,10))
    entry_no_induk.insert(0, no_induk)

    # ==========================
    # Nama
    # ==========================
    ctk.CTkLabel(win, text="Nama Lengkap").pack(anchor="w", padx=40)

    entry_nama = ctk.CTkEntry(win, width=420)
    entry_nama.pack(pady=(0,10))
    entry_nama.insert(0, nama)

    # ==========================
    # Jenis Kelamin
    # ==========================
    ctk.CTkLabel(win, text="Jenis Kelamin").pack(anchor="w", padx=40)

    combo_jk = ctk.CTkComboBox(
        win,
        values=["L", "P"],
        width=420
    )
    combo_jk.pack(pady=(0,10))
    print(f"JK dari database = '{jk}'")
    combo_jk.set(jk)

    # ==========================
    # Kelas
    # ==========================
    ctk.CTkLabel(win, text="Kelas").pack(anchor="w", padx=40)

    combo_kelas = ctk.CTkComboBox(
        win,
        width=420,
        values=[
            "4 A",
            "4 B",
            "5 A",
            "5 B",
            "6 A",
            "6 B"
        ]
    )
    combo_kelas.pack(pady=(0,10))

    combo_kelas.set(kelas)

    # ==========================
    # Status
    # ==========================
    ctk.CTkLabel(win, text="Status").pack(anchor="w", padx=40)

    combo_status = ctk.CTkComboBox(
        win,
        values=["Aktif", "Nonaktif"],
        width=420
    )
    combo_status.pack(pady=(0,20))
    combo_status.set(status)
    # ==========================
    # Simpan
    # ==========================

    def simpan_edit():

        try:

            update_siswa(
                id_siswa,
                entry_nisn.get(),
                entry_no_induk.get(),
                entry_nama.get(),
                combo_jk.get(),
                combo_kelas.get()
            )

            refresh_treeview()

            messagebox.showinfo(
                "Berhasil",
                "Data siswa berhasil diperbarui."
            )

            win.destroy()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    ctk.CTkButton(
        win,
        text="💾 Simpan",
        command=simpan_edit,
        width=200,
        height=40
    ).pack(pady=20)

menus=[
("Dashboard", tampil_dashboard),
("Data Siswa", tampil_data_siswa),

("Master Kelas", tampil_master_kelas),

("Anggota", lambda: messagebox.showinfo("Info","Segera hadir")),
("Absensi", lambda: messagebox.showinfo("Info","Segera hadir")),
("Rekap", lambda: messagebox.showinfo("Info","Segera hadir")),
("Nilai", lambda: messagebox.showinfo("Info","Segera hadir"))
]
for t,cmd in menus:
    ctk.CTkButton(sidebar,text=t,width=190,command=cmd).pack(pady=5)

tampil_dashboard()
app.mainloop()
