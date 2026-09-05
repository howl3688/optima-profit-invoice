# 奧提瑪工具箱 · 分潤對帳單產生器

> 軟體部工具箱的一員。純前端靜態站（無後端、無 DB）。
> 📌 主基地通則會自動往上遞迴載入，⛔ 本檔不重抄。

## 一、正式站與部署（2026-08-30 實查）

- 🔴 **唯一正式站＝ https://optima-toolbox.pages.dev/**（Cloudflare Pages 專案 `optima-toolbox`，**公司帳號** `39aa57ea828579cf95507a84de97725f`；2026-09-05 由 `optima-profit-invoice` 改名——Cloudflare 不能改專案名，是另建專案後把部署切過去）
- ⚠️ **前一個站 `optima-profit-invoice.pages.dev` 暫留**（Howl 2026-09-05 裁示「舊名暫留」），首頁會依 hostname 顯示搬家提示；⛔ 不再部署到它、⛔ 不自行刪除（刪＝動正式環境＝Howl 閘門）。
- **部署＝在本資料夾跑 `./deploy.sh`**。⛔ 不要自己下 `wrangler pages deploy .`——本 repo 平常在 `master` 分支，wrangler 會拿當前分支當部署分支 ⇒ **只上到 preview、正式站不動**。`deploy.sh` 固定帶 `--branch main` 就是在防這個。
- 🔴 **部署前必查帳號**：`npx wrangler whoami` 要看到 `iplumate@gmail.com` / `39aa57ea…`。**wrangler 會自己跑回 Howl 個人帳號**（記憶 `cloudflare-api-token`：同一個工作階段內就會翻掉，每次 deploy 前都要重查）。
- `git remote` 是 `github.com/howl3688/optima-profit-invoice`（repo 名尚未跟著改，Howl 未決），**GitHub Pages 已 404、不是部署管道**（僅版控）。

### ⚠️ 舊站還活著（2026-08-30 發現，待 Howl 決定）
`https://profit-invoice.pages.dev/`（Howl **個人**帳號）**仍回 200，且是過期版**（與正式站差 67 行）。
拿到舊網址的人會看到舊版。**關站＝動正式環境＝Howl 閘門**，⛔ 不自行處理。

## 二、檔案

| 檔 | 是什麼 |
|---|---|
| `index.html` | 工具箱首頁 |
| `invoice.html` | 分潤對帳單產生器（主體） |
| `warehouse-sku.html` ／ `build-warehouse-sku.py` | 倉庫料號表與產生器 |
| `zhongqin-inventory.html` | 眾勤月度進銷存表產生器（純前端 ExcelJS；計帳規則在檔內 RULES 區，與主基地 skill `眾勤進銷存表/計帳規則.md` 同步；眾勤模板 base64 內嵌） |
| `*logo.png`／`*發票章.jpg` | 內嵌用圖（**base64 內嵌在 html**，不依賴外部檔名） |
| `分潤對帳單產生器_使用教學.docx` | 給人看的操作教學 |

## 三、🔴 已知雷（踩過，別重犯）

**分頁 re-entrancy**：超過 15 項後**回頭再渲染一次**（改任一格／加項／多打字），訂購人數與所有合計會整塊消失，第三次 `renderPreview` 直接崩、預覽凍結、PDF 壞。
⇒ **改分頁/渲染邏輯後，驗收一定要「越過 15 項 → 反覆編輯 → 連跑多輪」**，⛔ 不可只驗一次 happy path。詳見記憶 `feedback-claimed-done-not-functionally-verified`。

## 四、完成的標準

**部署＝繞過快取實查線上內容、多次抽查全中才算**（邊緣傳播要 1~3 分鐘）。⛔ `wrangler` 印成功不算完成。
