#!/usr/bin/env python3
import argparse
import json


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def confidence(data):
    required = ["trend", "volume", "flow", "catalyst", "risk"]
    missing = sum(1 for k in required if k not in data)
    if missing >= 2:
        return "低"
    if missing == 1:
        return "中"
    return "高"


def direction_and_prob(score):
    # map score -10..10 to up probability 30..70
    up = 50 + score * 2
    up = int(clamp(round(up), 30, 70))
    down = 100 - up
    if score >= 4:
        direction = "偏多"
    elif score <= -4:
        direction = "偏空"
    else:
        direction = "震盪"
    return direction, up, down


def main():
    ap = argparse.ArgumentParser(description="Score-based short-term stock direction forecast")
    ap.add_argument("input", help="JSON input path")
    args = ap.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    # expected each field roughly in documented ranges
    t = clamp(float(data.get("trend", 0)), -3, 3)
    v = clamp(float(data.get("volume", 0)), -2, 2)
    fl = clamp(float(data.get("flow", 0)), -2, 2)
    c = clamp(float(data.get("catalyst", 0)), -2, 2)
    r = clamp(float(data.get("risk", 0)), -1, 1)

    score = t + v + fl + c + r
    direction, up, down = direction_and_prob(score)
    conf = confidence(data)

    print("# 預判結果")
    print(f"- 總分：{score:.1f}（範圍 -10~+10）")
    print(f"- 結論：{direction}")
    print(f"- 機率：上漲 {up}% / 下跌 {down}%")
    print(f"- 信心：{conf}")
    print("- 風險提醒：僅供研究，不構成投資建議。")


if __name__ == "__main__":
    main()
