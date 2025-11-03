import requests
import pandas as pd

def fetch_openaq(country="IN", pollutant="pm25", limit=10000):
    url = "https://api.openaq.org/v2/measurements"
    params = {
        "country": country,
        "parameter": pollutant,
        "limit": limit,
        "sort": "desc"
    }
    r = requests.get(url, params=params)
    data = r.json()["results"]
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = fetch_openaq("IN", "pm25")
    df.to_csv("data/raw/india_pm25.csv", index=False)
    print("Saved to data/raw/india_pm25.csv")
