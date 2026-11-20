# Import bibliotek i wczytanie danych
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from sklearn.model_selection import train_test_split
from sklearn.metrics import (mean_absolute_error, mean_squared_error,
                             r2_score, mean_absolute_percentage_error)
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.inspection import permutation_importance

TEST_SIZE = 0.20
RANDOM_STATE = 42
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'figure.dpi': 120, 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.titleweight': 'bold'})
KOLOR_GB = '#087F8C'
KOLOR_LR = '#5274AA'
KOLOR_BAZA = '#A0AAB8'

nazwa_pliku = 'dane_wzbogacone_biegnij_warszawo.csv'
sciezki = [Path(nazwa_pliku), Path('data') / nazwa_pliku]
sciezka = next((p for p in sciezki if p.exists()), None)
if sciezka is None:
    from google.colab import files
    uploaded = files.upload()
    if nazwa_pliku not in uploaded:
        raise FileNotFoundError(f'Wgraj plik {nazwa_pliku}')
    sciezka = Path(nazwa_pliku)

df = pd.read_csv(sciezka, low_memory=False)
print(f'Wczytano {len(df)} rekordów.')

# Przygotowanie danych
CECHY_WEJSCIOWE = ['czas1_sek', 'estymacja_naiwna', 'wiek_numeryczny',
                   'czy_lokals', 'plec', 'katw', 'koszyk_startowy']
ZMIENNA_DOCELOWA = 'czasnetto_sek'

for col in ['czas1_sek', 'czasnetto_sek', 'estymacja_naiwna', 'wiek_numeryczny', 'czy_lokals']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
if 'dystans' in df.columns:
    df = df[pd.to_numeric(df['dystans'], errors='coerce') == 1].copy()
przed_filtrem = len(df)
df_model = df.dropna(subset=['czas1_sek', 'czasnetto_sek', 'estymacja_naiwna']).copy()
df_model = df_model[(df_model['czas1_sek'] > 0) &
                    (df_model['czasnetto_sek'] > 0) &
                    (df_model['czasnetto_sek'] > df_model['czas1_sek'])].copy()
for col in ['plec', 'katw', 'koszyk_startowy']:
    df_model[col] = (df_model[col].astype(str).str.strip()
                     .replace({'': np.nan, 'nan': np.nan, 'None': np.nan}))
X = df_model[CECHY_WEJSCIOWE].copy()
y = df_model[ZMIENNA_DOCELOWA].copy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)

display(pd.DataFrame({'Etap':['Przed filtrem (10 km)','Odrzucone','Poprawne','Train','Test'],
                      'Liczba':[przed_filtrem,przed_filtrem-len(X),len(X),len(X_train),len(X_test)]}))
display(df_model[CECHY_WEJSCIOWE+[ZMIENNA_DOCELOWA]].head())
fig, ax = plt.subplots(figsize=(8,2.1))
ax.barh(['Podział danych'],len(X_train),color=KOLOR_LR,label='Train')
ax.barh(['Podział danych'],len(X_test),left=len(X_train),color=KOLOR_GB,label='Test')
ax.text(len(X_train)/2,0,f'{len(X_train)} (80%)',ha='center',va='center',color='white',weight='bold')
ax.text(len(X_train)+len(X_test)/2,0,f'{len(X_test)} (20%)',ha='center',va='center',color='white',weight='bold')
ax.set(xlim=(0,len(X)),xlabel='Liczba uczestników'); plt.tight_layout(); plt.show()

# Funkcje pomocnicze oraz modele bazowe
def stworz_preprocessor(cechy_num, cechy_kat):
    return ColumnTransformer([
        ('num', Pipeline([('imputer', SimpleImputer(strategy='median')),
                          ('scaler', StandardScaler())]), cechy_num),
        ('kat', Pipeline([('imputer', SimpleImputer(strategy='most_frequent')),
                          ('ohe', OneHotEncoder(handle_unknown='ignore', sparse_output=False))]), cechy_kat)
    ])

def ocen_model(y_true, y_pred, nazwa_modelu):
    mae = mean_absolute_error(y_true,y_pred)
    rmse = np.sqrt(mean_squared_error(y_true,y_pred))
    return {'Model':nazwa_modelu, 'MAE [sek]':mae, 'MAE [min]':mae/60,
            'RMSE [sek]':rmse, 'RMSE [min]':rmse/60,
            'R2':r2_score(y_true,y_pred), 'MAPE [%]':100*mean_absolute_percentage_error(y_true,y_pred)}

warianty = [
    ('1: 5 km', ['czas1_sek'], []),
    ('2: 5 km + demografia', ['czas1_sek'], ['plec','katw']),
    ('3: Pełne cechy', ['czas1_sek','wiek_numeryczny','czy_lokals'], ['plec','katw','koszyk_startowy'])
]
modele, predykcje, wyniki = {}, {}, []

def zapisz_wynik(nazwa, pred, model=None):
    predykcje[nazwa] = pd.Series(pred,index=y_test.index)
    wyniki.append(ocen_model(y_test,pred,nazwa))
    if model is not None:
        modele[nazwa] = model

