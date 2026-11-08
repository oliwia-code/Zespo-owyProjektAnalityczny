# Słownik Zmiennych
### Zbiór danych: Wyniki ING Biegnij Warszawo 2026 (surowe z API Datasport)

| Nazwa kolumny | Typ | Opis | Wartości / jednostka | Źródło |
| :--- | :--- | :--- | :--- | :--- |
| `kod` | `int64` | Unikalny identyfikator wpisu w bazie. | Liczba całkowita, np. 691749 | API Datasport |
| `dystans` | `int64` | Numer dystansu w imprezie (1 to bieg główny 10 km). | 1 | API Datasport |
| `numer` | `int64` | Numer startowy nadany zawodnikowi. | Liczba całkowita, > 0 | API Datasport |
| `nazwisko` | `object` | Nazwisko zawodnika. | Tekst, zazwyczaj wielkie litery | API Datasport |
| `imie` | `object` | Imię zawodnika. | Tekst, zazwyczaj wielkie litery | API Datasport |
| `miasto` | `object` | Deklarowane miasto zamieszkania. | Tekst | API Datasport |
| `druzyna` | `object` | Przynależność klubowa lub drużynowa. | Tekst (w tym spacja gdy brak) | API Datasport |
| `plec` | `object` | Płeć zawodnika (np. 'M' lub 'K'). | Kategoria ('M' / 'K') | API Datasport |
| `rokur` | `int64` | Rok urodzenia zawodnika. | np. 1999 (lub 0 dla braków) | API Datasport |
| `katw` | `object` | Kategoria wiekowa (np. M20, M30). | Kategoria, tekst | API Datasport |
| `msckatw` | `int64` | Miejsce w swojej kategorii wiekowej. | Liczba całkowita, > 0 | API Datasport |
| `katgrupa` | `object` | Dodatkowa kategoria/grupa wewnątrz biegu. | Tekst lub spacja | API Datasport |
| `msckatg` | `int64` | Miejsce w dodatkowej grupie. | Liczba całkowita | API Datasport |
| `mscplec` | `int64` | Miejsce w kategorii płci (open kobiet / open mężczyzn). | Liczba całkowita | API Datasport |
| `czas1` | `object` | Surowy międzyczas na punkcie pomiarowym (5 km). | Tekst, format `HH:MM:SS,MM` | API Datasport |
| `msc1` | `int64` | Miejsce z zajmowane na punkcie kontrolnym (5 km). | Liczba całkowita | API Datasport |
| `czas` | `object` | Czas brutto na mecie (od wystrzału startera). | Tekst, format `HH:MM:SS,MM` | API Datasport |
| `msc` | `int64` | Miejsce w klasyfikacji generalnej biegu (Open). | Liczba całkowita, > 0 | API Datasport |
| `czasnetto` | `object` | Czas netto (od przebiegnięcia przez linię startu). | Tekst, format `HH:MM:SS,MM` | API Datasport |
| `mscnetto` | `int64` | Zmienna techniczna z API (często wyzerowana). | Zazwyczaj 0 | API Datasport |
| `czaswsp` | `object` | Czas wykorzystywany przy przelicznikach / wyrównaniach (np. WMA). | Tekst, format `HH:MM:SS,MM` | API Datasport |
| `meta` | `object` | Dokładna godzina (czas zegarowy) przebiegnięcia mety. | Tekst, format `HH:MM:SS,MM` | API Datasport |
| `kraj` | `object` | Kod kraju zawodnika. | Tekst (np. 'POL', 'UKR') | API Datasport |
| `start` | `object` | Zegarowy czas minięcia linii startu przez zawodnika. | Tekst (np. '12:00:19') | API Datasport |
| `anonim` | `object` | Flaga anonimizacji danych zawodnika (często pusta). | Puste lub wartość logiczna | API Datasport |
| `id_per` | `int64` | Zewnętrzny ID biegacza w systemie Datasport. | Liczba całkowita (lub 0) | API Datasport |
| `odleglosc` | `float64` | Długość całego dystansu w metrach. | 10000.00 | API Datasport |
| `speed` | `float64` | Średnie tempo w przeliczeniu prawdopodobnie na min/km. | Liczba zmiennoprzecinkowa, np. 3.08 | API Datasport |

**Pominięte zmienne:**
Podczas zrzutu danych z API zidentyfikowano kilkadziesiąt dodatkowych kolumn technicznych i flag (m.in. serie `mscdod1-8`, `nazdod1-8`, `uwagi`, `zlystart`, `dns`, `dnf`, `dsq`). Zostały one celowo pominięte w niniejszym słowniku. Wstępna inspekcja surowego pliku wykazała, że są to w przytłaczającej większości puste zmienne (wartości null, puste ciągi znaków lub zera), których system Datasport nie wykorzystał przy tym konkretnym biegu. Całkowite usunięcie tych kolumn z ramki danych (drop) będzie jednym z pierwszych kroków czyszczenia w naszym notatniku EDA, co pozwoli zoptymalizować zbiór wyłącznie pod kątem naszego pytania badawczego.
