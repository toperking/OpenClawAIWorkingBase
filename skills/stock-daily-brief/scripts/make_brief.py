#!/usr/bin/env python3
import argparse
import json
from datetime import datetime


def pct(change, close):
    try:
        prev = close - change
        return (change / prev) * 100 if prev else 0.0
    except Exception:
        return 0.0


def line(item, key, default="資料不足"):
    v = item.get(key)
    return default if v in (None, "") else v


def build(item):
    name = line(item, "name")
    code = line(item, "code")
    close = item.get("close")
    change = item.get("change")
    volume_note = line(item, "volume_note")

    if close is None or change is None:
        change_pct = "資料不足"
        close_txt = "資料不足"
        change_txt = "資料不足"
    else:
        change_pct = f"{pct(float(change), float(close)):.2f}"
        close_txt = f"{float(close):.2f}"
        change_txt = f"{float(change):+.2f}"

    facts = item.get("facts", [])[:3]
    reads = item.get("reads", [])[:3]
    while len(facts) < 2:
        facts.append("資料不足")
    while len(reads) < 2:
        reads.append("資料不足")

    support = line(item, "support")
    resistance = line(item, "resistance")
    next_event = line(item, "next_event")
    headline = line(item, "headline")

    parts = [
        f"## {name} {code} 盤後摘要",
        f"- 今日重點：{headline}",
        f"- 收盤：{close_txt}｜漲跌：{change_txt}（{change_pct}%）｜量能：{volume_note}",
        "- 關鍵驅動：",
        f"  - 事實：{facts[0]}",
        f"  - 解讀：{reads[0]}",
        f"  - 事實：{facts[1]}",
        f"  - 解讀：{reads[1]}",
    ]
    if len(facts) > 2 or len(reads) > 2:
        f3 = facts[2] if len(facts) > 2 else "資料不足"
        r3 = reads[2] if len(reads) > 2 else "資料不足"
        parts.extend([f"  - 事實：{f3}", f"  - 解讀：{r3}"])

    parts.extend([
        f"- 明日觀察：上檔 {resistance} / 下檔 {support}；事件：{next_event}",
        "- 風險提醒：本摘要僅供資訊整理，不構成投資建議。",
    ])
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser(description="Generate TW stock post-market brief from JSON.")
    ap.add_argument("input", help="Path to JSON file (object or list)")
    args = ap.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data if isinstance(data, list) else [data]
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"# 股票盤後摘要\n\n更新時間：{ts}\n")
    for i, item in enumerate(items):
        print(build(item))
        if i != len(items) - 1:
            print("\n---\n")


if __name__ == "__main__":
    main()
