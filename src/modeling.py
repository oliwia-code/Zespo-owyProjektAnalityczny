"""
Schemat walidacji oraz zestaw metryk zostały ustalone przed wytrenowaniem
i oceną jakiegokolwiek modelu predykcyjnego (ochrona przed p-hackingiem).

1. Podział danych: Train/Test Split 80% / 20% (random_state=42)
   Uzasadnienie:
   Zbiór wyników biegu ING Biegnij Warszawo 2026 obejmuje ponad 9 tys.
   obserwacji. Wydzielenie 20% danych na zbiór testowy (~1800–1900 biegaczy)
   zapewnia odpowiednio dużą i reprezentatywną próbę do stabilnej oceny błędu
   generalizacji. Stałe ziarno losowości (random_state=42) gwarantuje pełną
   odtwarzalność eksperymentu – wszystkie modele (bazowe i zaawansowane) są
   uczone i testowane na dokładnie tych samych obserwacjach. Wszelkie operacje
   przetwarzania (imputacja braków, skalowanie, kodowanie One-Hot) są zamknięte
   w obiektach Pipeline i dopasowywane wyłącznie na zbiorze treningowym
   (eliminacja wycieku danych – data leakage).

2. Metryki oceny (regresja – predykcja czasu netto na 10 km w sekundach):
   - MAE (Mean Absolute Error) [sek i min]: główna metryka projektu i kryterium
     sukcesu. Bezpośrednio informuje organizatora, o ile średnio sekund/minut
     model myli się przy szacowaniu momentu wbiegnięcia biegacza na metę.
     Jest odporna na pojedyncze obserwacje odstające (np. kontuzja na trasie).
   - RMSE (Root Mean Squared Error) [sek i min]: silniej karze duże błędy,
     pokazując wrażliwość modelu na zawodników gwałtownie tracących tempo.
   - R2 (współczynnik determinacji): określa, jaki odsetek wariancji czasu
     końcowego wyjaśnia model.
   - MAPE (Mean Absolute Percentage Error) [%]: błąd względny wyrażony
     procentowo, pozwalający ocenić precyzję niezależnie od poziomu biegacza
     (zarówno dla elity ~30 min, jak i amatorów >60 min).
"""

from pathlib import Path
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    mean_absolute_percentage_error,
)
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

TEST_SIZE = 0.20
RANDOM_STATE = 42

CECHY_WEJSCIOWE = [
    'czas1_sek',
    'estymacja_naiwna',
    'wiek_numeryczny',
    'czy_lokals',
    'plec',
    'katw',
    'koszyk_startowy',
]
ZMIENNA_DOCELOWA = 'czasnetto_sek'


def znajdz_plik_danych(nazwa_pliku: str = 'dane_wzbogacone_biegnij_warszawo.csv') -> Path:
    project_root = Path(__file__).resolve().parent.parent
    sciezka = project_root / 'data' / nazwa_pliku
    if not sciezka.exists():
        raise FileNotFoundError(
            f"Nie znaleziono pliku: {sciezka}. "
            "Uruchom najpierw analizę eksploracyjną i inżynierię cech"
        )
    return sciezka


