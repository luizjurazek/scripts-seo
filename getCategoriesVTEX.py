import re
import requests
import pandas as pd

def get_data_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error fetching data from API:", e)
        return None

def flatten_data(data, parent=None, parent_urls=None):
    flat_data = []
    for item in data:
        current_urls = parent_urls + [item["url"]] if parent_urls else [item["url"]]
        flat_item = {
            "Nivel 1": current_urls[0] if current_urls else "-",
            "Nivel 2": current_urls[1] if len(current_urls) > 1 else "-",
            "Nivel 3": current_urls[2] if len(current_urls) > 2 else "-",
            "Nivel 4": current_urls[3] if len(current_urls) > 3 else "-",
            "id": item["id"],
            "name": item["name"],
            "url": item["url"],
            "Title": item.get("Title", ""),
            "MetaTagDescription": item.get("MetaTagDescription", "")
        }
        flat_data.append(flat_item)
        if item["hasChildren"]:
            flat_data.extend(flatten_data(item["children"], parent=item["id"], parent_urls=current_urls))
    return flat_data

def main(api_url, output_file):
    # Obter dados da API
    data = get_data_from_api(api_url)
    if not data:
        return
    
    # Achatamento dos dados
    flat_data = flatten_data(data)
    
    # Criar DataFrame
    df = pd.DataFrame(flat_data)
    
    # Salvar em um arquivo CSV
    df.to_csv(output_file, index=False)
    print("Data saved to", output_file)

if __name__ == "__main__":
    api_url = "https://example.myvtex.com/api/catalog_system/pub/category/tree/30/" # Insira o link da api da vtex aqui 
    domain = re.search(r'https://([\w.-]+)/', api_url).group(1)
    output_file = './Mapeamentos de categorias/' + domain + '.csv'
    main(api_url, output_file)
