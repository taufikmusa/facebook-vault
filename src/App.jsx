import { useState, useMemo } from 'react'
import { skrip, namaSiri, tabUtama } from './data'
import { muat, simpan, salinKeClipboard, tarikhMelayu } from './util'

// Tab: setiap siri dalam tabUtama dapat tab sendiri, siri lain semua masuk "Archive"
const ARKIB = "Archive"
const TABS = [...tabUtama, ARKIB]
const tabKe = siri => (tabUtama.includes(siri) ? siri : ARKIB)
const unik = arr => Array.from(new Set(arr))
const nombor = s => `${s.siri} · ${String(s.no).padStart(2, "0")}`
const aksara = t => Array.from(t).length
const HAD_AWAL = 30

export default function App() {
  const [tab, setTab] = useState(() => {
    const t = muat("tab", { nama: TABS[0] }).nama
    return TABS.includes(t) ? t : TABS[0]
  })
  const [cari, setCari] = useState("")
  const [topik, setTopik] = useState("Semua")
  const [status, setStatus] = useState("semua")   // semua | belum | dah
  const [dahPost, setDahPost] = useState(() => muat("dahPost", {}))
  const [had, setHad] = useState(HAD_AWAL)
  const [disalin, setDisalin] = useState(null)    // "<id>post" | "<id>komen"

  const skripTab = useMemo(() => skrip.filter(s => tabKe(s.siri) === tab), [tab])
  const TOPIK = useMemo(() => ["Semua", ...unik(skripTab.map(s => s.topik))], [skripTab])
  const hariIni = useMemo(() => pilihHariIni(skripTab, dahPost), [skripTab, dahPost])

  function tukarTab(t) {
    setTab(t); setTopik("Semua"); setHad(HAD_AWAL)
    simpan("tab", { nama: t })
  }

  const senaraiPenuh = useMemo(() => {
    const kata = cari.trim().toLowerCase().split(/\s+/).filter(Boolean)
    return skripTab.filter(s => {
      if (topik !== "Semua" && s.topik !== topik) return false
      if (status === "belum" && dahPost[s.id]) return false
      if (status === "dah" && !dahPost[s.id]) return false
      if (kata.length === 0) return true
      const hay = [nombor(s), namaSiri[s.siri] || "", s.tajuk, s.post, s.komen, s.tags.join(" "), s.topik, s.kategori].join(" ").toLowerCase()
      return kata.every(k => hay.includes(k))   // semua kata kunci mesti ada
    })
  }, [skripTab, cari, topik, status, dahPost])

  const senarai = senaraiPenuh.slice(0, had)
  const skop = skripTab.filter(s => topik === "Semua" || s.topik === topik)
  const jumlahPost = skop.filter(s => dahPost[s.id]).length
  const tukarStatus = (nilai, on) => { setStatus(on ? nilai : "semua"); setHad(HAD_AWAL) }

  function salin(s, jenis) {
    salinKeClipboard(jenis === "post" ? s.post : s.komen).then(() => {
      setDisalin(s.id + jenis)
      setTimeout(() => setDisalin(null), 1500)
    })
  }
  function tukarPost(id) {
    setDahPost(prev => {
      const baru = { ...prev, [id]: !prev[id] }
      simpan("dahPost", baru)
      return baru
    })
  }

  return (
    <div className="app">
      <header className="header">
        <div className="wrap">
          <h1 className="logo">📘 Facebook Vault</h1>
          <p className="tagline">Salin post untuk wall, salin komen untuk komen pertama. Siap.</p>
        </div>
      </header>

      <nav className="tabs wrap">
        {TABS.map(t => (
          <button key={t} className={"tab" + (tab === t ? " aktif" : "") + (t === ARKIB ? " tab-arkib" : "")} onClick={() => tukarTab(t)}>
            {t === ARKIB ? "🗄 " : ""}{t}{namaSiri[t] ? ` · ${namaSiri[t]}` : ""}
            <span className="chip-n">{skrip.filter(s => tabKe(s.siri) === t).length}</span>
          </button>
        ))}
      </nav>

      <div className="wrap kawalan">
        {hariIni && (
          <div className="banner">
            <div>
              <div className="banner-tarikh">📅 {tarikhMelayu(new Date())}</div>
              <div className="banner-sub">Cadangan post hari ni: <b>{nombor(hariIni)} — {hariIni.tajuk}</b></div>
            </div>
            <button className="btn btn-emas" onClick={() => { setCari(nombor(hariIni).toLowerCase().replace(" · ", " ")); setHad(HAD_AWAL) }}>Buka</button>
          </div>
        )}

        <input
          className="search"
          type="search"
          placeholder={`🔍 Cari dalam ${tab}… (cth: scam, kwsp, post-01 07)`}
          value={cari}
          onChange={e => { setCari(e.target.value); setHad(HAD_AWAL) }}
        />
        <div className="chips">
          {TOPIK.map(k => (
            <button key={k} className={"chip" + (topik === k ? " aktif" : "")} onClick={() => { setTopik(k); setHad(HAD_AWAL) }}>
              {k} <span className="chip-n">{skripTab.filter(s => k === "Semua" || s.topik === k).length}</span>
            </button>
          ))}
        </div>
        <div className="toggles">
          <label className="toggle">
            <input type="checkbox" checked={status === "belum"} onChange={e => tukarStatus("belum", e.target.checked)} />
            <span>Belum post sahaja</span>
          </label>
          <label className="toggle">
            <input type="checkbox" checked={status === "dah"} onChange={e => tukarStatus("dah", e.target.checked)} />
            <span>Dah post sahaja</span>
          </label>
        </div>
        <div className="statbar">
          <span>Papar {senarai.length} dari {senaraiPenuh.length}</span>
          <span>{jumlahPost} / {skop.length} dah post ({tab})</span>
        </div>
      </div>

      <main className="wrap grid">
        {senarai.length === 0 && <p className="kosong">Tiada post yang padan. Cuba kata kunci lain.</p>}
        {senarai.map(s => (
          <article key={s.id} className={"kad" + (dahPost[s.id] ? " kad-rakam" : "")}>
            <div className="kad-atas">
              <span className="no">{nombor(s)}</span>
              <span className="badge">{s.topik}</span>
            </div>
            <h2 className="tajuk">{s.tajuk}</h2>

            <div className="kotak">
              <div className="kotak-kepala">
                <span className="kotak-label">1️⃣ Post (wall)</span>
                <span className="kotak-info">Background warna · {aksara(s.post)} aksara</span>
              </div>
              <div className="kotak-teks post">{s.post}</div>
              <button className={"btn btn-salin" + (disalin === s.id + "post" ? " ok" : "")} onClick={() => salin(s, "post")}>
                {disalin === s.id + "post" ? "✓ Post disalin!" : "📋 Copy Post"}
              </button>
            </div>

            <div className="kotak">
              <div className="kotak-kepala">
                <span className="kotak-label">2️⃣ Komen pertama</span>
                <span className="kotak-info">Letak lepas post naik</span>
              </div>
              <div className="kotak-teks">{s.komen}</div>
              <button className={"btn btn-salin" + (disalin === s.id + "komen" ? " ok" : "")} onClick={() => salin(s, "komen")}>
                {disalin === s.id + "komen" ? "✓ Komen disalin!" : "📋 Copy Komen"}
              </button>
            </div>

            <button className="btn btn-garis" onClick={() => tukarPost(s.id)}>
              {dahPost[s.id] ? "↩ Belum post" : "✓ Dah post"}
            </button>
            {dahPost[s.id] && <div className="cap-rakam">✓ Dah post</div>}
          </article>
        ))}
      </main>

      {senaraiPenuh.length > senarai.length && (
        <div className="wrap lagi">
          <button className="btn btn-garis" onClick={() => setHad(h => h + HAD_AWAL)}>
            ⬇ Tunjuk lagi ({senaraiPenuh.length - senarai.length} lagi)
          </button>
        </div>
      )}

      <footer className="footer">Facebook Vault · Taufik Musa · facebook.taufik.fyi</footer>
    </div>
  )
}

// Pilih 1 post hari ni (deterministik ikut tarikh, utamakan yang belum post)
function pilihHariIni(semua, dahPost) {
  if (semua.length === 0) return null
  const t = new Date()
  const benih = t.getFullYear() * 10000 + (t.getMonth() + 1) * 100 + t.getDate()
  const belum = semua.filter(s => !dahPost[s.id])
  const sumber = belum.length ? belum : semua
  const rng = n => { const x = Math.sin(n) * 10000; return x - Math.floor(x) }
  return [...sumber].sort((a, b) => rng(a.id + benih) - rng(b.id + benih))[0]
}
