// Tab PG Jewel: post panjang dengan slot {hb}, {pos}, {jumlah}, {gap}, {gram}, {produk} dsb.
// Nilai asal setiap post disimpan dalam `vars`; harga GAP dikongsi (global). Simpanan bulanan tetap RM100.
// Taufik tukar nilai di ruangan khas, post dikira semula di sini.

// Harga emas PG Sell (999) hari ini: baki gram GAP ditukar ke Cash Voucher pada harga ini bila tebus di PG Jewel
export const lalaiJewel = { hargaGAP: "588", simpanan: "100", tarikh: "Selasa, 20 Oktober 2026" }

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

// Slot dalam teks (post dan tajuk) diganti nilai semasa
export function renderJewel(s, ubahan, global, teks) {
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
    simpan: format(nombor(lalaiJewel.simpanan), 0),   // tetap RM100, tak diubah dari panel
  }
  let tpl = teks ?? s.post
  // Post yang tak sebut upah: bila kos upah diisi, tambah "(termasuk upah RM...)" pada baris harga barang
  if (k.upah > 0 && !/\{upah0?\}/.test(tpl)) {
    tpl = tpl.replace(/^(• Harga Barang Kemas: RM\{hb\})$/m, `$1 (termasuk upah RM${val.upah})`)
  }
  // fungsi (bukan string) supaya `$` dalam nilai tak ditafsir sebagai corak ganti
  return tpl.replace(/\{(\w+)\}/g, (m, k2) => (k2 in val ? val[k2] : m))
}
