#!/usr/bin/env python3
import argparse
import json


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def confidence(data):
    core = ["news_sentiment", "global_macro", "geopolitics"]
    missing_core = sum(1 for k in core if k not in data)
    if missing_core >= 1:
        return "低"

    optional = ["trend_confirm", "flow_confirm", "event_risk"]
    missing_optional = sum(1 for k in optional if k not in data)
    if missing_optional >= 2:
        return "中"
    return "高"


def direction_and_prob(score):
    # map score to probability with wider range due to event-driven regime
    up = 50 + score * 2
    up = int(clamp(round(up), 25, 75))
    down = 100 - up
    if score >= 4:
        direction = "偏多"
    elif score <= -4:
        direction = "偏空"
    else:
        direction = "震盪"
    return direction, up, down


def main():
    ap = argparse.ArgumentParser(description="News-first stock direction forecast")
    ap.add_argument("input", help="JSON input path")
    args = ap.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    news = clamp(float(data.get("news_sentiment", 0)), -4, 4)
    macro = clamp(float(data.get("global_macro", 0)), -3, 3)
    geo = clamp(float(data.get("geopolitics", 0)), -3, 3)
    trend = clamp(float(data.get("trend_confirm", 0)), -2, 2)
    flow = clamp(float(data.get("flow_confirm", 0)), -2, 2)
    risk = clamp(float(data.get("event_risk", 0)), -2, 0)

    score = news + macro + geo + trend + flow + risk
    direction, up, down = direction_and_prob(score)
    conf = confidence(data)

    print("# 預判結果（新聞/國際局勢優先）")
    print(f"- 總分：{score:.1f}")
    print(f"- 結論：{direction}")
    print(f"- 機率：上漲 {up}% / 下跌 {down}%")
    print(f"- 信心：{conf}")
    print(f"- 分項：news={news:+.1f}, macro={macro:+.1f}, geo={geo:+.1f}, trend={trend:+.1f}, flow={flow:+.1f}, risk={risk:+.1f}")
    print("- 風險提醒：僅供研究，不構成投資建議。")


if __name__ == "__main__":
    main()
