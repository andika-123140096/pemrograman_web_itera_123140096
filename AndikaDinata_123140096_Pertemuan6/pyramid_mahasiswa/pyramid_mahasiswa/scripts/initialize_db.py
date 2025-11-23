import argparse
import sys
from datetime import date

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from .. import models

def setup_models(dbsession):
    """
    Add initial model objects.
    """

    existing_mahasiswa1 = dbsession.query(models.Mahasiswa).filter_by(nim='12345').first()
    existing_mahasiswa2 = dbsession.query(models.Mahasiswa).filter_by(nim='54321').first()
    
    if not existing_mahasiswa1:
        mahasiswa1 = models.Mahasiswa(
            nim='12345',
            nama='Budi Santoso',
            jurusan='Teknik Informatika',
            tanggal_lahir=date(2000, 5, 15),
            alamat='Jl. Merdeka No. 123, Bandung'
        )
        dbsession.add(mahasiswa1)
        print("Mahasiswa 12345 added.")
    else:
        print("Mahasiswa 12345 already exists.")
    
    if not existing_mahasiswa2:
        mahasiswa2 = models.Mahasiswa(
            nim='54321',
            nama='Siti Aminah',
            jurusan='Sistem Informasi',
            tanggal_lahir=date(2001, 8, 22),
            alamat='Jl. Mawar No. 45, Jakarta'
        )
        dbsession.add(mahasiswa2)
        print("Mahasiswa 54321 added.")
    else:
        print("Mahasiswa 54321 already exists.")

    # Setup matakuliah dummy data
    matakuliah_data = [
        {'kode_mk': 'TI101', 'nama_mk': 'Pemrograman Web', 'sks': 3, 'semester': 3},
        {'kode_mk': 'TI102', 'nama_mk': 'Basis Data', 'sks': 3, 'semester': 4},
        {'kode_mk': 'TI103', 'nama_mk': 'Algoritma dan Struktur Data', 'sks': 4, 'semester': 2},
        {'kode_mk': 'TI104', 'nama_mk': 'Sistem Operasi', 'sks': 3, 'semester': 5},
        {'kode_mk': 'TI105', 'nama_mk': 'Jaringan Komputer', 'sks': 3, 'semester': 4},
        {'kode_mk': 'TI106', 'nama_mk': 'Kecerdasan Buatan', 'sks': 3, 'semester': 6},
        {'kode_mk': 'TI107', 'nama_mk': 'Machine Learning', 'sks': 3, 'semester': 7},
        {'kode_mk': 'TI108', 'nama_mk': 'Keamanan Informasi', 'sks': 3, 'semester': 6},
        {'kode_mk': 'TI109', 'nama_mk': 'Rekayasa Perangkat Lunak', 'sks': 4, 'semester': 5},
        {'kode_mk': 'TI110', 'nama_mk': 'Manajemen Proyek TI', 'sks': 2, 'semester': 8},
    ]

    for mk_data in matakuliah_data:
        existing_mk = dbsession.query(models.Matakuliah).filter_by(kode_mk=mk_data['kode_mk']).first()
        if not existing_mk:
            matakuliah = models.Matakuliah(
                kode_mk=mk_data['kode_mk'],
                nama_mk=mk_data['nama_mk'],
                sks=mk_data['sks'],
                semester=mk_data['semester']
            )
            dbsession.add(matakuliah)
            print(f"Matakuliah {mk_data['kode_mk']} added.")
        else:
            print(f"Matakuliah {mk_data['kode_mk']} already exists.")

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)

    # bootstrap will return a context with request + closer
    env = bootstrap(args.config_uri)
    request = env['request']

    try:
        # gunakan request.tm (bukan tm_manager)
        with request.tm:
            dbsession = request.dbsession
            setup_models(dbsession)

        print("Database initialized successfully.")

    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.

Your database should be up and running before you
initialize your project. Make sure your database server
is running and your connection string in development.ini
is correctly configured.
''')

    finally:
        env['closer']()


if __name__ == '__main__':
    main()