---
name: stock-direction-forecast
description: Produce short-term stock up/down direction forecasts primarily based on current news flow and international macro/geopolitical conditions, then refine with price/volume/flow confirmation. Output transparent probabilities, confidence labels, and scenario triggers. Use when the user asks for 預判漲跌、短線方向、明日偏多偏空判斷、或想依新聞與國際局勢快速量化看法.
---

# Stock Direction Forecast

## Overview
Generate short-horizon direction views (偏多/偏空/震盪) with **news-first** logic: prioritize current news and international conditions, then validate with market data.

## Workflow
1. Define horizon: next session / 1-3 days / 1 week.
2. Collect news & global context first:
   - US market close tone (risk-on/risk-off)
   - Fed rate path expectations / USD / US yields
   - Geopolitics (war, sanctions, cross-strait, energy shocks)
   - Sector-specific global headlines (AI, semis, EV, commodities)
3. Convert narrative into score via `references/scorecard.md` or `scripts/forecast_score.py`.
4. Use technical/flow data as confirmation layer (not primary driver).
5. Output direction + probability + confidence + invalidation triggers.

## Required Inputs (News-First)
- `news_sentiment` (-4~+4): aggregate tone of current key news.
- `global_macro` (-3~+3): rates/USD/yields/global growth backdrop.
- `geopolitics` (-3~+3): geopolitical tension or easing impact.
- `trend_confirm` (-2~+2): price trend confirmation.
- `flow_confirm` (-2~+2): institutional/foreign flow confirmation.
- `event_risk` (-2~0): upcoming event downside risk (earnings, CPI/FOMC, policy).

If news/global fields are missing, force confidence to 低.

## Output Rules
- Use Traditional Chinese (Taiwan).
- Must include:
  - 結論（偏多/偏空/震盪）
  - 概率（上漲% / 下跌%）
  - 信心等級（低/中/高）
  - 新聞與國際局勢關鍵依據（2-4點）
  - 失效條件（價位或事件觸發）
- Never claim guaranteed returns.
- Add disclaimer: 僅供研究，不構成投資建議。

## Resources
- Method: `references/scorecard.md`
- Script: `scripts/forecast_score.py`
- Sample input: `scripts/sample_input.json`

Use script output as baseline, then refine with freshest news context.