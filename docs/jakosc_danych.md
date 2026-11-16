## Rejestr problemów z jakością danych

Podczas fazy inżynierii cech zidentyfikowano następujące problemy w surowych danych z API Datasport:

1. **Mieszane typy danych w kolumnach czasowych (DtypeWarning)**
   * **Opis:** Kolumny takie jak `czas1`, `czas`, `czasnetto`, `czaswsp` zawierają niejednolite typy (np. tekst z przecinkami zamiast kropek, zera dla braków, puste stringi). 
   * **Akcja podjęta:** Tymczasowo wymuszono wczytywanie całego zbioru jako tekst (`dtype=str`), aby uniknąć błędów parsowania i utraty danych.
   * **Do zrobienia:** Konieczna globalna konwersja tych kolumn na ustandaryzowany format czasowy (np. całkowita liczba sekund lub obiekty `timedelta`).

2. **Ciche braki danych (Silent NaNs) w kolumnie `miasto`**
   * **Opis:** Część rekordów nie posiadała zadeklarowanego miasta (puste wartości wciągane przez Pandas jako `NaN` o typie float). Powodowało to błędy środowiska przy operacjach tekstowych.
   * **Akcja podjęta:** Zabezpieczono potok danych poprzez rzutowanie pustych wartości na obojętne stringi (`fillna('')`) przed ekstrakcją flagi `czy_lokals`.

3. **Wartości zerowe w roku urodzenia (`rokur`)**
   * **Opis:** Obecność wartości `0` jako odpowiednika braku danych dla roku urodzenia.
   * **Akcja podjęta:** W skrypcie inżynierii cech zmapowano wartości 0 na `np.nan` (właściwy brak danych), aby zapobiec sztucznemu zaniżaniu lub zawyżaniu statystyk przy wyliczaniu wieku uczestników (np. 2026 - 0 = 2026 lat).
