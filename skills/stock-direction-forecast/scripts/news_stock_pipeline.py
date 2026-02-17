#!/usr/bin/env python3
import argparse
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

POS = ["surge", "rise", "gain", "cut", "easing", "optimism", "buy", "up", "beat"]
NEG = ["fall", "drop", "risk", "tension", "war", "sanction", "sell", "down", "miss"]


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def fetch_titles(query, lang, gl, ceid, n=5):
    q = urllib.parse.quote_plus(query)
    url = f"https://news.google.com/rss/search?q={q}&hl={lang}&gl={gl}&ceid={ceid}"
    with urllib.request.urlopen(url, timeout=20) as r:
        xml_data = r.read()
    root = ET.fromstring(xml_data)
    items = root.findall("./channel/item")[:n]
    return [i.findtext("title", default="") for i in items]


def score_titles(titles):
    s = 0
    for t in titles:
        lt = t.lower()
        s += sum(1 for w in POS if w in lt)
        s -= sum(1 for w in NEG if w in lt)
    return s


def direction(score):
    up = int(clamp(round(50 + score * 2), 25, 75))
    down = 100 - up
    if score >= 4:
        d = "偏多"
    elif score <= -4:
        d = "偏空"
    else:
        d = "震盪"
    return d, up, down


def one_symbol(sym, alias):
    tw = fetch_titles(f"{sym} {alias} 台股", "zh-TW", "TW", "TW:zh-Hant")
    us = fetch_titles("Fed Treasury yield rate cut", "en-US", "US", "US:en")
    geo = fetch_titles("Taiwan geopolitical tension", "en-US", "US", "US:en")

    news = clamp(score_titles(tw) / 3, -4, 4)
    macro = clamp(score_titles(us) / 3, -3, 3)
    geop = clamp(-abs(score_titles(geo)) / 3, -3, 3)
    trend = 0
    flow = 0
    risk = -1

    score = news + macro + geop + trend + flow + risk
    d, up, down = direction(score)

    return {
        "symbol": sym,
        "alias": alias,
        "score": round(score, 2),
        "direction": d,
        "up_probability": up,
        "down_probability": down,
        "confidence": "中",
        "inputs": {
            "news_sentiment": news,
            "global_macro": macro,
            "geopolitics": geop,
            "trend_confirm": trend,
            "flow_confirm": flow,
            "event_risk": risk,
        },
        "sources": {"symbol_news": tw[:3], "us_macro": us[:3], "geopolitics": geo[:3]},
    }


def main():
    ap = argparse.ArgumentParser(description="News-first multi-symbol forecast pipeline")
    ap.add_argument("--watchlist", required=True, help="JSON path. format: [{symbol,alias}]")
    ap.add_argument("--out", default="skills/stock-direction-forecast/scripts/realtime_batch.json")
    args = ap.parse_args()

    with open(args.watchlist, "r", encoding="utf-8") as f:
        watch = json.load(f)

    out = {
        "generated_at": datetime.now().isoformat(timespec="minutes"),
        "results": [one_symbol(i["symbol"], i.get("alias", i["symbol"])) for i in watch],
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(args.out)


if __name__ == "__main__":
    main()
