import requests
from bs4 import BeautifulSoup
import pandas as pd

# Faz a solicitação HTTP GET para a URL especificada
response = requests.get('https://empresas.serasaexperian.com.br/consulta-gratis/LUCIANA-LOPES-MENDES-32610935000186')

# Obtém o conteúdo da resposta
content = response.content

# Parsea o conteúdo HTML usando BeautifulSoup
site = BeautifulSoup(content, 'html.parser')

# Encontra a div específica com a classe 'BusinessData_businessData__contentData__fpkbz'
content = site.find('div', attrs={'class': 'BusinessData_businessData__contentData__fpkbz'})

# Define uma função para obter o segundo texto de um elemento e remover espaços em branco
def get_second_text(element):
    if element:
        texts = element.stripped_strings
        text_list = list(texts)
        return text_list[1].strip() if len(text_list) > 1 else None
    return None

# Dados extraídos
data = {
    "CNPJ": get_second_text(content.find('li', attrs={'style': "grid-area:cnpj"})),
    "Data Fundacao": get_second_text(content.find('li', attrs={'style': "grid-area:dataFundacao"})),
    "Situacao Cadastral": get_second_text(content.find('li', attrs={'style': "grid-area:situacaoCadastral"})),
    "Razao Social": get_second_text(content.find('li', attrs={'style': "grid-area:razaoSocial"})),
    "Nome Fantasia": get_second_text(content.find('li', attrs={'style': "grid-area:nomeFantasia"})),
    "Codigo e Descricao da natureza juridica": get_second_text(content.find('li', attrs={'style': "grid-area:codigoJuridico"})),
    "Matriz ou Filial": get_second_text(content.find('li', attrs={'style': "grid-area:matrizFilial"})),
    "Descricao da atividade": get_second_text(content.find('li', attrs={'style': "grid-area:codigoPrincipal"})),
    "Codigo e Descricao da atividade secundaria": get_second_text(content.find('li', attrs={'style': "grid-area:codigoSecundario"})),
    "Logradouro": get_second_text(content.find('li', attrs={'style': "grid-area:logradouro"})),
    "Bairro": get_second_text(content.find('li', attrs={'style': "grid-area:bairro"})),
    "CEP": get_second_text(content.find('li', attrs={'style': "grid-area:cep"})),
    "Municipio + UF": f"{get_second_text(content.find('li', attrs={'style': 'grid-area:municipio'}))} - {get_second_text(content.find('li', attrs={'style': 'grid-area:uf'}))}",
    "Telefone": get_second_text(content.find('li', attrs={'style': "grid-area:telefone"}))
}

# Cria um DataFrame
df = pd.DataFrame(list(data.items()), columns=['Campo', 'Valor'])

# Salva o DataFrame em um arquivo Excel
file_path = 'serasa_result.xlsx'
df.to_excel(file_path, index=False)

print(f"Dados salvos no arquivo: {file_path}")
