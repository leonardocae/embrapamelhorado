from bs4 import BeautifulSoup
from typing import List, Dict

# Mapeamento das subopções disponíveis por opção
SUBOPCOES_MAP = {
    'opt_01': [],
    'opt_02': [],
    'opt_03': [],
    'opt_04': [],
    'opt_05': ['subopt_01', 'subopt_02', 'subopt_03', 'subopt_04', 'subopt_05'],
    'opt_06': ['subopt_01', 'subopt_02', 'subopt_03', 'subopt_04']
}

def extrair_dados_html(html: str, opcao: str, ano: int, subopcao: str = None) -> List[Dict]:
    soup = BeautifulSoup(html, 'html.parser')
    tabela = soup.find('table', class_='tb_base tb_dados')

    if not tabela:
        return []

    resultado = []

    # Processa corpo da tabela
    corpo = tabela.find('tbody')
    if corpo:
        for linha in corpo.find_all('tr'):
            dados = [col.get_text(strip=True) for col in linha.find_all(['td', 'th'])]
            if dados:
                entrada = {
                    'ano': ano,
                    'tipo': 'item',
                    'dados': dados
                }
                if subopcao:
                    entrada['subopcao'] = subopcao
                resultado.append(entrada)

    # Processa rodapé da tabela (totais)
    rodape = tabela.find('tfoot')
    if rodape:
        for linha in rodape.find_all('tr'):
            dados = [col.get_text(strip=True) for col in linha.find_all(['td', 'th'])]
            if dados:
                entrada = {
                    'ano': ano,
                    'tipo': 'total',
                    'dados': dados
                }
                if subopcao:
                    entrada['subopcao'] = subopcao
                resultado.append(entrada)

    return resultado
