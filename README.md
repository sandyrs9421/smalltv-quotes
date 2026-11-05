# smalltv-quotes

Live price feed for the SmallTV ticker, for coins that Yahoo Finance doesn't list.

A GitHub Action runs hourly, fetches each coin from CoinGecko, and writes
`quotes/<id>.json` in the format the SmallTV firmware's **GitHub source** reads.
The device never talks to CoinGecko directly (that's what kept crashing it) — it
only reads these small static files.

## Add a coin
1. Open `coins.json` and add the coin's **CoinGecko ID** (the last part of its
   coingecko.com URL, e.g. `pearl-2`) to the `coins` list. Commit.
2. On the device: Ticker tab → **+ Add ticker**, set **Source = GitHub**,
   **Symbol = <that ID>**, **Category = Crypto**, Save.

The Action regenerates the files on every change and every hour.
