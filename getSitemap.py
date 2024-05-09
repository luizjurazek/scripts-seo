import csv
import xml.etree.ElementTree as ET
import requests

# Função para extrair URLs do XML
def extract_urls_from_xml(xml_content):
    # Carrega o XML
    root = ET.fromstring(xml_content)
    
    # Lista para armazenar os URLs
    urls = []
    
    # Itera sobre cada elemento <loc> no XML
    for loc in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        urls.append(loc.text)
    
    return urls

# URL do XML
xml_url = 'https://www.example.com.br/xml/categorias.xml'

# Faz a solicitação HTTP para obter o conteúdo do XML
response = requests.get(xml_url)
if response.status_code == 200:
    # Extrai os URLs do XML
    urls = extract_urls_from_xml(response.content)
    
    # Salva os URLs em um arquivo CSV
    with open('./URLs/output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['URLs'])  # Escreve o cabeçalho do CSV
        for url in urls:
            writer.writerow([url])
    print("Os URLs foram salvos em 'urls.csv'.")
else:
    print("Falha ao obter o XML. Status Code:", response.status_code)