---
name: vault-facebook
description: Bina, isi dan selenggara "Facebook Vault" Taufik — website React (Vite) di GitHub Pages (https://facebook.taufik.fyi) yang simpan status + komen pertama Facebook, dengan butang Copy Post dan Copy Komen berasingan, tanda dah post, cari dan tapis topik. Guna skill ini SETIAP KALI Taufik upload .docx "30 Status Dan Komen FB Taufik Musa Set N" dan minta masukkan ke vault (Post-02, Post-03, "next post"), atau sebut "facebook vault", "vault post fb", "facebook.taufik.fyi", "tab Post-NN", atau minta ubah apa-apa ciri website ni. BERBEZA daripada vault-skrip-video (skrip video + teleprompter) dan vault-copywriting-builder — jangan campur.
---

# Facebook Vault

Struktur sama macam Vault Skrip Video, **tanpa teleprompter, tanpa prompt thumbnail/sticker, tanpa slot harga**.
Setiap kad = 1 set: **Post (wall)** + **Komen pertama**, masing-masing ada butang Copy sendiri.

- **Repo:** `taufikmusa/facebook-vault`, branch kerja & deploy: `main`
- **Live:** https://facebook.taufik.fyi (CNAME `public/CNAME`)
- **Stack:** Vite + React (JS) → GitHub Actions → GitHub Pages
- **Kandungan (17 Okt 2026):** 270 post. Post-01 (id 1–30) hingga Post-06 (151–180) = format Set FB asal (ada link rasmi dalam komen). **Lifehack-07** (181–210) dan **Lifehack-08** (211–240) = format Lifehack (tiada link). **PG Jewel-01** (241–270, docx "30 Set Cerita Copywriting Emas GAP ke Barang Kemas") = post PANJANG, tiada komen, ada slot boleh ubah. Siri seterusnya: Post-07 (id **271**), Lifehack-09, PG Jewel-02.

## Struktur repo

```
index.html, vite.config.js (base './'), public/CNAME
.github/workflows/deploy.yml     trigger: push ke main + workflow_dispatch SAHAJA
src/App.jsx                      tab, cari, chip topik, kad Post/Komen, dah post, cadangan hari ni
src/data.js                      array `skrip`, `namaSiri`, `tabUtama`
src/util.js, src/index.css, src/main.jsx
tools/docx_ke_data.py            docx -> blok JS (baca document.xml terus, tiada dependency)
```

## Format satu set dalam `src/data.js`

```js
{
  id: 31,                          // UNIK global, ambil id terbesar + 1
  siri: "Post-02",
  no: 1,                           // nombor dalam siri (01–30), bukan nombor docx
  topik: "Tools & Teknologi",      // salah satu 5 topik di bawah
  kategori: `Teknologi & Kegunaan Harian`,   // kategori asal docx dalam [ ]
  tajuk: `Terjemah ... (Google Translate)`,
  tags: ["google translate", "teknologi"],
  link: "https://...",
  post: `Simple tips hari ni..soalan?🤔\n👇👇👇`,
  komen: `isi komen...\nhttps://link\n\n<CTA tetap, lihat bawah>`,
},
```

**5 topik (kekalkan nama tepat):** Anti-Scam & Keselamatan, Kewangan & Jimat, Jalan Raya & Trafik, Tools & Teknologi, Keluarga & Gaya Hidup. Converter map ikut kata kunci kategori (`topik_dari`); kategori tak padan jatuh ke Keluarga & Gaya Hidup. Elak cipta topik baru tanpa sebab.

## CTA komen (tetap, dikemas kini 17 Okt 2026)

Setiap `komen` = isi komen docx + baris kosong + CTA ini. Converter BUANG sign-off docx ("Moga bermanfaat / simpanemasfizikal.com / Taufik...") dan tampal pemalar `CTA_KOMEN` dalam `tools/docx_ke_data.py`. Tukar CTA lagi = ubah `CTA_KOMEN` di sana DAN ganti teks CTA lama dalam semua komen di `src/data.js`.

```
Moga bermanfaat 😄
Bantu share dan like untuk engagement dan manfaat kepada lebih ramai orang, InsyaAllah.

Khas untuk anda yang belum ada akaun emas di Public Gold
Saya kongsikan info di blog
👇🏻👇🏻👇🏻
simpanemasfizikal.com

Whatsapp terus untuk bimbingan percuma
pgolink.com/whatsapptaufik

