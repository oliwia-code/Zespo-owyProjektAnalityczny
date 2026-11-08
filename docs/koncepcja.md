# Pytanie badawcze i hipotezy  **wersja robocza** - poprawić (kilometry, pomoc organizatorom - gdzie postawić stoiska z piciem itp)

## 1. Temat projektu
Analiza zależności między płcią i kategorią wiekową uczestników biegu ING Biegnij Warszawo 2026 a uzyskiwanymi przez nich wynikami na dystansie 10 km.

Projekt koncentruje się na sprawdzeniu, czy podstawowe cechy uczestników --- płeć oraz przynależność do kategorii wiekowej --- są powiązane z czasem ukończenia biegu. Analiza będzie prowadzona na podstawie wyników udostępnionych przez API Datasport.

## 2. Główne pytanie badawcze
Czy płeć i kategoria wiekowa uczestników ING Biegnij Warszawo 2026 są związane z czasem netto uzyskanym na dystansie 10 km?

Pytanie będzie weryfikowane z wykorzystaniem następujących zmiennych ze zbioru danych:
- plec --- płeć uczestnika (K/M),
- katw --- kategoria wiekowa uczestnika,
- czasnetto --- czas netto ukończenia biegu.

Jako główną miarę wyniku przyjmujemy czas netto, ponieważ mierzy on czas od momentu przekroczenia linii startu przez danego zawodnika do przekroczenia mety. Pozwala to ograniczyć wpływ różnic w czasie oczekiwania na start wynikających z ustawienia uczestników w strefie startowej.

Analiza będzie dotyczyć osób, dla których dostępny jest prawidłowy czas ukończenia biegu. Przed analizą dane zostaną oczyszczone, a wartości czasu zapisane w jednolitej postaci liczbowej, np. w sekundach.

## 3. Hipotezy badawcze
**H1. Istnieje zależność między płcią uczestnika a czasem netto
uzyskanym na dystansie 10 km.**

Oczekujemy, że rozkład czasów netto będzie różnił się między kobietami i mężczyznami. W szczególności zakładamy, że mediana czasu netto mężczyzn będzie niższa niż mediana czasu netto kobiet.

**H2. Czas netto uzyskany na dystansie 10 km różni się pomiędzy
kategoriami wiekowymi uczestników.**

Oczekujemy, że uczestnicy należący do różnych kategorii wiekowych będą osiągać odmienne wyniki. Różnice zostaną sprawdzone poprzez porównanie rozkładów i median czasu netto w poszczególnych kategoriach.

**H3. Zależność między kategorią wiekową a czasem netto może być różna
wśród kobiet i mężczyzn.**

Sprawdzimy, czy różnice w czasie netto pomiędzy kategoriami wiekowymi mają podobny charakter w obu grupach płci. Analiza ta pozwoli ocenić, czy płeć i wiek warto rozpatrywać łącznie, a nie wyłącznie jako niezależne cechy uczestników.

Hipotezy mają charakter statystyczny i zostaną zweryfikowane na podstawie danych. Nie zakładamy z góry, że każda zaobserwowana różnica będzie istotna statystycznie lub duża pod względem praktycznym.

## 4. Kryterium sukcesu projektu
Projekt uznamy za udany, jeśli na podstawie oczyszczonych danych z biegu będziemy w stanie rzetelnie ocenić, czy płeć i kategoria wiekowa uczestników są związane z uzyskanym czasem netto, oraz przedstawić wyniki w sposób czytelny i poparty analizą statystyczną.

Spełnienie kryterium sukcesu będzie oznaczało, że:
1. przygotujemy spójny zbiór danych, w którym możliwe będzie przypisanie uczestnikom płci, kategorii wiekowej i prawidłowego czasu netto;
2. przeprowadzimy analizę opisową, obejmującą m.in. liczebności grup, mediany, kwartyle i rozkłady czasów;
3. zweryfikujemy postawione hipotezy za pomocą odpowiednio dobranych metod statystycznych;
4. przedstawimy wyniki na wykresach i sformułujemy wnioski, wskazując zarówno zauważone zależności, jak i ograniczenia analizy.
Za istotny element sukcesu uznajemy również jawne opisanie braków i ograniczeń danych, np. rekordów bez poprawnego czasu netto lub nieustalonej kategorii wiekowej. Wnioski będą odnosiły się do dostępnego zbioru wyników ING Biegnij Warszawo 2026 i nie będą automatycznie uogólniane na wszystkich biegaczy.

## 5. Plan weryfikacji hipotez
- **H1:** porównanie czasów netto kobiet i mężczyzn. W zależności od rozkładu danych zastosujemy test t-Studenta dla prób niezależnych albo test U Manna--Whitneya.
- **H2:** porównanie czasów netto pomiędzy kategoriami wiekowymi. W zależności od spełnienia założeń zastosujemy analizę wariancji (ANOVA) albo test Kruskala--Wallisa.
- **H3:** porównanie zależności między kategorią wiekową a czasem netto z uwzględnieniem płci, np. za pomocą modelu uwzględniającego oba czynniki i ich interakcję lub analiz przeprowadzonych osobno dla kobiet i mężczyzn.

Dobór testów zostanie ostatecznie potwierdzony po analizie rozkładów, liczebności grup i założeń metod statystycznych. Oprócz wartości p, o ile będzie to możliwe, podamy miary wielkości efektu i przedziały ufności, aby ocenić praktyczne znaczenie zaobserwowanych różnic.

## 6. Zakres i ograniczenia
Analiza obejmuje jeden bieg --- ING Biegnij Warszawo 2026 --- i jeden dystans: 10 km (dystans = 1, zgodnie ze słownikiem danych).
Ograniczenie zakresu pozwoli skupić się na porównaniu wyników w ramach tej samej imprezy i dystansu.

W analizie nie będziemy traktować identyfikatorów technicznych, takich jak kod czy id_per, jako cech wyjaśniających wynik. Zmienne techniczne i kolumny, które nie wnoszą informacji do postawionych pytań, zostaną pominięte po sprawdzeniu ich zawartości. W szczególności wartości 0 w polu rokur będą traktowane jako brak danych, a nie jako rzeczywisty rok urodzenia.

Wyniki analizy pokażą zależności, a nie dowiodą, że płeć lub wiek bezpośrednio powodują określony rezultat sportowy. Na czas biegu mogą wpływać również inne czynniki, których zbiór może nie zawierać, np. doświadczenie biegowe, trening, stan zdrowia czy warunki startu.
