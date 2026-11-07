# Plan pozyskiwania danych

## Tabela źródeł

| Źródło / URL / API | Format | Metoda pobrania | Kto odpowiada | Termin (próbka) |
| :--- | :--- | :--- | :--- | :--- |
| API Datasport (wyniki.datasport.pl) - ING Biegnij Warszawo 2026 | JSON | `requests` (HTTP GET) -> Przekształcenie w `pandas` | Anna Czernik | 07.11.2026 |

## Opis struktury danych, ograniczeń i decyzji projektowych
Dane są pobierane bezpośrednio z publicznego endpointu udostępniającego wyniki biegu masowego. 

Zamiast korzystać z dostępnego w interfejsie użytkownika eksportu wyników do formatu PDF (co wiąże się z wysokim ryzykiem błędów podczas parsowania i utratą struktury tabelarycznej), zespół wykorzystał Narzędzia Deweloperskie przeglądarki. Pozwoliło to na przechwycenie ukrytego zapytania XHR/Fetch i pobranie czystych, ustrukturyzowanych danych bezpośrednio z backendu w wygodnym formacie JSON. Strona nie blokuje tego typu zapytań.

Zbiór zawiera około 10 000 rekordów. Ze względu na dobrą praktykę i ograniczenia objętościowe w kontroli wersji, plik CSV ze zrzutem danych zostanie dodany do pliku `.gitignore`. W repozytorium utrzymywany będzie jedynie skrypt `fetch_data.py` pozwalający na powtarzalne wygenerowanie pliku docelowego.
