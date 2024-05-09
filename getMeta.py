import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

def extract_title_and_description(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else 'N/A'
        description = soup.find('meta', attrs={'name': 'description'})
        description = description['content'].strip() if description else 'N/A'
        return title, description
    except Exception as e:
        print(f"Erro ao extrair dados da URL {url}: {e}")
        return 'N/A', 'N/A'

def main():
    start_time = time.time()
    csv_file = './SERPs/output.csv'
    output_data = []
    df = pd.read_csv(csv_file)
    total_urls = len(df)
    for index, row in df.iterrows():
        url = row['URLs']
        title, description = extract_title_and_description(url)
        output_data.append({'URL': url, 'Title': title, 'Description': description})
        print(f"URL {index + 1} de {total_urls} processada.")
    output_df = pd.DataFrame(output_data)
    output_df.to_csv('output.csv', index=False)
    end_time = time.time()
    duration = end_time - start_time
    print(f"Extracao concluída. Os resultados foram salvos em 'output.csv'.")
    print(f"Tempo total gasto: {duration:.2f} segundos.")

if __name__ == "__main__":
    main()