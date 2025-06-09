import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import scraper

app = Flask(__name__)
CORS(app)

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
        },
        "observacao": "Os endpoints de importacao e exportacao possuem subgrupos que podem ser acessados via parâmetros"
    })

# Rotas da API com suporte a subgrupos
@app.route('/api/producao')
def get_producao():
    data = scraper.get_data('opt_02')
    return jsonify({
        "dados": data,
        "estrutura": "Cada item pode conter um array 'subitens' com os produtos detalhados"
    })

@app.route('/api/processamento')
def get_processamento():
    data = scraper.get_data('opt_03')
    return jsonify({
        "dados": data,
        "estrutura": "Cada item pode conter um array 'subitens' com os produtos detalhados"
    })

@app.route('/api/comercializacao')
def get_comercializacao():
    data = scraper.get_data('opt_04')
    return jsonify({
        "dados": data,
        "estrutura": "Cada item pode conter um array 'subitens' com os produtos detalhados"
    })

@app.route('/api/importacao')
def get_importacao():
    # Exemplo de como lidar com subopções
    subopcao = request.args.get('subopcao')
    data = scraper.get_data('opt_05', subopcao=subopcao)
    return jsonify({
        "dados": data,
        "subopcoes_disponiveis": scraper.SUBOPCOES_MAP['opt_05'],
        "observacao": "Passe o parâmetro 'subopcao' para filtrar (ex: subopt_01)"
    })

@app.route('/api/exportacao')
def get_exportacao():
    # Exemplo de como lidar com subopções
    subopcao = request.args.get('subopcao')
    data = scraper.get_data('opt_06', subopcao=subopcao)
    return jsonify({
        "dados": data,
        "subopcoes_disponiveis": scraper.SUBOPCOES_MAP['opt_06'],
        "observacao": "Passe o parâmetro 'subopcao' para filtrar (ex: subopt_01)"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  
    app.run(host='0.0.0.0', port=port)