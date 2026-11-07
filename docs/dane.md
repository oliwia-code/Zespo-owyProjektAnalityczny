# Plan pozyskiwania danych

## Tabela źródeł

| Źródło / URL / API | Format | Metoda pobrania | Kto odpowiada | Termin (próbka) |
| :--- | :--- | :--- | :--- | :--- |
| API Datasport (wyniki.datasport.pl) - ING Biegnij Warszawo 2026 | JSON | `requests` (HTTP GET) -> Przekształcenie w `pandas` | Anna Czernik | 07.11.2026 |

## Opis struktury danych i ograniczeń
Dane są pobierane bezpośrednio z nielimitowanego, publicznego endpointu JSON dostarczającego wyniki biegu masowego. Strona nie blokuje zapytań XHR. 

Zbiór zawiera około 10 000 rekordów. Ze względu na dobrą praktykę i ograniczenia objętościowe w kontroli wersji, plik `dane_surowe_biegnij_warszawo.csv` zostanie dodany do pliku `.gitignore`. W repozytorium (w folderze `/data/`) utrzymywany będzie jedynie skrypt `fetch_data.py` pozwalający na powtarzalne wygenerowanie pliku docelowego na dowolnym środowisku.
