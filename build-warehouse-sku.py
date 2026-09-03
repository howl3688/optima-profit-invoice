#!/usr/bin/env python3
# 從雲端主檔重生 warehouse-sku.html 的資料快照，然後 ./deploy.sh 上線
#
# 資料來源(正本)＝ Google Sheet「梅侍料號_主檔」
#   https://docs.google.com/spreadsheets/d/1d0rvmzNM0OkeCJKo9Eu5wNJ-flOsYhWvfjcf04-KLJQ
#   讀寫用服務帳號 plumate-sheets-reader@plumate-ops（金鑰在 plumate-order-form/config/sheets-reader.json）
# 用法：python3 build-warehouse-sku.py            # 預設抓雲端
#      python3 build-warehouse-sku.py --xlsx 路徑  # 改用本機 Excel(離線備援)
import json, re, sys, os, datetime

SHEET_ID = '1d0rvmzNM0OkeCJKo9Eu5wNJ-flOsYhWvfjcf04-KLJQ'
KEY = '/Users/howl/Downloads/howlai/optima/plumate-order-form/config/sheets-reader.json'
HTML = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'warehouse-sku.html')

def from_sheet():
    import gspread
    from google.oauth2.service_account import Credentials
    creds = Credentials.from_service_account_file(KEY, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
    ws = gspread.authorize(creds).open_by_key(SHEET_ID).sheet1
    vals = ws.get_all_values()
    hdr = vals[0]
    return hdr, [dict(zip(hdr, r)) for r in vals[1:] if any(r)]

def from_xlsx(path):
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True)['梅侍主檔']
    it = list(ws.iter_rows(values_only=True)); hdr = list(it[0])
    return hdr, [dict(zip(hdr, r)) for r in it[1:] if r[hdr.index('料號(SKU)')]]

if '--xlsx' in sys.argv:
    src = sys.argv[sys.argv.index('--xlsx') + 1]; hdr, recs = from_xlsx(src); print('來源: 本機', src)
else:
    hdr, recs = from_sheet(); print('來源: 雲端 Google Sheet「梅侍料號_主檔」')

def val(d, k): return str(d.get(k, '') or '')
rows = [{'sku': val(d,'料號(SKU)'), 'name': val(d,'品名'), 'cls': val(d,'類別(屬性)'),
         'vol': val(d,'規格'), 'unit': val(d,'單位'), 'barcode': val(d,'國際條碼'),
         'status': val(d,'狀態'), 'old': val(d,'舊料號(參考)')} for d in recs if val(d,'料號(SKU)')]
flav = {}
PACK = re.compile(r'^(單瓶|\d+入箱)$')   # 醋覓品名尾段是包裝，口味在倒數第二段
for x in rows:
    p = x['sku'].split('-')
    if p[0] in ('A','S') and len(p) >= 4:
        code = re.sub(r'\d+$', '', p[3])   # PPF12 → PPF（12入箱與單瓶同口味碼）
        segs = x['name'].split('_')
        if PACK.match(segs[-1]): segs.pop()
        flav.setdefault(code, segs[-1])

snap = sys.argv[sys.argv.index('--date')+1] if '--date' in sys.argv else datetime.date.today().isoformat()
html = open(HTML, encoding='utf-8').read()
html = re.sub(r"const DATA=.*?;\n", 'const DATA=' + json.dumps(rows, ensure_ascii=False) + ';\n', html, count=1)
html = re.sub(r"const FLAV=.*?;\n", 'const FLAV=' + json.dumps(flav, ensure_ascii=False) + ';\n', html, count=1)
html = re.sub(r"const SNAPSHOT='[^']*';", f"const SNAPSHOT='{snap}';", html, count=1)
open(HTML, 'w', encoding='utf-8').write(html)
print(f'注入完成：{len(rows)} 筆、{len(flav)} 口味碼、快照 {snap} → warehouse-sku.html')
print('接著 ./deploy.sh 上線')
