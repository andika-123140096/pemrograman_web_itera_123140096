class DashboardManager {
  constructor() {
    this.jadwal = []
    this.tugas = []
    this.catatan = []
    this.loadData()
    this.initEventListeners()
    this.updateTimeAndWeather()
    this.renderAll()
  }

  loadData = async () => {
    const jadwalData = localStorage.getItem("jadwal")
    const tugasData = localStorage.getItem("tugas")
    const catatanData = localStorage.getItem("catatan")

    this.jadwal = jadwalData ? JSON.parse(jadwalData) : []
    this.tugas = tugasData ? JSON.parse(tugasData) : []
    this.catatan = catatanData ? JSON.parse(catatanData) : []
  }

  saveData = () => {
    localStorage.setItem("jadwal", JSON.stringify(this.jadwal))
    localStorage.setItem("tugas", JSON.stringify(this.tugas))
    localStorage.setItem("catatan", JSON.stringify(this.catatan))
  }

  fetchWeather = async () => {
    try {
      const response = await fetch("https://wttr.in/?format=%C+%t")
      const weather = await response.text()
      return weather
    } catch (error) {
      console.error("Error fetching weather:", error)
      return "Weather unavailable"
    }
  }

  initEventListeners() {
    document.getElementById("tambah-jadwal").addEventListener("click", () => this.addJadwal())
    document.getElementById("tambah-tugas").addEventListener("click", () => this.addTugas())
    document.getElementById("tambah-catatan").addEventListener("click", () => this.addCatatan())
  }

  addJadwal() {
    const mataKuliah = document.getElementById("jadwal-mata-kuliah").value.trim()
    const hari = document.getElementById("jadwal-hari").value
    const waktu = document.getElementById("jadwal-waktu").value
    const ruangan = document.getElementById("jadwal-ruangan").value.trim()

    if (!mataKuliah || !hari || !waktu || !ruangan) {
      alert("Semua field harus diisi!")
      return
    }

    const newJadwal = { mataKuliah, hari, waktu, ruangan, id: Date.now() }
    this.jadwal.push(newJadwal)
    this.saveData()
    this.renderJadwal()
    document.getElementById("jadwal-form").reset()
  }

  addTugas() {
    const judul = document.getElementById("tugas-judul").value.trim()
    const deskripsi = document.getElementById("tugas-deskripsi").value.trim()
    const deadline = document.getElementById("tugas-deadline").value

    if (!judul || !deskripsi || !deadline) {
      alert("Semua field harus diisi!")
      return
    }

    const newTugas = { judul, deskripsi, deadline, status: "Belum Selesai", id: Date.now() }
    this.tugas.push(newTugas)
    this.saveData()
    this.renderTugas()
    document.getElementById("tugas-form").reset()
  }

  addCatatan() {
    const judul = document.getElementById("catatan-judul").value.trim()
    const isi = document.getElementById("catatan-isi").value.trim()

    if (!judul || !isi) {
      alert("Semua field harus diisi!")
      return
    }

    const newCatatan = { judul, isi, id: Date.now() }
    this.catatan.push(newCatatan)
    this.saveData()
    this.renderCatatan()
    document.getElementById("catatan-form").reset()
  }

  deleteJadwal(id) {
    this.jadwal = this.jadwal.filter((item) => item.id !== id)
    this.saveData()
    this.renderJadwal()
  }

  deleteTugas(id) {
    this.tugas = this.tugas.filter((item) => item.id !== id)
    this.saveData()
    this.renderTugas()
  }

  deleteCatatan(id) {
    this.catatan = this.catatan.filter((item) => item.id !== id)
    this.saveData()
    this.renderCatatan()
  }

  toggleTugasStatus(id) {
    const tugas = this.tugas.find((item) => item.id === id)
    if (tugas) {
      tugas.status = tugas.status === "Belum Selesai" ? "Selesai" : "Belum Selesai"
      this.saveData()
      this.renderTugas()
    }
  }

  renderJadwal() {
    const table = document.getElementById("jadwal-table")
    while (table.rows.length > 1) {
      table.deleteRow(1)
    }
    this.jadwal.forEach((item) => {
      const row = table.insertRow()
      row.innerHTML = `
        <td>${item.mataKuliah}</td>
        <td>${item.hari}</td>
        <td>${item.waktu}</td>
        <td>${item.ruangan}</td>
        <td><button onclick="dashboard.deleteJadwal(${item.id})">Hapus</button></td>
      `
    })
  }

  renderTugas() {
    const table = document.getElementById("tugas-table")
    while (table.rows.length > 1) {
      table.deleteRow(1)
    }
    this.tugas.forEach((item) => {
      const row = table.insertRow()
      row.innerHTML = `
        <td>${item.judul}</td>
        <td>${item.deskripsi}</td>
        <td>${item.deadline}</td>
        <td>${item.status}</td>
        <td>
          <button onclick="dashboard.toggleTugasStatus(${item.id})">Toggle Status</button>
          <button onclick="dashboard.deleteTugas(${item.id})">Hapus</button>
        </td>
      `
    })
  }

  renderCatatan() {
    const table = document.getElementById("catatan-table")
    while (table.rows.length > 1) {
      table.deleteRow(1)
    }
    this.catatan.forEach((item) => {
      const row = table.insertRow()
      row.innerHTML = `
        <td>${item.judul}</td>
        <td>${item.isi}</td>
        <td><button onclick="dashboard.deleteCatatan(${item.id})">Hapus</button></td>
      `
    })
  }

  renderAll() {
    this.renderJadwal()
    this.renderTugas()
    this.renderCatatan()
  }

  async updateTimeAndWeather() {
    const display = document.getElementById("time-weather-display")
    const update = async () => {
      const now = new Date()
      const time = now.toLocaleTimeString()
      const weather = await this.fetchWeather()
      display.innerHTML = `Waktu: ${time}<br>Cuaca: ${weather}`
    }
    update()
    setInterval(update, 60000)
  }
}

const dashboard = new DashboardManager()
