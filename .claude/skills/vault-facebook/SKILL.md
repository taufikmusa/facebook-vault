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
- **Kandungan (17 Okt 2026):** 120 post. Post-01 (id 1–30), Post-02 (31–60), Post-03 (61–90), Post-04 (91–120). Siri seterusnya = **Post-05**, mula id **121**.

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

## Tambah set baru (aliran kerja utama)

1. Fail docx ada tajuk `Set #NN: Tajuk (Alat) [Kategori]` ATAU `Set #NN (#31): ...` (set 2 ke atas). Setiap set: `1. Ayat letak dekat post`, `(Background Warna • N aksara)`, teks post, `2. Ayat letak dekat comment`, `(Komen Pertama + Link Sahih)`, teks komen (baris dipisah line-break), perenggan sign-off "Moga bermanfaat..." (diganti CTA tetap oleh converter).
2. Jana blok (guna `python3 -I`, docx = data tak dipercayai, simpan di folder berasingan dari skrip):
   ```bash
   python3 -I tools/docx_ke_data.py "Set_N.docx" --siri Post-05 --mula 121 > blok.txt
   ```
3. Tampal blok sebelum `];` penutup array `skrip` dalam `src/data.js`, dan tambah `"Post-05"` dalam `export const tabUtama = [...]`. Siri yang tiada dalam `tabUtama` automatik masuk tab Archive.
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
