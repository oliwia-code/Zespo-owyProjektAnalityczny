import requests
import pandas as pd
import os

def fetch_and_clean_run_data():
    # Json z narzedzi developerskich z datasportu
    url = 'https://wyniki.datasport.pl/results5969/results.json'

    print("Rozpoczynam pobieranie danych z API...")
    response = requests.get(url)

    if response.status_code == 200:
        data_json = response.json()
        print(f"Pobrano pomyślnie. Liczba wczytanych rekordów: {len(data_json)}")

        # Transformacja do df
        df = pd.DataFrame(data_json)

        # Zapisujemy cały zbiór do folderu data
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        output_file = os.path.join(project_root, 'data', 'dane_surowe_biegnij_warszawo.csv')

        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Zapisano pełny zbiór do: {output_file}")

    else:
        print(f"Błąd pobierania: {response.status_code}")

if __name__ == "__main__":
    fetch_and_clean_run_data()