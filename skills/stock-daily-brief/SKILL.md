---
name: stock-daily-brief
description: Create concise Taiwanese-Chinese post-market stock summaries with clear structure, key drivers, risk notes, and next-session watch items. Use when the user asks for 盤後摘要、收盤重點、個股/大盤回顧、或要把市場數據整理成可讀的 daily brief.
---

# Stock Daily Brief

## Overview
Generate a clean, decision-oriented盤後摘要 in Traditional Chinese. Prioritize clarity, numbers, and actionable watchpoints over long commentary.

## Workflow
1. Confirm scope: market-wide, sector, or single ticker.
2. Collect required inputs (price/volume/change and notable events).
3. Build the brief using `references/brief-template.md`.
4. Add a short "明日觀察" section with specific trigger prices/events.
5. End with risk reminder; never present this as guaranteed investment advice.

## Required Input Fields
For each symbol/index, collect at least:
- 名稱 / 代號
- 開高低收 (or at minimum 收盤價)
- 漲跌金額與漲跌幅
- 成交量（或量能相對昨日）
- 2-3 個影響因子（財報、法說、政策、資金面、技術面）

If any field is missing, state "資料不足" explicitly instead of guessing.

## Output Rules
- Language: Traditional Chinese (Taiwan).
- Length target: 120-280 Chinese characters per symbol for quick reading.
- Use bullets and short sections; avoid walls of text.
- Separate facts from interpretation:
  - `事實` = observable data/news
  - `解讀` = likely meaning / scenario
- Include one-line risk note in every brief.

## Quick Format
Use this order unless the user asks for another layout:
1. 今日重點（一句話）
2. 盤勢摘要（數據）
3. 關鍵驅動（2-3點）
4. 明日觀察（價位/事件）
5. 風險提醒

## Resources
- Template: `references/brief-template.md`
- Optional helper script: `scripts/make_brief.py`

Run the helper script when the user provides structured JSON data and wants fast, consistent output.