def wczytaj_i_podziel_dane(
    nazwa_pliku: str = 'dane_wzbogacone_biegnij_warszawo.csv',
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_STATE,
):
    """
    Wczytuje wzbogacony zbiór danych, filtruje go zgodnie z zakresem projektu
    (dystans 10 km, poprawne czasy na 5 km i mecie) i zwraca podział 80/20.
    """
    sciezka = znajdz_plik_danych(nazwa_pliku)
    df = pd.read_csv(sciezka, low_memory=False)

    # Konwersja kolumn numerycznych na liczby
    kolumny_num = ['czas1_sek', 'czasnetto_sek', 'estymacja_naiwna', 'wiek_numeryczny', 'czy_lokals']
    for col in kolumny_num:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Zakres projektu: wyłącznie bieg główny 10 km (dystans == 1)
    if 'dystans' in df.columns:
        df = df[pd.to_numeric(df['dystans'], errors='coerce') == 1].copy()

    # Usunięcie rekordów z brakującym lub fizycznie błędnym czasem 5 km / 10 km
    przed_filtrem = len(df)
    df_model = df.dropna(subset=['czas1_sek', 'czasnetto_sek', 'estymacja_naiwna']).copy()
    df_model = df_model[
        (df_model['czas1_sek'] > 0)
        & (df_model['czasnetto_sek'] > 0)
        & (df_model['czasnetto_sek'] > df_model['czas1_sek'])
    ].copy()
    odrzuceni = przed_filtrem - len(df_model)

    # Ujednolicenie braków w kolumnach kategorycznych
    for col in ['plec', 'katw', 'koszyk_startowy']:
        df_model[col] = (
            df_model[col]
            .astype(str)
            .str.strip()
            .replace({'': np.nan, 'nan': np.nan, 'None': np.nan})
        )

    X = df_model[CECHY_WEJSCIOWE].copy()
    y = df_model[ZMIENNA_DOCELOWA].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    info = {
        'sciezka': str(sciezka),
        'wiersze_po_filtrze': len(df_model),
        'odrzuceni_bledny_czas': odrzuceni,
        'train_n': len(X_train),
        'test_n': len(X_test),
    }
    return X_train, X_test, y_train, y_test, info


def ocen_model(y_true, y_pred, nazwa_modelu: str) -> dict:
    """Oblicza zestaw metryk oceny dla regresji."""
    mae_sek = mean_absolute_error(y_true, y_pred)
    rmse_sek = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    r2 = r2_score(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100.0

    return {
        'Model': nazwa_modelu,
        'MAE [sek]': round(mae_sek, 2),
        'MAE [min]': round(mae_sek / 60.0, 2),
        'RMSE [sek]': round(rmse_sek, 2),
        'RMSE [min]': round(rmse_sek / 60.0, 2),
        'R2': round(r2, 4),
        'MAPE [%]': round(mape, 2),
    }


def stworz_preprocessor(cechy_num: list[str], cechy_kat: list[str]) -> ColumnTransformer:
    """
    Tworzy potok przetwarzania (imputacja + skalowanie + One-Hot Encoding)
    bezpieczny przed wyciekiem danych (fit tylko na X_train wewnątrz Pipeline).
    """
    return ColumnTransformer(
        transformers=[
            ('num', Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler()),
            ]), cechy_num),
            ('kat', Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('ohe', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
            ]), cechy_kat),
        ]
    )


def uruchom_modele_bazowe(X_train, X_test, y_train, y_test) -> list[dict]:
    """
    ZADANIE 4 (Część 1 – Baseline):
    Trenuje i ocenia modele stanowiące punkt odniesienia oraz weryfikuje H1 i H2.
    """
    wyniki = []

    # 1. Baseline 0: Średnia arytmetyczna (DummyRegressor – wymóg tabeli z Zadania 4)
    dummy = DummyRegressor(strategy='mean')
    dummy.fit(X_train, y_train)
    wyniki.append(ocen_model(y_test, dummy.predict(X_test), 'Baseline 0: Średnia (DummyRegressor)'))

    # 2. Baseline 1: Naiwna estymacja domenowa (2 * czas na 5 km – kryterium sukcesu)
    y_pred_naiwny = X_test['estymacja_naiwna'].values
    wyniki.append(ocen_model(y_test, y_pred_naiwny, 'Baseline 1: Naiwny (2 * czas_5km)'))

    # 3. Baseline 2a: Regresja liniowa – tylko czas 5 km (Model 1 -> Hipoteza H1)
    lr_h1 = LinearRegression()
    lr_h1.fit(X_train[['czas1_sek']], y_train)
    y_pred_lr_h1 = lr_h1.predict(X_test[['czas1_sek']])
    wyniki.append(ocen_model(y_test, y_pred_lr_h1, 'Baseline 2a: Regresja liniowa (tylko 5 km - H1)'))

    # 4. Baseline 2b: Regresja liniowa – 5 km + płeć + katw (Model 2 -> Hipoteza H2)
    prep_h2 = stworz_preprocessor(cechy_num=['czas1_sek'], cechy_kat=['plec', 'katw'])
    lr_h2 = Pipeline([
        ('prep', prep_h2),
        ('model', LinearRegression()),
    ])
    lr_h2.fit(X_train, y_train)
    wyniki.append(ocen_model(y_test, lr_h2.predict(X_test), 'Baseline 2b: Regresja liniowa (5 km + demografia - H2)'))

    # 5. Baseline 2c: Regresja liniowa – pełny zestaw z cechami z Zadania 3
    # (bez 'estymacja_naiwna', która jest liniową kopią 'czas1_sek' -> współliniowość)
    prep_pelny = stworz_preprocessor(
        cechy_num=['czas1_sek', 'wiek_numeryczny', 'czy_lokals'],
        cechy_kat=['plec', 'katw', 'koszyk_startowy'],
    )
    lr_pelny = Pipeline([
        ('prep', prep_pelny),
        ('model', LinearRegression()),
    ])
    lr_pelny.fit(X_train, y_train)
    wyniki.append(ocen_model(y_test, lr_pelny.predict(X_test), 'Baseline 2c: Regresja liniowa (pełne cechy + Zad. 3)'))

    return wyniki


