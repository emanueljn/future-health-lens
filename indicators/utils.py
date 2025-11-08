import requests
import numpy as np
from sklearn.linear_model import LinearRegression

# Dicionário de indicadores com os códigos corretos da WHO
INDICATORS = {
    "expectativa_vida": "WHOSIS_000001",
    "mortalidade_infantil": "MDG_0000000001",
    "vacina_sarampo": "WHS9_86",
    "alcoolismo": "SA_0000001462",
    "tabagismo": "SA_0000001400",
}


def fetch_indicator_data(indicator_code, country_code="BRA"):
    """
    Busca os dados de um indicador da WHO API para um país.
    """
    url = f"https://ghoapi.azureedge.net/api/{indicator_code}?$filter=SpatialDim eq '{country_code}'"
    response = requests.get(url)
    if response.status_code != 200:
        return []

    data = response.json().get("value", [])
    result = []
    for item in data:
        if item.get("TimeDim") and item.get("NumericValue"):
            result.append({
                "year": int(item["TimeDim"]),
                "value": float(item["NumericValue"])
            })
    return sorted(result, key=lambda x: x["year"])


def predict_future(data, years=5):
    """
    Gera previsões lineares para os próximos anos com base nos dados históricos.
    """
    if not data:
        return []

    X = np.array([d["year"] for d in data]).reshape(-1, 1)
    y = np.array([d["value"] for d in data])

    model = LinearRegression().fit(X, y)
    last_year = int(X[-1][0])

    predictions = []
    for i in range(1, years + 1):
        future_year = last_year + i
        predicted_value = model.predict([[future_year]])[0]
        predictions.append({
            "year": future_year,
            "value": round(float(predicted_value), 2)
        })
    return predictions


def build_dashboard_data(country_code="BRA"):
    """
    Retorna dados agregados para o dashboard, incluindo previsões.
    """
    dashboard_data = []
    for name, code in INDICATORS.items():
        data = fetch_indicator_data(code, country_code)
        predictions = predict_future(data)
        full_data = data + predictions
        dashboard_data.append({
            "name": name,
            "code": code,
            "data": full_data
        })
    return dashboard_data
