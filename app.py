from flask import Flask, request, render_template
from datetime import datetime
from dotenv import load_dotenv
from weather_service import buscar_clima_por_cidade
from database import salvar_historico_clima, buscar_historico_clima

load_dotenv()
app = Flask(__name__)


@app.route('/', methods=["GET"])
def home():
    cidade = request.args.get('cidade', '').strip()
    weather = None
    error = None

    data_hoje = datetime.now().strftime('%Y-%m-%d')

    if cidade:
        registro_banco = buscar_historico_clima(cidade, data_hoje)

        if registro_banco:
            print(f"--- Dados vindos do BANCO LOCAL: {cidade} ---")
            weather = registro_banco
        else:
            print(f"--- Dados vindos da API EXTERNA: {cidade} ---")
            result = buscar_clima_por_cidade(cidade)

            if result["error"]:
                error = result["message"]
            else:
                weather = result["data"]
                salvar_historico_clima(weather)

    return render_template("index.html", cidade=cidade, weather=weather, error=error)


if __name__ == '__main__':
    app.run(debug=True)