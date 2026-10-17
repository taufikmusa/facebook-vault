# Facebook Vault

Vault post + komen pertama Facebook untuk Taufik. Struktur sama macam Vault Skrip Video, **tanpa teleprompter**.
Setiap kad ada 2 kotak: **Post (wall)** dan **Komen pertama**, masing-masing ada butang Copy.

- Tab `Post-01` = 30 set dari docx "30 Koleksi Status & Komen Facebook (Set 1)"
- Stack: Vite + React → GitHub Pages (GitHub Actions)
- Domain: **facebook.taufik.fyi** (fail `public/CNAME`)

## Tambah set baru (Post-02, dst.)

```bash
python3 tools/docx_ke_data.py "Set_2.docx" --siri Post-02 --mula 31 > /tmp/blok.txt
```
Tampal blok sebelum `];` dalam `src/data.js`, tambah `"Post-02"` dalam `tabUtama`, `npm run build`, push.

## Setup subdomain facebook.taufik.fyi (Cloudflare + GitHub Pages)

1. **GitHub** → repo `facebook-vault` → Settings → Pages → Source: **GitHub Actions**.
2. Pastikan branch yang deploy ialah branch default (merge ke `main`), atau tambah branch tu dalam Settings → Environments → `github-pages`.
3. **Cloudflare** → domain `taufik.fyi` → DNS → Add record:
   - Type: `CNAME`
   - Name: `facebook`
   - Target: `taufikmusa.github.io`
   - Proxy status: **DNS only** (awan kelabu) dulu
4. **GitHub** → Settings → Pages → Custom domain: `facebook.taufik.fyi` → Save. Tunggu check DNS hijau, kemudian tick **Enforce HTTPS**.
5. (Pilihan) Lepas HTTPS aktif, boleh tukar ke Proxied (awan oren). Kalau buat, Cloudflare SSL/TLS mode mesti **Full** — jangan Flexible (redirect loop).
6. Buka https://facebook.taufik.fyi
