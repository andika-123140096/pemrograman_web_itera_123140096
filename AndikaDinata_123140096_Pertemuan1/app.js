const tabelTugas = document.getElementById("tabelTugas")
const tombolTambahTugas = document.getElementById("tombolTambahTugas")
const pesanPemberitahuan = document.getElementById("pesanPemberitahuan")
const jumlahTugasBelumSelesai = document.getElementById("taskCounter")
const filterStatus = document.getElementById("filterStatus")
const cariMataKuliah = document.getElementById("cariMataKuliah")
const applyFilterButton = document.getElementById("applyFilterButton")
const resetFilterButton = document.getElementById("resetFilterButton")

function loadTugas() {
  const tugas = JSON.parse(localStorage.getItem("tasks")) || []
  clearTable()
  for (let i = 0; i < tugas.length; i++) {
    addTaskToTable(tugas[i].judul, tugas[i].deskripsi, tugas[i].mataKuliah, tugas[i].deadline, tugas[i].status)
  }
  updateJumlahTugasBelumSelesai()
}

function clearTable() {
  while (tabelTugas.rows.length > 1) {
    tabelTugas.deleteRow(1)
  }
}

function saveTugas() {
  const tugas = []
  for (let i = 1; i < tabelTugas.rows.length; i++) {
    const row = tabelTugas.rows[i]
    tugas.push({
      judul: row.cells[0].innerHTML,
      deskripsi: row.cells[1].innerHTML,
      mataKuliah: row.cells[2].innerHTML,
      deadline: row.cells[3].innerHTML,
      status: row.cells[4].innerHTML,
    })
  }
  localStorage.setItem("tasks", JSON.stringify(tugas))
}

function addTaskToTable(judul, deskripsi, mataKuliah, deadline, status = "Belum Selesai") {
  const row = tabelTugas.insertRow()
  const cell1 = row.insertCell(0)
  const cell2 = row.insertCell(1)
  const cell3 = row.insertCell(2)
  const cell4 = row.insertCell(3)
  const cell5 = row.insertCell(4)
  const cell6 = row.insertCell(5)

  cell1.innerHTML = judul
  cell2.innerHTML = deskripsi
  cell3.innerHTML = mataKuliah
  cell4.innerHTML = deadline
  cell5.innerHTML = status
  cell6.innerHTML = `<button onclick="hapusTugas(this)">Hapus</button>`
  cell6.innerHTML += `<button onclick="ubahStatusTugas(this)">Ubah Status</button>`
}

function updateJumlahTugasBelumSelesai() {
  const tugas = JSON.parse(localStorage.getItem("tasks")) || []
  let belumSelesai = 0
  for (let i = 0; i < tugas.length; i++) {
    if (tugas[i].status === "Belum Selesai") {
      belumSelesai++
    }
  }
  jumlahTugasBelumSelesai.innerHTML = `Jumlah Tugas Belum Selesai: ${belumSelesai}`
}

function tambahTugasBaru() {
  const judul = document.getElementById("judul").value.trim()
  const deskripsi = document.getElementById("deskripsi").value.trim()
  const mataKuliah = document.getElementById("mata-kuliah").value.trim()
  const deadline = document.getElementById("deadline").value

  if (!judul) {
    pesanPemberitahuan.innerHTML = "Judul tugas tidak boleh kosong."
    pesanPemberitahuan.style.color = "red"
    return
  } else if (!deskripsi) {
    pesanPemberitahuan.innerHTML = "Deskripsi tugas tidak boleh kosong."
    pesanPemberitahuan.style.color = "red"
    return
  } else if (!mataKuliah) {
    pesanPemberitahuan.innerHTML = "Mata kuliah tidak boleh kosong."
    pesanPemberitahuan.style.color = "red"
    return
  } else if (!deadline) {
    pesanPemberitahuan.innerHTML = "Deadline tugas tidak boleh kosong."
    pesanPemberitahuan.style.color = "red"
    return
  }

  const deadlineDate = new Date(deadline)
  const now = new Date()
  if (deadlineDate < now) {
    pesanPemberitahuan.innerHTML = "Deadline tidak boleh di masa lalu."
    pesanPemberitahuan.style.color = "red"
    return
  }

  addTaskToTable(judul, deskripsi, mataKuliah, deadline)
  saveTugas()
  updateJumlahTugasBelumSelesai()
  document.getElementById("tambahTugasForm").reset()
  pesanPemberitahuan.innerHTML = "Tugas berhasil ditambahkan."
  pesanPemberitahuan.style.color = "green"
}

function hapusTugas(button) {
  const row = button.parentNode.parentNode
  tabelTugas.deleteRow(row.rowIndex)
  saveTugas()
  updateJumlahTugasBelumSelesai()
}

function ubahStatusTugas(button) {
  const row = button.parentNode.parentNode
  const statusCell = row.cells[4]

  if (statusCell.innerHTML === "Belum Selesai") {
    statusCell.innerHTML = "Selesai"
  } else {
    statusCell.innerHTML = "Belum Selesai"
  }
  saveTugas()
  updateJumlahTugasBelumSelesai()
}

function applyFilter() {
  const tugas = JSON.parse(localStorage.getItem("tasks")) || []
  const statusFilter = filterStatus.value
  const mataKuliahYangDicari = cariMataKuliah.value.toLowerCase().trim()

  clearTable()

  const filteredTugas = []
  for (let i = 0; i < tugas.length; i++) {
    let matchStatus
    let matchMataKuliah

    if (statusFilter === "Semua") {
      matchStatus = true
    } else {
      matchStatus = tugas[i].status === statusFilter
    }

    if (!mataKuliahYangDicari) {
      matchMataKuliah = true
    } else {
      matchMataKuliah = tugas[i].mataKuliah.toLowerCase().includes(mataKuliahYangDicari)
    }

    if (matchStatus && matchMataKuliah) {
      filteredTugas.push(tugas[i])
    }
  }

  for (let i = 0; i < filteredTugas.length; i++) {
    addTaskToTable(filteredTugas[i].judul, filteredTugas[i].deskripsi, filteredTugas[i].mataKuliah, filteredTugas[i].deadline, filteredTugas[i].status)
  }
}

function resetFilter() {
  filterStatus.value = "Semua"
  cariMataKuliah.value = ""
  loadTugas()
}

tombolTambahTugas.addEventListener("click", tambahTugasBaru)
applyFilterButton.addEventListener("click", applyFilter)
resetFilterButton.addEventListener("click", resetFilter)
loadTugas()
