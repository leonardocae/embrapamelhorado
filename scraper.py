from bs4 import BeautifulSoup
from typing import List, Dict, Union

# Mapeamento das subopções disponíveis por opção
SUBOPCOES_MAP = {
    'opt_05': ['subopt_01', 'subopt_02', 'subopt_03', 'subopt_04', 'subopt_05'],
    'opt_06': ['subopt_01', 'subopt_02', 'subopt_03', 'subopt_04']
}


def get_data(html: str, opcao: str, ano: int, subopcao: str = None) -> List[Dict[str, Union[str, List]]]:
    soup = BeautifulSoup(html, 'html.parser')
    tabela = soup.find('table', class_='tb_base tb_dados')

    if not tabela:
        return []

    resultado = []
    item_atual = None

    # Processa corpo da tabela
    corpo = tabela.find('tbody')
    if corpo:
        for linha in corpo.find_all('tr'):
            # Verifica se é item principal ou subitem
            cols = linha.find_all(['td', 'th'])
            if not cols:
                continue
                
            primeira_col = cols[0]
            is_subitem = 'tb_subitem' in primeira_col.get('class', [])
            
            dados = [col.get_text(strip=True) for col in cols]
            
            if not is_subitem:
                # Item principal
                if item_atual:
                    resultado.append(item_atual)
                item_atual = {
                    'produto': dados[0],
                    'quantidade': dados[1] if len(dados) > 1 else None,
                    'ano': ano,
                    'subitens': []
                }
                if subopcao:
                    item_atual['subopcao'] = subopcao
            else:
                # Subitem
                if item_atual:
                    item_atual['subitens'].append({
                        'produto': dados[0],
                        'quantidade': dados[1] if len(dados) > 1 else None
                    })

    # Adiciona o último item processado
    if item_atual:
        resultado.append(item_atual)

    # Processa rodapé da tabela (totais)
    rodape = tabela.find('tfoot')
    if rodape:
        totais = []
        for linha in rodape.find_all('tr'):
            dados = [col.get_text(strip=True) for col in linha.find_all(['td', 'th'])]
            if dados:
                totais.append({
                    'descricao': dados[0],
                    'valor': dados[1] if len(dados) > 1 else None
                })
        
        if totais:
            resultado.append({
                'tipo': 'total',
                'ano': ano,
                'totaizador': totais[0]['valor'],
                'detalhes': totais
            })

    return resultado