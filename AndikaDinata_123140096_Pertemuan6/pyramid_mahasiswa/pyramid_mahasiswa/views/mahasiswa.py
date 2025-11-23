import datetime
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    HTTPBadRequest,
)
from ..models import Mahasiswa


@view_config(route_name='mahasiswa_list', renderer='json')
def mahasiswa_list(request):
    """View untuk menampilkan daftar mahasiswa"""
    dbsession = request.dbsession
    mahasiswas = dbsession.query(Mahasiswa).all()
    return {'mahasiswas': [m.to_dict() for m in mahasiswas]}


@view_config(route_name='mahasiswa_detail', renderer='json')
def mahasiswa_detail(request):
    """View untuk melihat detail satu mahasiswa"""
    dbsession = request.dbsession
    mahasiswa_id = request.matchdict['id']
    mahasiswa = dbsession.query(Mahasiswa).filter_by(id=mahasiswa_id).first()

    if mahasiswa is None:
        return HTTPNotFound(json_body={'error': 'Mahasiswa tidak ditemukan'})

    return {'mahasiswa': mahasiswa.to_dict()}


@view_config(route_name='mahasiswa_add', request_method='POST', renderer='json')
def mahasiswa_add(request):
    """View untuk menambahkan mahasiswa baru"""
    try:
        # Ambil data dari request JSON
        json_data = request.json_body

        # Validasi data minimal
        required_fields = ['nim', 'nama', 'jurusan']
        for field in required_fields:
            if field not in json_data:
                return HTTPBadRequest(
                    json_body={'error': f'Field {field} wajib diisi'}
                )

        # Parse tanggal lahir jika ada
        tanggal_lahir = None
        if 'tanggal_lahir' in json_data and json_data['tanggal_lahir']:
            try:
                tanggal_lahir = datetime.datetime.fromisoformat(
                    json_data['tanggal_lahir']
                ).date()
            except ValueError:
                return HTTPBadRequest(
                    json_body={
                        'error': 'Format tanggal lahir tidak valid. Gunakan YYYY-MM-DD'
                    }
                )

        # Buat objek Mahasiswa baru
        mahasiswa = Mahasiswa(
            nim=json_data['nim'],
            nama=json_data['nama'],
            jurusan=json_data['jurusan'],
            tanggal_lahir=tanggal_lahir,
            alamat=json_data.get('alamat')
        )

        # Simpan ke database
        dbsession = request.dbsession
        dbsession.add(mahasiswa)
        dbsession.flush()  # Untuk mendapatkan ID yang baru dibuat

        return {'success': True, 'mahasiswa': mahasiswa.to_dict()}

    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})


@view_config(route_name='mahasiswa_update', request_method='PUT', renderer='json')
def mahasiswa_update(request):
    """View untuk mengupdate data mahasiswa"""
    dbsession = request.dbsession
    mahasiswa_id = request.matchdict['id']

    # Cari mahasiswa yang akan diupdate
    mahasiswa = dbsession.query(Mahasiswa).filter_by(id=mahasiswa_id).first()
    if mahasiswa is None:
        return HTTPNotFound(json_body={'error': 'Mahasiswa tidak ditemukan'})

    try:
        # Ambil data dari request JSON
        json_data = request.json_body

        # Update atribut yang ada di request
        if 'nim' in json_data:
            mahasiswa.nim = json_data['nim']
        if 'nama' in json_data:
            mahasiswa.nama = json_data['nama']
        if 'jurusan' in json_data:
            mahasiswa.jurusan = json_data['jurusan']
        if 'alamat' in json_data:
            mahasiswa.alamat = json_data['alamat']

        # Parse tanggal lahir jika ada
        if 'tanggal_lahir' in json_data:
            if json_data['tanggal_lahir']:
                try:
                    mahasiswa.tanggal_lahir = datetime.datetime.fromisoformat(
                        json_data['tanggal_lahir']
                    ).date()
                except ValueError:
                    return HTTPBadRequest(
                        json_body={
                            'error': 'Format tanggal lahir tidak valid. Gunakan YYYY-MM-DD'
                        }
                    )
            else:
                mahasiswa.tanggal_lahir = None

        return {'success': True, 'mahasiswa': mahasiswa.to_dict()}

    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})


@view_config(route_name='mahasiswa_delete', request_method='DELETE', renderer='json')
def mahasiswa_delete(request):
    """View untuk menghapus data mahasiswa"""
    dbsession = request.dbsession
    mahasiswa_id = request.matchdict['id']

    # Cari mahasiswa yang akan dihapus
    mahasiswa = dbsession.query(Mahasiswa).filter_by(id=mahasiswa_id).first()
    if mahasiswa is None:
        return HTTPNotFound(json_body={'error': 'Mahasiswa tidak ditemukan'})

    # Hapus dari database
    dbsession.delete(mahasiswa)

    return {
        'success': True,
        'message': f'Mahasiswa dengan id {mahasiswa_id} berhasil dihapus'
    }