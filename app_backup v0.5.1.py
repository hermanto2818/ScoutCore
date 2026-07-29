
# ==========================================================
# ScoutCore
# Pramuka Information System
# Version : 0.5.1
# ==========================================================

import customtkinter as ctk
from tkinter import ttk, messagebox

from database import create_database, ambil_semua_siswa, jumlah_siswa
from import_excel import import_excel

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

create_database()

app = ctk.CTk()
app.title("ScoutCore - Pramuka Information System v0.5.1")
app.geometry("1280x720")

tree = None
lbl_jumlah = None
lbl_filter = None
content = None

search_var = ctk.StringVar()
kelas_var = ctk.StringVar(value="Semua")


def refresh_treeview():
    global tree, lbl_jumlah
    if tree is None:
        return

    for item in tree.get_children():
        tree.delete(item)

    for no, row in enumerate(ambil_semua_siswa(), start=1):
        _, nisn, no_induk, nama, jk, kelas, status = row
        tree.insert("", "end", values=(no, no_induk, nisn, nama, jk, kelas, status))

    lbl_jumlah.configure(text=f"Jumlah Data : {jumlah_siswa()}")


def aksi_import():
    import_excel()
    refresh_treeview()


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
    tb.pack(fill="x", padx=20)

    for t in ("Tambah","Edit","Hapus"):
        ctk.CTkButton(tb,text=t,width=120).pack(side="left", padx=5,pady=10)

    ctk.CTkButton(tb,text="Import Excel",command=aksi_import,width=150)\
        .pack(side="right", padx=5,pady=10)

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

ctk.CTkLabel(sidebar,text="Version 0.5.1").pack(pady=(5,20))

menus=[
("Dashboard",tampil_dashboard),
("Data Siswa",tampil_data_siswa),
("Anggota",lambda:messagebox.showinfo("Info","Segera hadir")),
("Absensi",lambda:messagebox.showinfo("Info","Segera hadir")),
("Rekap",lambda:messagebox.showinfo("Info","Segera hadir")),
("Nilai",lambda:messagebox.showinfo("Info","Segera hadir"))
]
for t,cmd in menus:
    ctk.CTkButton(sidebar,text=t,width=190,command=cmd).pack(pady=5)

tampil_dashboard()
app.mainloop()