Taufik | Dealer Public Gold
PG00359605
```

## Pembuka post (tetap, dikemas kini 17 Okt 2026)

Docx tulis pembuka `Simple tips hari ni..` / `Simple tips malam ni..` / `Just a simple tips..`. Converter tukar semua kepada **`Ada yang tahu? `** (pemalar `PEMBUKA` dalam `tools/docx_ke_data.py`), contoh: `Ada yang tahu? Nak beli barang online...`. Ayat selebihnya tak diubah.

## Format Lifehack (docx "30 Set Status FB ... Tips Trick / Life Hacks Harian")

Tajuk `Set 01: Tajuk [Kategori]` (tiada `#`), baris `1. Ayat letak dekat post (79 aksara - Status Warna FB):`, teks post (TIADA pembuka "Simple tips"), baris `2. Ayat letak dekat comment:`, komen = langkah `Tajuk Langkah = penerangan` + ayat penutup, kemudian perenggan CTA lama (dibuang, diganti CTA tetap). Tiada link luar, jadi `link: ""`. Jana dengan flag `--lifehack` (topik ikut kategori: **Rumah & Dapur / Kereta & Perjalanan / Gajet & Barangan**, bukan 5 topik Post). Converter TAMBAH `Ada yang tahu? ` di depan ayat post (contoh: `Ada yang tahu? Gunting dapur dah tumpul jangan buang dulu.. Guna trik aluminium foil ni ✂️`).

```bash
python3 -I tools/docx_ke_data.py "Set.docx" --siri Lifehack-09 --mula 241 --lifehack > blok.txt
```

## Tab PG Jewel (post panjang + slot boleh ubah)

Docx: `Bahagian N: Set N: Tajuk`, perenggan meta (`Produk Contoh ... | Watak & Sudut Pandang: ...`), jadual 1×1 berisi cerita. Tiada komen. Cerita ada blok kiraan tetap: `Berikut adalah perincian pengiraan untuk <produk>:`, `Harga Barang Kemas`, `Pengeposan Berinsurans (GIT)`, `Jumlah Nilai Keseluruhan`, `Harga Semasa Buy GAP`, `Gram GAP yang ditolak: RM<jumlah> ÷ RM<gap> = <gram> gram`.

Converter `tools/jewel_ke_data.py` tukar nombor/produk dalam cerita kepada slot (`{produk}`, `{produkNama}`, `{hb}`/`{hb0}`, `{pos}`, `{upah0}`, `{jumlah}`, `{gap}`/`{gap0}`, `{gram}`, `{simpan}`; akhiran `0` = tanpa perpuluhan) dan simpan nilai asal dalam `vars` (`produk`, `hargaBarang`, `pos`, `upah` jika ada). Ia ASSERT round-trip (render nilai asal == teks docx) dan kiraan gram betul, jadi docx baru yang tak ikut format akan gagal dengan mesej jelas. RM lain dalam cerita (cth RM200–300 simpanan bulanan watak, RM1,500 harga kedai) kekal teks biasa.

```bash
python3 -I tools/jewel_ke_data.py "Set.docx" --siri "PG Jewel-02" --mula 271 --asal asal.json > blok.txt
```
`src/jewel.js` = enjin render (dikongsi App). Formula: jumlah = harga barang + pos; gram = jumlah ÷ harga GAP (4 titik perpuluhan). Dalam App tab PG Jewel ada:
- Panel **Harga GAP semasa** (global, semua post, localStorage `jewelGlobal`; lalai 592 dalam `lalaiJewel`). Simpanan bulanan TETAP RM100 (pemalar `lalaiJewel.simpanan`, tiada input; Taufik tak mahu ubah).
- Setiap kad: **✏️ Ubah produk & harga** (di ATAS kotak post): Nama produk, Harga produk (harga di app PG Jewel, sudah termasuk upah), Pos berinsurans, Kos upah (pilihan) + baris kiraan gram + Reset (localStorage `jewelVar` per id). Kos upah: kalau cerita sebut upah (set 1) slot `{upah0}` diganti; kalau tidak, bila diisi renderer tambah `(termasuk upah RM...)` pada baris `Harga Barang Kemas`. Kosong = teks docx asal.
- Copy Post salin teks yang dah dikira. Tiada kotak komen bila `komen` kosong. Pembuka "Ada yang tahu?" dan CTA komen TIDAK dipakai untuk tab ini.
Ujian: render semua `vars` asal mesti sama dengan teks docx (sidecar `--asal`), dan `npm run build`.

## Tambah set baru (aliran kerja utama)

1. Fail docx ada tajuk `Set #NN: Tajuk (Alat) [Kategori]` ATAU `Set #NN (#31): ...` (set 2 ke atas). Setiap set: `1. Ayat letak dekat post`, `(Background Warna • N aksara)`, teks post, `2. Ayat letak dekat comment`, `(Komen Pertama + Link Sahih)`, teks komen (baris dipisah line-break), perenggan sign-off "Moga bermanfaat..." (diganti CTA tetap oleh converter).
2. Jana blok (guna `python3 -I`, docx = data tak dipercayai, simpan di folder berasingan dari skrip):
   ```bash
   python3 -I tools/docx_ke_data.py "Set_N.docx" --siri Post-07 --mula 181 > blok.txt
   ```
