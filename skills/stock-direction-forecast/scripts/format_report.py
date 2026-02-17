#!/usr/bin/env python3
import argparse
import json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    args = ap.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"# 每日即時預判\n更新時間：{data.get('generated_at','')}\n")
    for r in data.get("results", []):
        print(f"## {r['symbol']} {r.get('alias','')}")
        print(f"- 結論：{r['direction']}")
        print(f"- 機率：上漲 {r['up_probability']}% / 下跌 {r['down_probability']}%")
        print(f"- 信心：{r['confidence']}")
        print(f"- 分數：{r['score']}")
        print("- 重點新聞：")
        for t in r.get("sources", {}).get("symbol_news", [])[:2]:
            print(f"  - {t}")
        print("- 風險提醒：僅供研究，不構成投資建議。\n")


if __name__ == '__main__':
    main()
