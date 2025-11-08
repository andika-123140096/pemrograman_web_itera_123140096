mahasiswa = [
    {"nama": "Andi", "nim": "12345678", "nilai_uts": 85, "nilai_uas": 90, "nilai_tugas": 88},
    {"nama": "Budi", "nim": "12345679", "nilai_uts": 78, "nilai_uas": 82, "nilai_tugas": 80},
    {"nama": "Citra", "nim": "12345680", "nilai_uts": 92, "nilai_uas": 88, "nilai_tugas": 95},
    {"nama": "Dewi", "nim": "12345681", "nilai_uts": 65, "nilai_uas": 70, "nilai_tugas": 68},
    {"nama": "Eko", "nim": "12345682", "nilai_uts": 55, "nilai_uas": 60, "nilai_tugas": 58}
]

def hitung_nilai_akhir(uts, uas, tugas):
    return (0.3 * uts) + (0.4 * uas) + (0.3 * tugas)

def tentukan_grade(nilai_akhir):
    if nilai_akhir >= 80:
        return 'A'
    elif nilai_akhir >= 70:
        return 'B'
    elif nilai_akhir >= 60:
        return 'C'
    elif nilai_akhir >= 50:
        return 'D'
    else:
        return 'E'

def tampilkan_tabel():
    print("\n{:<20} {:<10} {:<8} {:<8} {:<10} {:<12} {:<5}".format("Nama", "NIM", "UTS", "UAS", "Tugas", "Nilai Akhir", "Grade"))
    print("-" * 80)
    for mhs in mahasiswa:
        nilai_akhir = hitung_nilai_akhir(mhs["nilai_uts"], mhs["nilai_uas"], mhs["nilai_tugas"])
        grade = tentukan_grade(nilai_akhir)
        print("{:<20} {:<10} {:<8} {:<8} {:<10} {:<12.2f} {:<5}".format(
            mhs["nama"], mhs["nim"], mhs["nilai_uts"], mhs["nilai_uas"], mhs["nilai_tugas"], nilai_akhir, grade))

def cari_nilai_berdasarkan_tipe(tipe):
    if not mahasiswa:
        print("Tidak ada data mahasiswa.")
        return
    nilai_akhir_list = [(mhs, hitung_nilai_akhir(mhs["nilai_uts"], mhs["nilai_uas"], mhs["nilai_tugas"])) for mhs in mahasiswa]
    if tipe == "tertinggi":
        mhs_extrem = max(nilai_akhir_list, key=lambda x: x[1])
    elif tipe == "terendah":
        mhs_extrem = min(nilai_akhir_list, key=lambda x: x[1])
    else:
        print("Tipe tidak valid.")
        return
    print(f"Mahasiswa dengan nilai {tipe}: {mhs_extrem[0]['nama']} (NIM: {mhs_extrem[0]['nim']}) dengan nilai akhir {mhs_extrem[1]:.2f}")

def input_mahasiswa_baru():
    nama = input("Masukkan nama mahasiswa: ")
    nim = input("Masukkan NIM: ")
    try:
        uts = float(input("Masukkan nilai UTS: "))
        uas = float(input("Masukkan nilai UAS: "))
        tugas = float(input("Masukkan nilai Tugas: "))
        mahasiswa.append({"nama": nama, "nim": nim, "nilai_uts": uts, "nilai_uas": uas, "nilai_tugas": tugas})
        print("Data mahasiswa berhasil ditambahkan.")
    except ValueError:
        print("Input nilai harus berupa angka.")

def filter_berdasarkan_grade(grade):
    filtered = []
    for mhs in mahasiswa:
        nilai_akhir = hitung_nilai_akhir(mhs["nilai_uts"], mhs["nilai_uas"], mhs["nilai_tugas"])
        if tentukan_grade(nilai_akhir) == grade.upper():
            filtered.append(mhs)
    if filtered:
        print(f"\nMahasiswa dengan grade {grade.upper()}:")
        for mhs in filtered:
            nilai_akhir = hitung_nilai_akhir(mhs["nilai_uts"], mhs["nilai_uas"], mhs["nilai_tugas"])
            print(f"- {mhs['nama']} (NIM: {mhs['nim']}) - Nilai Akhir: {nilai_akhir:.2f}")
    else:
        print(f"Tidak ada mahasiswa dengan grade {grade.upper()}.")

def hitung_rata_rata():
    if not mahasiswa:
        print("Tidak ada data mahasiswa.")
        return
    total = sum(hitung_nilai_akhir(mhs["nilai_uts"], mhs["nilai_uas"], mhs["nilai_tugas"]) for mhs in mahasiswa)
    rata_rata = total / len(mahasiswa)
    print(f"Rata-rata nilai kelas: {rata_rata:.2f}")

while True:
    print("\nProgram Pengelolaan Data Nilai Mahasiswa")
    print("1. Tampilkan data mahasiswa")
    print("2. Cari mahasiswa dengan nilai tertinggi")
    print("3. Cari mahasiswa dengan nilai terendah")
    print("4. Tambah mahasiswa baru")
    print("5. Filter mahasiswa berdasarkan grade")
    print("6. Hitung rata-rata nilai kelas")
    print("7. Keluar")
    pilihan = input("Pilih menu (1-7): ")
    
    if pilihan == "1":
        tampilkan_tabel()
    if pilihan == "2":
        cari_nilai_berdasarkan_tipe("tertinggi")
    elif pilihan == "3":
        cari_nilai_berdasarkan_tipe("terendah")
    elif pilihan == "4":
        input_mahasiswa_baru()
    elif pilihan == "5":
        grade = input("Masukkan grade (A/B/C/D/E): ")
        filter_berdasarkan_grade(grade)
    elif pilihan == "6":
        hitung_rata_rata()
    elif pilihan == "7":
        print("Terima kasih telah menggunakan program ini.")
        break
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")