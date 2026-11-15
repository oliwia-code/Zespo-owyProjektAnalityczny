# Pytanie badawcze i hipotezy  **wersja robocza** - poprawić (kilometry, pomoc organizatorom - gdzie postawić stoiska z piciem itp)

## 1. Temat projektu
Predykcja czasu ukończenia biegu 10 km na podstawie wyniku z połowy dystansu i danych demograficznych.

Projekt koncentruje się na sprawdzeniu, czy podstawowe cechy uczestników --- płeć oraz przynależność do kategorii wiekowej --- są powiązane z czasem ukończenia biegu. Analiza będzie prowadzona na podstawie wyników udostępnionych przez API Datasport.

Jest to przydatne w celu oszacowania przez organizatora jak rozlokować zasoby i wolontariuszy na macie(kiedy ma być więcej osób na macie, a kiedy mniej). W przyszłości można rozważyć dodanie tej predykcji do Datasport. 

## 2. Główne pytanie badawcze
**Czy na podstawie czasu uzyskanego na 5 km oraz danych demograficznych uczestników (płeć i kategoria wiekowa) można skutecznie przewidzieć czas netto ukończenia biegu na dystansie 10 km?**
Pytanie będzie weryfikowane z wykorzystaniem następujących zmiennych ze zbioru danych:

- plec – płeć uczestnika (K/M),
- katw – kategoria wiekowa uczestnika,
- czas na 5 km – czas uzyskany na połowie dystansu,
- czas – czas netto ukończenia biegu na dystansie 10 km.

Głównym celem analizy będzie stworzenie modelu predykcyjnego, który na podstawie czasu uzyskanego na 5 km oraz płci i kategorii wiekowej oszacuje końcowy czas biegu na 10 km.

Jako zmienną, którą będziemy przewidywać, przyjmujemy czas netto ukończenia biegu. Jest to czas mierzony od momentu przekroczenia linii startu do przekroczenia linii mety przez danego uczestnika.

Analiza będzie dotyczyć osób, dla których dostępne są prawidłowe czasy na 5 km i 10 km. Przed rozpoczęciem modelowania dane zostaną oczyszczone, a wartości czasu przeliczone na sekundy, aby możliwe było ich porównywanie i wykorzystanie w modelach.

Praktycznym zastosowaniem projektu będzie możliwość oszacowania, kiedy uczestnicy dotrą do mety. Informacje te mogą pomóc organizatorom w lepszym rozplanowaniu pracy wolontariuszy i obsługi biegu, szczególnie w momentach, gdy na mecie pojawia się najwięcej zawodników.

## 3. Hipotezy badawcze
**H1. Czas uzyskany na 5 km jest istotnym czynnikiem pozwalającym przewidzieć końcowy czas biegu na 10 km.**

Zakładamy, że osoby osiągające krótsze czasy na połowie dystansu będą również szybciej kończyć cały bieg. Oczekujemy, że na podstawie wyniku z 5 km będzie można zbudować model pozwalający z niewielkim błędem oszacować końcowy czas uczestnika.

**H2. Uwzględnienie płci i kategorii wiekowej uczestników poprawia dokładność przewidywania czasu ukończenia biegu na 10 km.**

Zakładamy, że poza wynikiem na 5 km również płeć i kategoria wiekowa mogą dostarczać dodatkowych informacji przydatnych do przewidywania końcowego rezultatu.

Sprawdzimy, czy model wykorzystujący wszystkie trzy cechy osiąga lepsze wyniki niż model oparty wyłącznie na czasie uzyskanym na połowie dystansu.

**H3. Mężczyźni częściej zwalniają na drugiej połowie dystansu 10 km, natomiast kobiety utrzymują bardziej stabilne tempo biegu.**

Zakładamy, że mężczyźni częściej osiągają wolniejsze tempo na drugiej połowie biegu (5–10 km) w porównaniu z pierwszą połową (0–5 km), podczas gdy kobiety utrzymują bardziej równomierne tempo na całym dystansie.

Sprawdzimy, jak zmienia się tempo biegu pomiędzy pierwszymi a ostatnimi 5 km w obu grupach. Pozwoli to ocenić, czy płeć ma związek ze sposobem rozłożenia sił podczas biegu oraz czy różnice te mogą być przydatne przy przewidywaniu końcowego czasu uczestników.

Hipotezy mają charakter statystyczny i zostaną zweryfikowane na podstawie danych. Nie zakładamy z góry, że każda zaobserwowana różnica będzie istotna statystycznie lub duża pod względem praktycznym.

## 4. Kryterium sukcesu projektu
Projekt uznamy za udany, jeśli na podstawie danych z biegu ING Biegnij Warszawo 2026 uda się przygotować i ocenić model pozwalający przewidywać czas ukończenia biegu na 10 km na podstawie wyniku z 5 km oraz danych demograficznych uczestników.

