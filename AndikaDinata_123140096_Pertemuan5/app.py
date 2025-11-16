from abc import ABC, abstractmethod

class ItemPerpustakaan(ABC):
    def __init__(self, id, judul):
        self._id = id
        self._judul = judul

    @abstractmethod
    def tampilkan_info(self):
        pass

class Buku(ItemPerpustakaan):
    def __init__(self, id, judul, penulis, tahun):
        super().__init__(id, judul)
        self._penulis = penulis
        self._tahun = tahun

    def tampilkan_info(self):
        return f"ID Buku: {self._id}, Judul: {self._judul}, Penulis: {self._penulis}, Tahun: {self._tahun}"

    @property
    def judul(self):
        return self._judul

    @judul.setter
    def judul(self, value):
        self._judul = value

class Majalah(ItemPerpustakaan):
    def __init__(self, id, judul, nomor_edisi, tanggal_publikasi):
        super().__init__(id, judul)
        self._nomor_edisi = nomor_edisi
        self._tanggal_publikasi = tanggal_publikasi

    def tampilkan_info(self):
        return f"ID Majalah: {self._id}, Judul: {self._judul}, Edisi: {self._nomor_edisi}, Tanggal: {self._tanggal_publikasi}"

class Perpustakaan:
    def __init__(self):
        self.__item = []

    def tambah_item(self, item):
        if isinstance(item, ItemPerpustakaan):
            self.__item.append(item)
            print("Item berhasil ditambahkan.")
        else:
            print("Item harus merupakan instance dari ItemPerpustakaan.")

    def tampilkan_item(self):
        if not self.__item:
            print("Tidak ada item di perpustakaan.")
            return
        print("\nDaftar Item di Perpustakaan:")
        for item in self.__item:
            print(item.tampilkan_info())

    def cari_berdasarkan_judul(self, judul):
        results = [item for item in self.__item if item.judul.lower() == judul.lower()]
        return results

    def cari_berdasarkan_id(self, id):
        results = [item for item in self.__item if item._id == id]
        return results

def main():
    perpustakaan = Perpustakaan()

    while True:
        print("\nSistem Manajemen Perpustakaan")
        print("1. Tambah Buku")
        print("2. Tambah Majalah")
        print("3. Tampilkan Daftar Item")
        print("4. Cari Item berdasarkan Judul")
        print("5. Cari Item berdasarkan ID")
        print("6. Keluar")
        pilihan = input("Pilih menu (1-6): ")

        if pilihan == "1":
            id = input("Masukkan ID Buku: ")
            judul = input("Masukkan Judul Buku: ")
            penulis = input("Masukkan Penulis: ")
            try:
                tahun = int(input("Masukkan Tahun Terbit: "))
                buku = Buku(id, judul, penulis, tahun)
                perpustakaan.tambah_item(buku)
            except ValueError:
                print("Tahun harus berupa angka.")

        elif pilihan == "2":
            id = input("Masukkan ID Majalah: ")
            judul = input("Masukkan Judul Majalah: ")
            nomor_edisi = input("Masukkan Nomor Edisi: ")
            tanggal_publikasi = input("Masukkan Tanggal Publikasi: ")
            majalah = Majalah(id, judul, nomor_edisi, tanggal_publikasi)
            perpustakaan.tambah_item(majalah)

        elif pilihan == "3":
            perpustakaan.tampilkan_item()

        elif pilihan == "4":
            judul = input("Masukkan Judul yang dicari: ")
            results = perpustakaan.cari_berdasarkan_judul(judul)
            if results:
                print(f"\nHasil pencarian untuk judul '{judul}':")
                for item in results:
                    print(item.tampilkan_info())
            else:
                print(f"Tidak ada item dengan judul '{judul}'.")

        elif pilihan == "5":
            id = input("Masukkan ID yang dicari: ")
            results = perpustakaan.cari_berdasarkan_id(id)
            if results:
                print(f"\nHasil pencarian untuk ID '{id}':")
                for item in results:
                    print(item.tampilkan_info())
            else:
                print(f"Tidak ada item dengan ID '{id}'.")

        elif pilihan == "6":
            print("Terima kasih telah menggunakan sistem ini.")
            break

        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()