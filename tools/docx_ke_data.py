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

def js(s):
    return '`' + s.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${') + '`'

ap = argparse.ArgumentParser()
ap.add_argument('docx'); ap.add_argument('--siri', required=True)
ap.add_argument('--mula', type=int, required=True, help='id global pertama')
ap.add_argument('--no-mula', type=int, default=1)
a = ap.parse_args()

x = zipfile.ZipFile(a.docx).read('word/document.xml').decode('utf8')
ps = [para(p) for p in re.findall(r'<w:p[ >].*?</w:p>', x, flags=re.S)]
ps = [p for p in ps if p]

sets, cur = [], None
for p in ps:
    m = re.match(r'Set\s*#?(\d+)\s*(?:\(#\d+\))?\s*:\s*(.+)$', p)
    if m:
        cur = {'tajuk': m.group(2), 'bahagian': []}
        sets.append(cur); continue
    if cur is not None:
        cur['bahagian'].append(p)

for i, s in enumerate(sets):
    b = s['bahagian']
    # b: "1. Ayat..", "(Background..)", POST, "2. Ayat..", "(Komen..)", KOMEN..., FOOTER
    i1 = next(k for k, t in enumerate(b) if t.startswith('1.'))
    i2 = next(k for k, t in enumerate(b) if t.startswith('2.'))
    post = '\n'.join(b[i1 + 2:i2])
    komen = '\n\n'.join(b[i2 + 2:])
    m = re.match(r'(.*?)\s*\[(.+)\]\s*$', s['tajuk'])
    tajuk, kat = (m.group(1), m.group(2)) if m else (s['tajuk'], '')
    alat = re.search(r'\(([^()]+)\)\s*$', tajuk)
    alat = alat.group(1) if alat else ''
    link = re.search(r'https?://\S+', komen)
    tags = [t for t in {alat.lower(), *[w.lower() for w in re.split(r'[ &/]+', kat) if len(w) > 3]} if t]
    print('  {')
    print(f'    id: {a.mula + i},')
    print(f'    siri: "{a.siri}",')
    print(f'    no: {a.no_mula + i},')
    print(f'    topik: "{topik_dari(kat)}",')
    print(f'    kategori: {js(kat)},')
    print(f'    tajuk: {js(tajuk)},')
    print(f'    tags: {sorted(tags)!r},'.replace("'", '"'))
    print(f'    link: "{link.group(0) if link else ""}",')
    print(f'    post: {js(post)},')
    print(f'    komen: {js(komen)},')
    print('  },')