Spełnienie kryterium sukcesu będzie oznaczało, że:
1. Przygotujemy oczyszczony zbiór danych zawierający płeć, kategorię wiekową, czas na 5 km i końcowy czas netto na 10 km.
2. Przeprowadzimy analizę danych, sprawdzając rozkłady czasów oraz zależności między wynikiem z połowy dystansu a czasem końcowym.
3. Zbudujemy co najmniej dwa modele predykcyjne i porównamy ich skuteczność.
4. Ocenimy jakość przewidywań za pomocą odpowiednich miar, takich jak MAE, RMSE i R².
5. Sprawdzimy, czy dodanie płci i kategorii wiekowej poprawia dokładność modelu w porównaniu z wykorzystaniem samego czasu na 5 km.
6. Przedstawimy wyniki za pomocą tabel i wykresów oraz określimy, czy uzyskane przewidywania mogą być przydatne organizatorom biegu.

Za główne kryterium skuteczności modelu przyjmujemy uzyskanie błędu MAE niższego niż w przypadku prostego oszacowania końcowego czasu jako dwukrotności czasu na 5 km. Błąd zostanie przedstawiony również w minutach, aby łatwiej ocenić praktyczną przydatność przewidywań.

Ważnym elementem projektu będzie także pokazanie, w jaki sposób przygotowany model mógłby pomóc organizatorom oszacować liczbę osób docierających do mety w określonych przedziałach czasowych.

## 5. Plan weryfikacji hipotez
- **H1:** Sprawdzenie zależności między czasem na 5 km a czasem na 10 km.

W pierwszym etapie przeanalizujemy zależność między czasem uzyskanym na połowie dystansu a końcowym czasem biegu.
Następnie przygotujemy prosty model przewidujący czas na 10 km wyłącznie na podstawie wyniku z 5 km. Jego wyniki porównamy z rzeczywistymi czasami uczestników.

- **H2:** Sprawdzenie wpływu danych demograficznych na dokładność predykcji.
  
Zbudujemy i porównamy dwa warianty modelu:
-- Model 1 – przewidywanie czasu na 10 km wyłącznie na podstawie czasu na 5 km.
-- Model 2 – przewidywanie czasu na 10 km na podstawie czasu na 5 km, płci i kategorii wiekowej.

Do modelowania możemy wykorzystać np. regresję liniową i Random Forest Regressor.
Porównamy wyniki modeli na tych samych danych testowych, aby sprawdzić, czy uwzględnienie dodatkowych cech poprawia dokładność przewidywań.
  
- **H3:** Sprawdzenie różnic w tempie biegu między kobietami a mężczyznami.
  
Przeanalizujemy, jak zmienia się tempo uczestników pomiędzy pierwszą a drugą połową dystansu 10 km. Na podstawie czasu na 5 km i końcowego czasu na 10 km obliczymy czas pokonania drugiej połowy biegu.
Następnie porównamy wyniki kobiet i mężczyzn, aby sprawdzić, czy mężczyźni częściej zwalniają na drugiej połowie dystansu, a kobiety utrzymują bardziej stabilne tempo.
Sprawdzimy również, czy zaobserwowane różnice mogą mieć znaczenie przy przewidywaniu końcowego czasu ukończenia biegu.

Dane podzielimy na zbiór treningowy i testowy, aby sprawdzić działanie modeli na obserwacjach, których nie wykorzystywano podczas uczenia.
Na końcu porównamy przewidywane i rzeczywiste czasy ukończenia biegu oraz przedstawimy wykresy obrazujące dokładność predykcji.

## 6. Zakres i ograniczenia
Analiza obejmuje jeden bieg --- ING Biegnij Warszawo 2026 --- i jeden dystans: 10 km (dystans = 1, zgodnie ze słownikiem danych).
Ograniczenie zakresu pozwoli skupić się na porównaniu wyników w ramach tej samej imprezy i dystansu.

W analizie nie będziemy traktować identyfikatorów technicznych, takich jak kod czy id_per, jako cech wyjaśniających wynik. Zmienne techniczne i kolumny, które nie wnoszą informacji do postawionych pytań, zostaną pominięte po sprawdzeniu ich zawartości. W szczególności wartości 0 w polu rokur będą traktowane jako brak danych, a nie jako rzeczywisty rok urodzenia.

Wyniki analizy pokażą zależności, a nie dowiodą, że płeć lub wiek bezpośrednio powodują określony rezultat sportowy. Na czas biegu mogą wpływać również inne czynniki, których zbiór może nie zawierać, np. doświadczenie biegowe, trening, stan zdrowia czy warunki startu.

**Główne ograniczenia projektu:**

- Analiza dotyczy tylko jednej imprezy biegowej, dlatego uzyskane wyniki nie muszą być równie dokładne dla innych biegów.
- Model będzie wykorzystywał ograniczoną liczbę cech. Na końcowy wynik mogą wpływać również trening, doświadczenie, kondycja, pogoda i tempo biegu na drugiej połowie dystansu.
- Predykcja będzie możliwa dopiero po przekroczeniu przez uczestnika punktu pomiarowego na 5 km.
- Nieprawidłowe lub brakujące dane mogą zmniejszyć liczbę obserwacji wykorzystanych do modelowania.