def trenuj_i_ocen(nazwa, model):
    model.fit(X_train,y_train)
    zapisz_wynik(nazwa,model.predict(X_test),model)

# Baseline 0 i 1
trenuj_i_ocen('DummyRegressor', DummyRegressor(strategy='mean'))
zapisz_wynik('Model naiwny',X_test['estymacja_naiwna'].to_numpy())
# Regresja liniowa – trzy warianty
for wariant, cechy_num, cechy_kat in warianty:
    lr = Pipeline([('prep',stworz_preprocessor(cechy_num,cechy_kat)),('model',LinearRegression())])
    trenuj_i_ocen(f'LR {wariant}',lr)
print('Oceniono pięć modeli bazowych.')

# Model zaawansowany - Gradient Boosting Regressor
for wariant, cechy_num, cechy_kat in warianty:
    gb = Pipeline([
        ('prep',stworz_preprocessor(cechy_num,cechy_kat)),
        ('model',GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=3,
            min_samples_leaf=20,
            loss='absolute_error',
            random_state=RANDOM_STATE
        ))
    ])
    trenuj_i_ocen(f'GB {wariant}',gb)
    print(f'Zakończono: GB {wariant}')

# Tabela porównawcza – zbiór testowy
df_wyniki = pd.DataFrame(wyniki).sort_values('MAE [sek]').reset_index(drop=True)
metryki = df_wyniki.set_index('Model')
mae_naiwny = metryki.loc['Model naiwny','MAE [sek]']
df_wyniki['Poprawa MAE [sek]'] = mae_naiwny-df_wyniki['MAE [sek]']
formaty = {col:'{:.2f}' for col in df_wyniki.columns if col!='Model'}
formaty['R2']='{:.4f}'
display(df_wyniki.style.format(formaty).hide(axis='index')
        .highlight_min(subset=['MAE [sek]','MAE [min]','RMSE [sek]','RMSE [min]','MAPE [%]'],color='#C9E9DC')
        .highlight_max(subset=['R2','Poprawa MAE [sek]'],color='#C9E9DC'))
najlepszy = df_wyniki.iloc[0]
print(f"Najniższy MAE: {najlepszy['Model']} – {najlepszy['MAE [sek]']:.2f} sek")
print(f"Poprawa względem naiwnego: {najlepszy['Poprawa MAE [sek]']:.2f} sek")
print('Kryterium sukcesu na teście:', 'SPEŁNIONE' if najlepszy['MAE [sek]']<mae_naiwny else 'NIESPEŁNIONE')

# Wykresy porównujące modele
def kolor_modelu(nazwa):
    return KOLOR_GB if nazwa.startswith('GB') else KOLOR_LR if nazwa.startswith('LR') else KOLOR_BAZA

def wykres_metryki(ax,dane,metryka,tytul):
    dane = dane.sort_values(metryka,ascending=metryka!='R2')
    bars = ax.barh(dane['Model'],dane[metryka],color=[kolor_modelu(m) for m in dane['Model']])
    ax.invert_yaxis()
    ax.bar_label(bars,fmt='%.4f' if metryka=='R2' else '%.2f',padding=4,fontsize=9)
    ax.set(title=tytul,xlabel=metryka)
    if metryka=='R2':
        ax.set_xlim(dane[metryka].min()-.003,dane[metryka].max()+.004)
    else:
        ax.set_xlim(0,dane[metryka].max()*1.2)
    ax.grid(axis='y',visible=False)

fig,ax=plt.subplots(figsize=(10,5))
wykres_metryki(ax,df_wyniki,'MAE [sek]','MAE wszystkich modeli – mniej znaczy lepiej')
plt.tight_layout(); plt.show()

por = df_wyniki[df_wyniki['Model']!='DummyRegressor']
fig,axes=plt.subplots(2,2,figsize=(16,8))
for ax,metryka,tytul in zip(axes.flat,['MAE [sek]','RMSE [sek]','R2','MAPE [%]'],
    ['MAE – mniej znaczy lepiej','RMSE – mniej znaczy lepiej','R² – więcej lepiej (skala zawężona)','MAPE – mniej znaczy lepiej']):
    wykres_metryki(ax,por,metryka,tytul)
fig.suptitle('Szczegółowe porównanie modeli (bez DummyRegressor)',fontsize=16,weight='bold')
plt.tight_layout(); plt.show()

por = por[por['Model']!='Model naiwny'].sort_values('Poprawa MAE [sek]')
fig,ax=plt.subplots(figsize=(10,4))
bars=ax.barh(por['Model'],por['Poprawa MAE [sek]'],color=[kolor_modelu(m) for m in por['Model']])
ax.bar_label(bars,fmt='%+.2f s',padding=4); ax.axvline(0,color='black'); ax.margins(x=.2)
ax.set(title='Poprawa względem naiwnej predykcji',xlabel='Zmniejszenie MAE [sek]')
plt.tight_layout(); plt.show()
