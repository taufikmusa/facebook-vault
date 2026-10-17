// Tab PG Jewel: post panjang dengan slot {hb}, {pos}, {jumlah}, {gap}, {gram}, {produk} dsb.
// Nilai asal setiap post disimpan dalam `vars`; harga GAP & simpanan bulanan dikongsi (global).
// Taufik tukar nilai di ruangan khas, post dikira semula di sini.

export const lalaiJewel = { hargaGAP: "592", simpanan: "100", tarikh: "" }

const nombor = v => {
  const n = parseFloat(String(v ?? "").replace(/,/g, ""))
  return Number.isFinite(n) ? n : 0
}

// 1663 -> "1,663.00" (dp=2) / "1,663" (dp=0). Tak guna toLocaleString supaya sama di semua pelayar.
export function format(n, dp) {
  const [i, d] = n.toFixed(dp).split(".")
  return i.replace(/\B(?=(\d{3})+$)/g, ",") + (d ? "." + d : "")
}

// Nilai terkira untuk satu post: jumlah = harga barang + pos, gram = jumlah / harga GAP
export function kira(vars, global) {
  const hb = nombor(vars.hargaBarang)
  const pos = nombor(vars.pos)
  const upah = nombor(vars.upah)
  const gap = nombor(global.hargaGAP) || nombor(lalaiJewel.hargaGAP)
  const jumlah = hb + pos
  return { hb, pos, upah, gap, jumlah, gram: gap ? jumlah / gap : 0 }
}

export function renderJewel(s, ubahan, global) {
  const vars = { ...s.vars, ...(ubahan || {}) }
  const k = kira(vars, global)
  const produk = String(vars.produk || "")
  const val = {
    produk,
    produkNama: produk.replace(/\s*\([^)]*\)\s*$/, ""),
    hb: format(k.hb, 2), hb0: format(k.hb, 0),
    pos: format(k.pos, 2), pos0: format(k.pos, 0),
    upah: format(k.upah, 2), upah0: format(k.upah, 0),
    jumlah: format(k.jumlah, 2), jumlah0: format(k.jumlah, 0),
    gap: format(k.gap, 2), gap0: format(k.gap, 0),
    gram: k.gram.toFixed(4),
    simpan: format(nombor(global.simpanan) || nombor(lalaiJewel.simpanan), 0),
  }
  // fungsi (bukan string) supaya `$` dalam nilai tak ditafsir sebagai corak ganti
  return s.post.replace(/\{(\w+)\}/g, (m, k2) => (k2 in val ? val[k2] : m))
}
