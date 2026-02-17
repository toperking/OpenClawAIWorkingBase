#!/usr/bin/env python3
import argparse
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


POS = ["surge", "rise", "gain", "cut", "easing", "optimism", "buy", "up"]
NEG = ["fall", "drop", "risk", "tension", "war", "sanction", "sell", "down"]


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


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def main():
    ap = argparse.ArgumentParser(description="Fetch news + estimate 0050 direction inputs")
    ap.add_argument("--out", default="skills/stock-direction-forecast/scripts/realtime_0050_auto.json")
    args = ap.parse_args()

    tw = fetch_titles("0050 ETF 台灣50", "zh-TW", "TW", "TW:zh-Hant")
    us = fetch_titles("Fed Treasury yield rate cut", "en-US", "US", "US:en")
    geo = fetch_titles("Taiwan geopolitical tension", "en-US", "US", "US:en")

    news_raw = score_titles(tw)
    macro_raw = score_titles(us)
    geo_raw = -abs(score_titles(geo)) if geo else -1

    data = {
        "news_sentiment": clamp(news_raw / 3, -4, 4),
        "global_macro": clamp(macro_raw / 3, -3, 3),
        "geopolitics": clamp(geo_raw / 3, -3, 3),
        "trend_confirm": 0,
        "flow_confirm": 0,
        "event_risk": -1,
        "sources": {
            "tw_0050": tw,
            "us_macro": us,
            "geo": geo,
        },
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(args.out)


if __name__ == "__main__":
    main()
