import requests
from bs4 import BeautifulSoup
import pandas as pd

try:
    # faz com que uma exceção seja levantada
    response = requests.get('https://cnpj.linkana.com/cnpj/LUCIANA-LOPES-MENDES-31817503871/32610935000186') 
    response.raise_for_status() # se a requisição falhar faz com que uma exceção seja levantada

    content = response.content
    site = BeautifulSoup(content, 'html.parser') # Analisar o HTML

    results = site.findAll('li', attrs={'class': \
        'flex flex-row gap-4 p-5 odd:bg-gray-200 sm:odd:bg-transparent sm:[&:nth-child(4n+1)]:bg-gray-200 sm:[&:nth-child(4n+2)]:bg-gray-200'})

    data = [] # Lista vazia para armazenar os dados coletados no for.
    for result in results:
        # Procura um elemento <h3> / dentro da classe especificada
        titulo = result.find('h3', attrs={'class': 'text-gray-700 font-bold text-sm w-32'}) 
        titulo_text = titulo.text.strip() if titulo else "Título não encontrado"

        subtitulo = result.find('p', attrs={'class': 'text-gray-700 font-medium text-sm'}) or \
                    result.find('p', attrs={'class': 'text-gray-700 text-sm'}) or \
                    result.find('p', attrs={'class': 'text-gray-700 sm:font-medium text-sm'}) or \
                    result.find('p', attrs={'class': 'text-gray-700 text-sm font-medium sm:font-normal'}) or \
                    result.find('p', attrs={'class': 'text-gray-700 text-sm font-medium sm:font-normal'})

        subtitulo_text = subtitulo.text.strip() if subtitulo else "Parágrafo não encontrado"

        data.append({'Título': titulo_text, 'Subtítulo': subtitulo_text})

    df = pd.DataFrame(data)
    df.to_excel('linkana_result.xlsx', index=False)

    print("Dados salvos no arquivo 'linkana_result.xlsx' com sucesso.")

except requests.exceptions.RequestException as e:
    print(f"Erro ao fazer a requisição: {e}")

except Exception as e:
    print(f"Erro durante a análise do HTML: {e}")