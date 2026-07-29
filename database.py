import sqlite3
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