// Fungsi kecil yang dikongsi. Semua akses localStorage dibungkus try/catch
// supaya app tak mati (skrin putih) kalau pelayar sekat storage.

export function muat(kunci, lalai) {
  try {
    const raw = localStorage.getItem(kunci)
    return raw ? { ...lalai, ...JSON.parse(raw) } : lalai
  } catch { return lalai }
}

export function simpan(kunci, nilai) {
  try { localStorage.setItem(kunci, JSON.stringify(nilai)) } catch {}
}

// Clipboard API perlukan HTTPS; fallback textarea untuk pelayar lama
export function salinKeClipboard(teks) {
  if (navigator.clipboard && window.isSecureContext) {
    return navigator.clipboard.writeText(teks).catch(() => salinLama(teks))
  }
  return Promise.resolve(salinLama(teks))
}
function salinLama(teks) {
  const ta = document.createElement("textarea")
  ta.value = teks
  ta.setAttribute("readonly", "")
  ta.style.position = "fixed"
  ta.style.opacity = "0"
  document.body.appendChild(ta)
  ta.select()
  try { document.execCommand("copy") } catch {}
  document.body.removeChild(ta)
}

export function kiraPatah(teks) {
  return teks.split(/\s+/).filter(Boolean).length
}

// Anggaran masa bacaan ~165 patah seminit (skrip 60 saat ≈ 160-165 patah)
export function anggarMasa(patah, ppm = 165) {
  const saat = Math.round((patah / ppm) * 60)
  if (saat < 60) return `~${saat}s`
  return `~${Math.floor(saat / 60)}m ${String(saat % 60).padStart(2, "0")}s`
}

// Tarikh Melayu manual. JANGAN guna toLocaleDateString('ms-MY') — throw error di Safari/iPhone.
export function tarikhMelayu(d) {
  const hari = ["Ahad", "Isnin", "Selasa", "Rabu", "Khamis", "Jumaat", "Sabtu"]
  const bulan = ["Januari", "Februari", "Mac", "April", "Mei", "Jun", "Julai", "Ogos", "September", "Oktober", "November", "Disember"]
  try {
    return `${hari[d.getDay()]}, ${d.getDate()} ${bulan[d.getMonth()]} ${d.getFullYear()}`
  } catch { return "" }
}
