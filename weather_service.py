import os
import requests
from datetime import datetime, timedelta


def fahrenheit_to_celsius(temp):
    return round((temp - 32) / 1.8, 2) if temp is not None else None


def mph_to_kmph(v_mph):
    return round(v_mph * 1.609, 2) if v_mph is not None else None


def transformar_dados_clima(dados_clima):
    clima_atual = dados_clima.get('currentConditions', {})
    hoje = dados_clima.get('days', [])[0]

    dados_processados = {
        "data": hoje.get('datetime'),
        "cidade": dados_clima.get('resolvedAddress'),
        "temperatura": fahrenheit_to_celsius(clima_atual.get('temp')),
        "umidade": int(clima_atual.get('humidity') or 0),
        "vento": int(mph_to_kmph(clima_atual.get('windspeed')) or 0),
        "precipitacao": int(clima_atual.get('precip') or 0),
        "temp_min": int(fahrenheit_to_celsius(hoje.get('tempmin')) or 0),
        "temp_max": int(fahrenheit_to_celsius(hoje.get('tempmax')) or 0),
        "icon": clima_atual.get('icon'),
        "previsao": []
    }

    for dia in dados_clima.get('days', [])[:7]:
        dados_processados['previsao'].append({
            "data": datetime.strptime(dia['datetime'], "%Y-%m-%d").strftime('%d/%m/%Y'),
            "temperatura_max": fahrenheit_to_celsius(dia.get('tempmax')),
            "temperatura_min": fahrenheit_to_celsius(dia.get('tempmin')),
            "icon": dia.get('icon'),
        })

    return dados_processados


def buscar_clima_por_cidade(cidade):
    base_url = os.getenv('BASE_URL_VISUAL_CROSSING')
    api_key = os.getenv('VISUAL_CROSSING_API_KEY')

    url = f"{base_url}{cidade}?key={api_key}&unitGroup=us&include=days,current"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return {"error": False, "data": transformar_dados_clima(response.json())}
    except Exception as e:
        return {"error": True, "message": str(e)}