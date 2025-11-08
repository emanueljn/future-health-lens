import requests
import pandas as pd

BASE = "http://apps.who.int/gho/athena/api/GHO/"

def fetch_indicator(indicator_code, country_code=None):
    url = f"{BASE}{indicator_code}"
    params = {}
    if country_code:
        params['filter'] = f"COUNTRY:{country_code}"
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # A resposta tem campo 'value' ou 'fact' dependendo do endpoint.
    # Vamos transformar num DataFrame (year, value, country, sex, etc)
    records = []
    for item in data.get('fact', []):
        # campos podem variar; inspecione a estrutura real
        year = int(item.get('Year') or item.get('YEAR') or item.get('TimePeriod'))
        val = item.get('NumericValue') or item.get('Value')
        country = item.get('SpatialDimension') or item.get('Country') or item.get('SpatialDim')
        try:
            val = float(val)
        except:
            val = None
        records.append({'year': year, 'value': val, 'country': country})
    return pd.DataFrame(records)