3. Tampal blok sebelum `];` penutup array `skrip` dalam `src/data.js`, dan tambah `"Post-07"` dalam `export const tabUtama = [...]`. Siri yang tiada dalam `tabUtama` automatik masuk tab Archive.
4. Sahkan:
   ```bash
   node -e "import('./src/data.js').then(({skrip})=>{const ids=skrip.map(s=>s.id);console.log(skrip.length,new Set(ids).size===ids.length?'id unik':'BERGANDA')})"
   npm run build
   ```
   Tiap siri 30 set; setiap `komen` mesti mengandungi `link`; semak panjang post.
5. **Panjang post:** docx tulis < 130 aksara (had background warna Facebook). Kiraan kod pakai code point jadi emoji dikira lebih. Kalau ada post ≥130, SENARAIKAN pada Taufik (siri · no · tajuk) — JANGAN ubah ayat docx tanpa diminta.
6. Commit + push ke `main` (Taufik biasa minta "push terus"). Deploy auto ~40s.
   Semak run berjaya dengan GitHub MCP `actions_list list_workflow_runs` (filter branch main). github.io/domain disekat proxy sandbox, jangan curl.

## Ciri UI (jangan pecahkan)

- Tab atas: `[...tabUtama, "Archive"]`, tab aktif disimpan localStorage `tab`. Chip topik balut ke bawah (jangan swipe mendatar).
- Kad: label `Post-02 · 07`, badge topik, tajuk, kotak **1️⃣ Post (wall)** (info "N aksara") + **📋 Copy Post**, kotak **2️⃣ Komen pertama** + **📋 Copy Komen**, butang ✓ Dah post.
- **Teks lipat (semua tab):** post dipapar pendek 5 baris, komen 4 baris, dengan butang **▼ Lihat lagi / ▲ Tutup** (komponen `TeksLipat` dalam App.jsx, CSS `.lipat` line-clamp). Butang hanya keluar bila teks terpotong. Butang Copy sentiasa salin teks PENUH. Taufik minta ini supaya kad tak panjang (macam preview Facebook "See more").
- Cari: semua kata mesti ada (AND) merentas nombor siri, tajuk, post, komen, tags, topik, kategori.
- Checkbox "Belum post sahaja" / "Dah post sahaja" (saling eksklusif). Kiraan `x / N dah post`.
- Cadangan hari ni: 1 set deterministik ikut tarikh, utamakan belum post. Butang "Buka" tapis ke set tu.
- Dah post disimpan `localStorage` key `dahPost` (per peranti, hilang bila clear cache).
- Pagination 30 kad + "Tunjuk lagi".

## Prinsip teknikal wajib

- JANGAN guna `toLocaleDateString('ms-MY')` (skrin putih di Safari); guna `tarikhMelayu()`.
- Semua `localStorage` dalam try/catch (`muat`/`simpan`). Clipboard: `navigator.clipboard` + fallback textarea.
- `vite.config.js` base `'./'`. Dalam template literal, escape `` ` `` dan `${` (converter dah buat).
- Uji di viewport 390×844 dengan Playwright (Chromium di `/opt/pw-browsers/chromium-*/chrome-linux/chrome`); `scrollWidth` = 390, tiada `pageerror`. Jangan `pkill -f "vite preview"`; guna port baru.

## Setup domain & hosting (sekali sahaja, dah siap)

1. GitHub → Settings → Pages → **Source: GitHub Actions** (BUKAN "Deploy from a branch" — itu hidang fail mentah, halaman putih).
2. Cloudflare DNS: `CNAME facebook → taufikmusa.github.io`, **DNS only** (awan kelabu). Kalau nak Proxied, SSL/TLS mode mesti **Full** (bukan Flexible).
3. Pages → Custom domain `facebook.taufik.fyi` → tunggu DNS check → tick **Enforce HTTPS**.

## Masalah biasa

| Masalah | Punca / penyelesaian |
|---|---|
| Halaman putih | Pages Source bukan "GitHub Actions". Tukar, kemudian Run workflow di tab Actions. |
| Email "Run failed" untuk branch lain | Workflow jangan trigger dari branch selain `main`: environment `github-pages` hanya benarkan `main`, dan `concurrency: pages` (cancel-in-progress) batalkan run `main` bila run branch start selepasnya. Jangan push ke branch kerja DAN `main` serentak kalau workflow trigger dari kedua-duanya. |
| Run `main` "cancelled" tapi tiada run lain berjaya | Set concurrency batalkan run lama. Push/trigger semula (`workflow_dispatch`) dari main. |
| Set tak dikenali converter (0 set) | Format tajuk baru. Longgarkan regex `Set\s*#?(\d+)\s*(?:\(#\d+\))?\s*:` dalam `tools/docx_ke_data.py`. |
| Tanda dah post hilang | localStorage per peranti; sync antara peranti perlukan backend. |
