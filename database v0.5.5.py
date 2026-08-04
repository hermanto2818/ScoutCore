import sqlite3
from sqlite3 import IntegrityError
from datetime import datetime

DATABASE = "pramuka.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS siswa (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nisn TEXT UNIQUE,
        no_induk TEXT,
        nama TEXT,
        jk TEXT,
        kelas TEXT,

        status TEXT DEFAULT 'Aktif',

        anggota_pramuka INTEGER DEFAULT 0,

        created_at TEXT,
        updated_at TEXT

    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kelas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_kelas TEXT NOT NULL UNIQUE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS golongan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_golongan TEXT NOT NULL UNIQUE
    )
    """)
    try:
        cursor.execute("""
            ALTER TABLE siswa
            ADD COLUMN golongan TEXT
        """)
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()
    

def kosongkan_data_siswa():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM siswa")

    conn.commit()
    conn.close()


def simpan_siswa(data):

    conn = get_connection()
    cursor = conn.cursor()

    sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for siswa in data:

        cursor.execute("""

        INSERT OR REPLACE INTO siswa
        (
            nisn,
            no_induk,
            nama,
            jk,
            kelas,
            status,
            anggota_pramuka,
            created_at,
            updated_at
        )

        VALUES
        (?,?,?,?,?,?,?,?,?)

        """,
        (
            siswa["nisn"],
            siswa["no_induk"],
            siswa["nama"],
            siswa["jk"],
            siswa["kelas"],
            "Aktif",
            0,
            sekarang,
            sekarang
        ))

    conn.commit()
    conn.close()


def ambil_semua_siswa():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        id,
        nisn,
        no_induk,
        nama,
        jk,
        kelas,
        golongan,
        status

        FROM siswa

        ORDER BY kelas,nama

    """)

    data = cursor.fetchall()

    conn.close()

    return data


def jumlah_siswa():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM siswa")

    jumlah = cursor.fetchone()[0]

    conn.close()

    return jumlah

def tambah_siswa(nisn, no_induk, nama, jk, kelas, golongan):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO siswa
        (
            nisn,
            no_induk,
            nama,
            jk,
            kelas,
            golongan,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        (
        nisn,
        no_induk,
        nama,
        jk,
        kelas,
        golongan,
        datetime.now().isoformat(),
        datetime.now().isoformat()
    )
    ))

    conn.commit()
    conn.close()


def cek_jumlah_siswa():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM siswa")
    jumlah = cursor.fetchone()[0]

    conn.close()
    return jumlah

def update_siswa(id_siswa, nisn, no_induk, nama, jk, kelas):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE siswa
        SET
            nisn = ?,
            no_induk = ?,
            nama = ?,
            jk = ?,
            kelas = ?,
            updated_at = ?
        WHERE id = ?
    """, (
        nisn,
        no_induk,
        nama,
        jk,
        kelas,
        datetime.now().isoformat(),
        id_siswa
    ))

    conn.commit()
    conn.close()
def ambil_siswa_by_nisn(nisn):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            nisn,
            no_induk,
            nama,
            jk,
            kelas,
            status
        FROM siswa
        WHERE nisn = ?
    """, (nisn,))

    data = cursor.fetchone()

    conn.close()

    return data

def hapus_siswa(id_siswa):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM siswa
        WHERE id = ?
    """, (id_siswa,))

    conn.commit()
    conn.close()
# ==================================================
# DATABASE MASTER GOLONGAN
# ==================================================

def ambil_semua_golongan():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nama_golongan
        FROM golongan
        ORDER BY nama_golongan
    """)

    data = cursor.fetchall()

    conn.close()
    return data
def tambah_golongan(nama_golongan):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO golongan (nama_golongan)
        VALUES (?)
    """, (nama_golongan,))

    conn.commit()
    conn.close()
def update_golongan(id_golongan, nama_golongan):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE golongan
        SET nama_golongan = ?
        WHERE id = ?
    """, (nama_golongan, id_golongan))

    conn.commit()
    conn.close()
def hapus_golongan(id_golongan):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM golongan
        WHERE id = ?
    """, (id_golongan,))

    conn.commit()
    conn.close()
# ==================================================
# DATABASE MASTER KELAS
# ==================================================

def ambil_semua_kelas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nama_kelas
        FROM kelas
        ORDER BY nama_kelas
    """)

    data = cursor.fetchall()

    conn.close()
    return data
def daftar_nama_kelas():

    data = ambil_semua_kelas()

    print(data)

    return [row[1] for row in data]

def tambah_kelas(nama_kelas):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO kelas (nama_kelas)
        VALUES (?)
    """, (nama_kelas,))

    conn.commit()
    conn.close()


def update_kelas(id_kelas, nama_kelas):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE kelas
        SET nama_kelas = ?
        WHERE id = ?
    """, (nama_kelas, id_kelas))

    conn.commit()
    conn.close()


def hapus_kelas(id_kelas):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM kelas
        WHERE id = ?
    """, (id_kelas,))

    conn.commit()
    conn.close()

def tentukan_golongan(nama_kelas):

    nama_kelas = str(nama_kelas).strip()

    if nama_kelas.startswith(("1", "2", "3")):
        return "Siaga"

    elif nama_kelas.startswith(("4", "5", "6", "7", "8", "9")):
        return "Penggalang"

    elif nama_kelas.startswith(("10", "11", "12")):
        return "Penegak"

    return ""