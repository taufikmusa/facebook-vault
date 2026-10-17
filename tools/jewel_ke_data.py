#!/usr/bin/env python3
"""docx "30 Set Cerita Copywriting Emas GAP ke Barang Kemas" -> blok JS untuk src/data.js (tab PG Jewel).

Post panjang (tiada komen). Nombor/produk dalam cerita ditukar kepada slot {produk}, {hb}, {pos},
{jumlah}, {gap}, {gram} dsb. supaya App boleh kira semula bila Taufik tukar harga GAP / produk / harga barang.
Round-trip dipastikan: render(slot, nilai asal) == teks asal docx. Sidecar JSON (--asal) untuk ujian di Node.

Guna:  python3 -I tools/jewel_ke_data.py fail.docx --siri "PG Jewel-01" --mula 241 [--asal asal.json] > blok.txt
"""
import re, sys, zipfile, argparse, html, json

def txt(p):
    p = re.sub(r'<w:br[^>]*/>', '\n', p)
    return html.unescape(''.join(a or b for a, b in re.findall(r'<w:t[^>]*>(.*?)</w:t>|(\n)', p, flags=re.S)))

def baca(docx):
    x = zipfile.ZipFile(docx).read('word/document.xml').decode('utf8')
    body = x[x.index('<w:body>') + 8:]
    items = []
    for m in re.finditer(r'<w:tbl>.*?</w:tbl>|<w:p[ >].*?</w:p>', body, flags=re.S):
        s = m.group(0)
        if s.startswith('<w:tbl>'):
            cells = re.findall(r'<w:tc>.*?</w:tc>', s, flags=re.S)
            paras = [txt(p).strip() for p in re.findall(r'<w:p[ >].*?</w:p>', cells[0], flags=re.S)] if cells else []
            items.append(('T', paras, len(re.findall(r'<w:tr[ >]', s)), len(cells)))
        else:
            t = txt(s).strip()
            if t:
                items.append(('P', t))
    return items

def fmt(n, dp):
    i, _, d = f'{n:.{dp}f}'.partition('.')
    i = re.sub(r'\B(?=(\d{3})+$)', ',', i)
    return i + ('.' + d if d else '')

def num(s):
    return float(s.replace(',', ''))

