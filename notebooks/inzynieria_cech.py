import pandas as pd
import numpy as np


def dodaj_nowe_zmienne(df):

    ROK_BIEGU = 2026

    df['rokur'] = pd.to_numeric(df['rokur'], errors='coerce')
    df['wiek_numeryczny'] = ROK_BIEGU - df['rokur']
    df.loc[df['rokur'] == 0, 'wiek_numeryczny'] = np.nan

    df['czy_lokals'] = df['miasto'].fillna('').astype(str).str.upper().apply(
        lambda x: 1 if 'WARSZAWA' in x else 0
    )

    # funkcja pomocnicza (zmiana dat na jeden format)
    def time_to_seconds(t):
        if pd.isna(t) or str(t).strip() == '':
            return np.nan
        try:
            t = str(t).replace(',', '.')
            h, m, s = t.split(':')
            return int(h) * 3600 + int(m) * 60 + float(s)
        except:
            return np.nan

    start_sec = df['start'].apply(time_to_seconds)
    opoznienie = start_sec - (12 * 3600)

    # do 2 min (Szybki), 2-10 min (Średni), powyżej 10 min (Wolny)
    df['koszyk_startowy'] = pd.cut(
        opoznienie,
        bins=[-np.inf, 120, 600, np.inf],
        labels=['Szybki', 'Sredni', 'Wolny']
    )

    df['czas1_sek'] = df['czas1'].apply(time_to_seconds)
    df['czasnetto_sek'] = df['czasnetto'].apply(time_to_seconds)
    df['estymacja_naiwna'] = df['czas1_sek'] * 2

    return df

# Sposób użycia w głównym skrypcie:
if __name__ == "__main__":
    df_raw = pd.read_csv('../data/dane_oczyszczone_biegnij_warszawo.csv', dtype=str)
    # df_raw = pd.read_csv('../data/dane_surowe_biegnij_warszawo.csv', dtype=str)
    df_wzbogacone = dodaj_nowe_zmienne(df_raw)
    sciezka_wyjsciowa = '../data/dane_wzbogacone_biegnij_warszawo.csv'
    df_wzbogacone.to_csv(sciezka_wyjsciowa, index=False, encoding='utf-8')
    print(f"Zapisano plik z nowymi cechami: {sciezka_wyjsciowa}")
