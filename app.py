from flask import Flask, jsonify, request
from flask_cors import CORS
import scraper

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "message": "API de dados da vitivinicultura - Embrapa",
        "endpoints": {
            "producao": "/api/producao",
            "processamento": "/api/processamento",
            "comercializacao": "/api/comercializacao",
            "importacao": "/api/importacao?subopcao=subopt_01&ano=2024",
            "exportacao": "/api/exportacao?subopcao=subopt_01&ano=2024"
        }
    })

@app.route('/api/producao')
def get_producao():
    data = scraper.get_data('opt_02', ano=2024)
    return jsonify(data)

@app.route('/api/processamento')
def get_processamento():
    data = scraper.get_data('opt_03', ano=2024)
    return jsonify(data)

@app.route('/api/comercializacao')
def get_comercializacao():
    data = scraper.get_data('opt_04', ano=2024)
    return jsonify(data)

@app.route('/api/importacao')
def get_importacao():
    subopcao = request.args.get('subopcao', 'subopt_01')
    ano = int(request.args.get('ano', 2024))
    data = scraper.get_data('opt_05', subopcao=subopcao, ano=ano)
    return jsonify(data)

@app.route('/api/exportacao')
def get_exportacao():
    subopcao = request.args.get('subopcao', 'subopt_01')
    ano = int(request.args.get('ano', 2024))
    data = scraper.get_data('opt_06', subopcao=subopcao, ano=ano)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
