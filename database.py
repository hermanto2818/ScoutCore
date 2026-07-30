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

def tambah_siswa(nisn, no_induk, nama, jk, kelas):
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
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        nisn,
        no_induk,
        nama,
        jk,
        kelas,
        datetime.now().isoformat(),
        datetime.now().isoformat()
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

    print("Row terhapus =", cursor.rowcount)

    conn.commit()
    conn.close()