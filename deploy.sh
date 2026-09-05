#!/usr/bin/env bash
# 奧提瑪工具箱 — 正式部署（Cloudflare Pages，唯一正式站）
#   正式網址：https://optima-toolbox.pages.dev/（2026-09-05 由 optima-profit-invoice 改名；Cloudflare 不能改專案名，故另建專案）
#   舊站 optima-profit-invoice.pages.dev 暫留，⛔ 不再部署到它（Howl 2026-09-05：舊名暫留）
#
# 用法：改完檔案後，在本資料夾執行 ./deploy.sh
#
# ⚠️ 為什麼一定要 --branch main：
#   這是 Cloudflare「direct upload」專案，正式(Production)分支固定叫 main，
#   而本 repo 平常在 master 分支。若用預設 `wrangler pages deploy .`，
#   wrangler 會自動抓當前 git 分支(master)當部署分支 → 只上到 preview、正式站不動。
#   所以這裡固定 --branch main，確保永遠打到正式站。
set -euo pipefail
cd "$(dirname "$0")"
npx wrangler pages deploy . \
  --project-name optima-toolbox \
  --branch main \
  --commit-dirty=true
