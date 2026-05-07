import os
import requests
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()


def fahrenheit_to_celsius(temp):
    if temp is not None:
        celsius = (temp - 32) / 1.8
        return round(celsius, 2)
    return None


def mph_to_kmph(v_mph):
    if v_mph is not None:
        v_kmph = v_mph * 1.609
        return round(v_kmph, 2)
    return None


def transformar_dados_clima(dados_clima):
    clima_atual = dados_clima.get('currentConditions', {})
    dias = dados_clima.get('days', [])

    hoje = dias[0] if dias else {}

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

    for dia in dias[:7]:
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

    if not base_url or not api_key:
        return {
            "error": True,
            "message": "Erro: Variáveis de ambiente BASE_URL ou API_KEY não configuradas."
        }

    if not base_url.endswith('/'):
        base_url += '/'

    url = f"{base_url}{cidade}?key={api_key}&unitGroup=us&include=days,current"

    try:
        print(f"--- Solicitando clima para: {cidade} ---")
        print(f"URL: {url}")

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        dados_brutos = response.json()
        return {
            "error": False,
            "data": transformar_dados_clima(dados_brutos)
        }

    except requests.exceptions.HTTPError as http_err:
        return {"error": True, "message": f"Erro na API (Status {response.status_code}): {http_err}"}
    except requests.exceptions.ConnectionError:
        return {"error": True, "message": "Erro de conexão: Verifique a URL ou sua internet."}
    except Exception as e:
        return {"error": True, "message": f"Erro inesperado: {str(e)}"}