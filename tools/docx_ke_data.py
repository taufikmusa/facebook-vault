#!/usr/bin/env python3
"""Tukar docx "Koleksi Status & Komen Facebook" -> blok JS untuk src/data.js.

Guna:  python3 tools/docx_ke_data.py fail.docx --siri Post-01 --mula 1 > /tmp/blok.txt
Tampal output sebelum `];` penutup array `skrip` dalam src/data.js.
Baca document.xml terus (tak perlu python-docx).
"""
import re, sys, zipfile, argparse, html

def para(p):
    p = re.sub(r'<w:br[^>]*/>', '\n', p)
    out = []
    for a, b in re.findall(r'<w:t[^>]*>(.*?)</w:t>|(\n)', p, flags=re.S):
        out.append(a or b)
    return html.unescape(''.join(out)).strip()

def topik_dari(kat):
    k = kat.lower()
    for kunci, nama in [
        ('keselamatan', 'Anti-Scam & Keselamatan'),
        ('kewangan', 'Kewangan & Jimat'), ('cukai', 'Kewangan & Jimat'),
        ('jimat', 'Kewangan & Jimat'), ('pendidikan', 'Kewangan & Jimat'),
        ('kenderaan', 'Jalan Raya & Trafik'), ('trafik', 'Jalan Raya & Trafik'),
        ('produktiviti', 'Tools & Teknologi'), ('edit', 'Tools & Teknologi'),
        ('reka', 'Tools & Teknologi'), ('kandungan', 'Tools & Teknologi'),
        ('teknologi', 'Tools & Teknologi'), ('internet', 'Tools & Teknologi'),
    ]:
        if kunci in k:
            return nama
    return 'Keluarga & Gaya Hidup'

CTA_KOMEN = """Moga bermanfaat 😄
Bantu share dan like untuk engagement dan manfaat kepada lebih ramai orang, InsyaAllah.

Khas untuk anda yang belum ada akaun emas di Public Gold
Saya kongsikan info di blog
👇🏻👇🏻👇🏻
simpanemasfizikal.com

Whatsapp terus untuk bimbingan percuma
pgolink.com/whatsapptaufik

Taufik | Dealer Public Gold
PG00359605"""

PEMBUKA = r'^(?:Just a simple tips|Simple tips (?:hari|malam) ni)\.\.[ ]?'   # "Simple tips hari ni.." dsb. -> "Ada yang tahu? "

def topik_lifehack(kat):
    k = kat.lower()
    if 'kereta' in k:
        return 'Kereta & Perjalanan'
    if 'gajet' in k or 'pakaian' in k or 'barangan' in k:
        return 'Gajet & Barangan'
    return 'Rumah & Dapur'

def topik_numbered(kat):
    k = kat.lower()
    for kunci, nama in [
        ('kecerdasan buatan', 'AI & Automasi'),
        ('penghasilan video', 'Video & Penjenamaan'), ('video, pembentangan', 'Video & Kandungan Kreatif'),
        ('reka bentuk lanjutan', 'Reka Bentuk Lanjutan'), ('reka bentuk grafik', 'Reka Bentuk & Visual'),
        ('pengurusan dokumen', 'Dokumen & Utiliti Pejabat'),
        ('produktiviti bisnes', 'Produktiviti & Keselamatan Siber'),
        ('perniagaan, pemasaran', 'Bisnes & Jualan Online'), ('pengurusan bisnes', 'Bisnes & E-Dagang'),
        ('utiliti komputer', 'Telefon, Komputer & Privasi'),
        ('pengurusan kewangan', 'Kewangan & Produktiviti Harian'), ('kewangan, gaya hidup', 'Kewangan & Gaya Hidup'),
    ]:
        if kunci in k:
            return nama
    return kat.title()

