---
name: stock-direction-forecast
description: Produce short-term stock up/down direction forecasts using a transparent scorecard (price trend, volume, flow, news/event risk) and output scenario-based probabilities with confidence labels. Use when the user asks for 預判漲跌、短線方向、明日偏多偏空判斷、或要快速量化看法而非黑箱答案.
---

# Stock Direction Forecast

## Overview
Generate a transparent short-horizon direction view (偏多/偏空/震盪) with assumptions, key drivers, and risk triggers. Keep it explainable and avoid absolute certainty.

## Workflow
1. Define horizon: intraday / next session / 1-5 trading days.
2. Gather required inputs: trend, volume, flow, catalyst/risk.
3. Score with `scripts/forecast_score.py` or manual scorecard in `references/scorecard.md`.
4. Convert score to direction + probability + confidence.
5. Output base case / bull case / bear case with invalidation levels.

## Required Inputs
- Price context: recent close, moving-average relation, key support/resistance.
- Volume context: today vs recent average.
- Flow context: foreign/institutional net buy-sell (if available).
- Catalyst context: earnings, guidance, macro/policy, sector news.

If data is incomplete, explicitly mark "低信心".

## Output Rules
- Use Traditional Chinese (Taiwan).
- Must include:
  - 結論（偏多/偏空/震盪）
  - 概率（例如：上漲 55% / 下跌 45%）
  - 信心等級（低/中/高）
  - 關鍵依據（2-4點）
  - 失效條件（跌破/站上何價位或事件）
- Never claim guaranteed returns.
- Add disclaimer: 僅供研究，不構成投資建議。

## Resources
- Method: `references/scorecard.md`
- Script: `scripts/forecast_score.py`
- Sample input: `scripts/sample_input.json`

Use script output as a baseline, then refine with recent context and user constraints.