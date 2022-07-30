import requests


# TODO: cache this
def fetch_current_prices() -> dict[str, float]:
    try:
        res = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false"
        )
        data = res.json()
        current_prices = dict((e["symbol"], e["current_price"]) for e in data)
        return current_prices
    except:
        return {}