def js(s):
    return '`' + s.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${') + '`'

ap = argparse.ArgumentParser()
ap.add_argument('docx'); ap.add_argument('--siri', required=True)
ap.add_argument('--mula', type=int, required=True, help='id global pertama')
ap.add_argument('--no-mula', type=int, default=1)
ap.add_argument('--numbered', action='store_true', help='format Numbered List ("Cadangan / Set NN" + KATEGORI): topik ikut kategori')
ap.add_argument('--lifehack', action='store_true', help='format Lifehack: topik ikut kategori (Rumah & Dapur / Kereta & Perjalanan / Gajet & Barangan)')
a = ap.parse_args()

x = zipfile.ZipFile(a.docx).read('word/document.xml').decode('utf8')
ps = [para(p) for p in re.findall(r'<w:p[ >].*?</w:p>', x, flags=re.S)]
ps = [p for p in ps if p]

sets, cur, kat_semasa = [], None, ''
for p in ps:
    if p.startswith('KATEGORI:'):
        kat_semasa = p.split(':', 1)[1].strip()   # baris kategori datang SEBELUM set pertama dalam kategori tu
        continue
    m = re.match(r'(?:Cadangan\s*/\s*)?Set\s*#?(\d+)\s*(?:\(#\d+\))?\s*:\s*(.+)$', p)
    if m:
        cur = {'tajuk': m.group(2), 'bahagian': [], 'kat': kat_semasa}
        sets.append(cur); continue
    if cur is not None:
        cur['bahagian'].append(p)

for i, s in enumerate(sets):
    b = s['bahagian']
    # b: "1. Ayat..", "(Background..)", POST, "2. Ayat..", "(Komen..)", KOMEN..., FOOTER
    i1 = next(k for k, t in enumerate(b) if t.startswith('1.'))
    i2 = next(k for k, t in enumerate(b) if t.startswith('2.'))
    # buang baris label "(Background Warna • N aksara)" / "(Komen Pertama + Link Sahih)"
    label = lambda t: t.startswith('(') and t.endswith(')')
    pos = [t for t in b[i1 + 1:i2] if not label(t)]
    post = '\n'.join(pos)
    if re.match(PEMBUKA, post):
        post = re.sub(PEMBUKA, 'Ada yang tahu? ', post)
    elif not post.startswith('Ada yang tahu'):
        post = 'Ada yang tahu? ' + post   # format Lifehack: ayat terus, tambah pembuka
    isi = []
    for t in b[i2 + 1:]:
        if t.startswith('Moga bermanfaat'):
            break   # perenggan CTA docx (Moga bermanfaat / Khas untuk / Whatsapp / Taufik) diganti CTA_KOMEN
        if not label(t):
            isi.append(t)
    komen = '\n\n'.join(isi) + '\n\n' + CTA_KOMEN   # CTA tetap, ganti sign-off docx
    m = re.match(r'(.*?)\s*\[(.+)\]\s*$', s['tajuk'])
    tajuk, kat = (m.group(1), m.group(2)) if m else (s['tajuk'], s.get('kat', ''))
    alat = re.search(r'\(([^()]+)\)\s*$', tajuk)
    alat = alat.group(1) if alat else ''
    link = re.search(r'https?://\S+', komen)
    pisah = r'[ &/,]+' if a.numbered else r'[ &/]+'   # format Numbered: kategori ada koma
    tags = [t for t in {alat.lower(), *[w.lower() for w in re.split(pisah, kat) if len(w) > 3]} if t]
    print('  {')
    print(f'    id: {a.mula + i},')
    print(f'    siri: "{a.siri}",')
    print(f'    no: {a.no_mula + i},')
    print(f'    topik: "{topik_lifehack(kat) if a.lifehack else topik_numbered(kat) if a.numbered else topik_dari(kat)}",')
    print(f'    kategori: {js(kat)},')
    print(f'    tajuk: {js(tajuk)},')
    print(f'    tags: {sorted(tags)!r},'.replace("'", '"'))
    print(f'    link: "{link.group(0) if link else ""}",')
    print(f'    post: {js(post)},')
    print(f'    komen: {js(komen)},')
    print('  },')
