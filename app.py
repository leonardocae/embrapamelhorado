import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import scraper
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Obter o ano atual
ANO_ATUAL = datetime.now().year

# Rota principal
@app.route('/')
def home():
    return jsonify({
        "message": "API de dados da vitivinicultura - Embrapa",
        "endpoints": {
            "producao": "/api/producao",
            "processamento": "/api/processamento",
            "comercializacao": "/api/comercializacao",
            "importacao": "/api/importacao",
            "exportacao": "/api/exportacao"
        }
    })

# Rotas da API com tratamento de erro
@app.route('/api/producao')
def get_producao():
    try:
        # Você precisará obter o HTML da página primeiro
        # Aqui estou assumindo que você tem uma função para isso
        html = obter_html_da_pagina('producao')  # Você precisará implementar esta função
        data = scraper.get_data(opcao='opt_02', html=html, ano=ANO_ATUAL)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/processamento')
def get_processamento():
    try:
        html = obter_html_da_pagina('processamento')
        data = scraper.get_data(opcao='opt_03', html=html, ano=ANO_ATUAL)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/comercializacao')
def get_comercializacao():
    try:
        html = obter_html_da_pagina('comercializacao')
        data = scraper.get_data(opcao='opt_04', html=html, ano=ANO_ATUAL)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/importacao')
def get_importacao():
    try:
        subopcao = request.args.get('subopcao')
        html = obter_html_da_pagina('importacao')
        data = scraper.get_data(opcao='opt_05', html=html, ano=ANO_ATUAL, subopcao=subopcao)
        return jsonify({
            "dados": data,
            "subopcoes_disponiveis": scraper.SUBOPCOES_MAP['opt_05']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/exportacao')
def get_exportacao():
    try:
        subopcao = request.args.get('subopcao')
        html = obter_html_da_pagina('exportacao')
        data = scraper.get_data(opcao='opt_06', html=html, ano=ANO_ATUAL, subopcao=subopcao)
        return jsonify({
            "dados": data,
            "subopcoes_disponiveis": scraper.SUBOPCOES_MAP['opt_06']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def obter_html_da_pagina(tipo: str):
    """Função para obter o HTML da página correspondente"""
    # Você precisará implementar esta função
    # Pode usar requests ou outro método para buscar o HTML
    # Exemplo simplificado:
    import requests
    url = f"https://www.embrapa.br/uva-e-vinho/{tipo}/{ANO_ATUAL}"
    response = requests.get(url)
    return response.text

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  
    app.run(host='0.0.0.0', port=port)