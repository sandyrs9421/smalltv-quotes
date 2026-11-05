import json, urllib.request, os, time, sys
cfg = json.load(open("coins.json"))
coins = [c for c in cfg.get("coins", []) if c]
if not coins:
    print("no coins configured"); sys.exit(0)
ids = ",".join(coins)
url = ("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids="
       + urllib.parse.quote(ids) + "&sparkline=true&price_change_percentage=24h")
data = None
for attempt in range(5):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "smalltv-quotes"})
        data = json.load(urllib.request.urlopen(req, timeout=30)); break
    except Exception as e:
        print("attempt", attempt, "failed:", e); time.sleep(15)
if data is None:
    print("could not fetch from CoinGecko"); sys.exit(1)
os.makedirs("quotes", exist_ok=True)
for c in data:
    sp = (c.get("sparkline_in_7d") or {}).get("price") or []
    sp24 = [round(x, 6) for x in sp[-24:]]          # last ~24h, hourly
    out = {
        "symbol": c["id"],
        "name": c.get("name", c["id"]),
        "price": round(c.get("current_price") or 0, 6),
        "currency": "$",
        "changePct": round(c.get("price_change_percentage_24h") or 0, 3),
        "range": "24H",
        "spark": sp24,
        "ok": True,
    }
    json.dump(out, open("quotes/%s.json" % c["id"], "w"))
    print("wrote", c["id"], out["price"], "USD")