def js(s):
    return '`' + s.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${') + '`'

def render(tpl, v, gap, simpan):
    hb, pos = v['hargaBarang'], v['pos']
    jumlah = hb + pos
    val = {
        'produk': v['produk'], 'produkNama': re.sub(r'\s*\([^)]*\)\s*$', '', v['produk']),
        'hb': fmt(hb, 2), 'hb0': fmt(hb, 0), 'pos': fmt(pos, 2), 'pos0': fmt(pos, 0),
        'jumlah': fmt(jumlah, 2), 'jumlah0': fmt(jumlah, 0),
        'gap': fmt(gap, 2), 'gap0': fmt(gap, 0), 'gram': f'{jumlah / gap:.4f}',
        'simpan': fmt(simpan, 0),
        'upah': fmt(v.get('upah', 0), 2), 'upah0': fmt(v.get('upah', 0), 0),
    }
    return re.sub(r'\{(\w+)\}', lambda m: val.get(m.group(1), m.group(0)), tpl)

def slot(post, v, gap, simpan):
    """Ganti nombor/produk literal dalam post dengan slot. Pulang (templat, baki RM tak dipetakan)."""
    t = post
    def sub_num(t, n, key, extra_before=''):
        # RM1,663.00 -> RM{key}; RM1,663 -> RM{key0} (hanya bila nilai bulat)
        t = re.sub(r'(?<![\d,.])RM' + re.escape(fmt(n, 2)) + r'(?!\d)', 'RM{' + key + '}', t)
        if n == int(n):
            t = re.sub(r'(?<![\d,.])RM' + re.escape(fmt(n, 0)) + r'(?![\d,]|\.\d)', 'RM{' + key + '0}', t)
        return t
    jumlah = v['hargaBarang'] + v['pos']
    gram = f'{jumlah / gap:.4f}'
    # produk dulu (nama penuh, kemudian nama asas tanpa kurungan akhir)
    t = t.replace(v['produk'], '{produk}')
    base = re.sub(r'\s*\([^)]*\)\s*$', '', v['produk'])
    if base != v['produk']:
        t = t.replace(base, '{produkNama}')
    t = re.sub(r'(?<![\d.])' + re.escape(gram) + r'(?!\d)', '{gram}', t)
    if 'upah' in v:
        t = re.sub(r'(upah RM)' + re.escape(fmt(v['upah'], 0)) + r'(?![\d,])', r'\g<1>{upah0}', t)
    t = sub_num(t, jumlah, 'jumlah')
    t = sub_num(t, v['hargaBarang'], 'hb')
    t = sub_num(t, v['pos'], 'pos')
    t = sub_num(t, gap, 'gap')
    t = sub_num(t, simpan, 'simpan') if False else re.sub(r'(?<![\d,.])RM' + re.escape(fmt(simpan, 0)) + r'(?![\d,]|\.\d)', 'RM{simpan}', t)
    baki = sorted(set(re.findall(r'RM[\d,]+(?:\.\d+)?', re.sub(r'\{\w+\}', '', t))))
    return t, baki

ap = argparse.ArgumentParser()
ap.add_argument('docx'); ap.add_argument('--siri', required=True)
ap.add_argument('--mula', type=int, required=True); ap.add_argument('--asal')
a = ap.parse_args()

items = baca(a.docx)
idx = [i for i, it in enumerate(items) if it[0] == 'P' and re.match(r'Bahagian\s+\d+\s*:', it[1])]
out, asal, log = [], {}, []
gap_global = None
for n, i in enumerate(idx):
    m = re.match(r'Bahagian\s+\d+\s*:\s*Set\s*\d+\s*:\s*(.+)$', items[i][1])
    tajuk = m.group(1).strip()
    meta = items[i + 1][1]
    cell = items[i + 2]
    assert cell[0] == 'T', f'set {n + 1}: jadual cerita tiada'
    post = '\n'.join(cell[1]).strip()
    post = re.sub(r'\n{3,}', '\n\n', post)
    persona = re.search(r'Watak & Sudut Pandang:\s*(.+)', meta)
    persona = persona.group(1).strip() if persona else ''
    produk = re.search(r'perincian pengiraan untuk (.+?):\s*(?:\n|•|$)', post).group(1).strip()
    hb = num(re.search(r'Harga Barang Kemas:\s*RM([\d,]+\.\d\d)', post).group(1))
    pos = num(re.search(r'Pengeposan Berinsurans \(GIT\):\s*RM([\d,]+\.\d\d)', post).group(1))
    gap = num(re.search(r'Harga Semasa Buy GAP:\s*RM([\d,]+(?:\.\d\d)?)', post).group(1))
    jml = num(re.search(r'Jumlah Nilai Keseluruhan:\s*RM([\d,]+\.\d\d)', post).group(1))
    gram_doc = re.search(r'=\s*([\d.]+)\s*gram', post).group(1)
    assert abs(hb + pos - jml) < 0.005, f'set {n + 1}: hb+pos != jumlah'
    assert f'{jml / gap:.4f}' == gram_doc, f'set {n + 1}: gram {jml / gap:.4f} != {gram_doc}'
    gap_global = gap_global or gap
    assert gap == gap_global, f'set {n + 1}: harga GAP berbeza'
    simpan = 100.0
    v = {'produk': produk, 'hargaBarang': hb, 'pos': pos}
    mu = re.search(r'upah RM([\d,]+)', post)
    if mu:
        v['upah'] = num(mu.group(1))
    tpl, baki = slot(post, v, gap, simpan)
    assert render(tpl, v, gap, simpan) == post, f'set {n + 1}: round-trip gagal'
    log.append((n + 1, baki))
    kod = f'{produk} {tajuk}'
    topik = 'Emas 999' if '999' in kod and '916' not in kod else 'Emas 916' if '916' in kod and '999' not in kod else 'Emas 999 & 916' if '999' in kod and '916' in kod else 'Umum'
    vs = ', '.join(f'{k}: ' + (js(x) if isinstance(x, str) else (str(int(x)) if x == int(x) else str(x))) for k, x in v.items())
    out.append(f'''  {{
    id: {a.mula + n},
    siri: "{a.siri}",
    no: {n + 1},
    topik: "{topik}",
    kategori: ``,
    tajuk: {js(tajuk)},
    tags: [],
    link: "",
    persona: {js(persona)},
    vars: {{ {vs} }},
    post: {js(tpl)},
    komen: ``,
  }},''')
    asal[a.mula + n] = post
print('\n'.join(out))
if a.asal:
    json.dump({'gap': gap_global, 'simpan': 100, 'asal': asal}, open(a.asal, 'w'), ensure_ascii=False)
print(f'# {len(idx)} set; harga GAP {gap_global}', file=sys.stderr)
for n, baki in log:
    if baki:
        print(f'  set {n}: RM tak dipetakan -> {baki}', file=sys.stderr)