def wydrukuj_podsumowanie_hipotez(df_wyniki: pd.DataFrame) -> None:
    """Wypisuje zwięzłe porównanie wyników względem kryterium sukcesu oraz H1/H2."""
    mae_naiwny = df_wyniki.loc[df_wyniki['Model'].str.contains('Baseline 1'), 'MAE [sek]'].iloc[0]
    mae_h1 = df_wyniki.loc[df_wyniki['Model'].str.contains('Baseline 2a'), 'MAE [sek]'].iloc[0]
    mae_h2 = df_wyniki.loc[df_wyniki['Model'].str.contains('Baseline 2b'), 'MAE [sek]'].iloc[0]
    mae_pelny = df_wyniki.loc[df_wyniki['Model'].str.contains('Baseline 2c'), 'MAE [sek]'].iloc[0]

    print("\n=== SZYBKA WERYFIKACJA NA MODELACH BAZOWYCH ===")
    print(f"Kryterium sukcesu (MAE < Baseline 1 = {mae_naiwny} s):")
    print(f"  - Regresja liniowa (H1):         poprawa o {mae_naiwny - mae_h1:+.2f} sek ({(mae_naiwny - mae_h1) / 60:+.2f} min)")
    print(f"  - Regresja liniowa (H2):         poprawa o {mae_naiwny - mae_h2:+.2f} sek ({(mae_naiwny - mae_h2) / 60:+.2f} min)")
    print(f"  - Regresja liniowa (pełne+cechy powstałe w wyniku inżynierii): poprawa o {mae_naiwny - mae_pelny:+.2f} sek ({(mae_naiwny - mae_pelny) / 60:+.2f} min)")
    print(f"Wpływ demografii (H2 vs H1):       różnica MAE = {mae_h1 - mae_h2:+.2f} sek")
    print(f"Wpływ powstałych cech (2c vs 2b): różnica MAE = {mae_h2 - mae_pelny:+.2f} sek")


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 140)

    X_train, X_test, y_train, y_test, info = wczytaj_i_podziel_dane()
    print(f"Źródło danych: {info['sciezka']}")
    print(f"Odrzucono rekordy z brakującym/błędnym czasem 5 km lub 10 km: {info['odrzuceni_bledny_czas']}")
    print(f"Obserwacje do modelowania: {info['wiersze_po_filtrze']} "
          f"(train 80%: {info['train_n']}, test 20%: {info['test_n']})\n")

    wyniki_ewaluacji = uruchom_modele_bazowe(X_train, X_test, y_train, y_test)

    #do tych wynikow sie doklej natalia i w tym pliku mozesz to robic, a z bardziej zaawansowanych modeli mozesz uzyc RandomForestRegressor, GradientBoostingRegressor
    df_wyniki = pd.DataFrame(wyniki_ewaluacji)
    print("=== TABELA PORÓWNAWCZA MODELI (ZBIÓR TESTOWY 20%) ===")
    print(df_wyniki.to_string(index=False))

    wydrukuj_podsumowanie_hipotez(df_wyniki)