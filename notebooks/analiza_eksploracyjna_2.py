import os
import pandas as pd

# Ścieżki lokalne (PyCharm) – działają niezależnie od katalogu roboczego
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
data_dir = os.path.join(project_root, 'data')
os.makedirs(data_dir, exist_ok=True)    # Informacje o bazie
file_path = os.path.join(data_dir, 'dane_surowe_biegnij_warszawo.csv')
df = pd.read_csv(file_path, low_memory=False)

print("Liczba rekordów:", len(df))
print("Liczba kolumn:", len(df.columns))

# WNIOSEK
# Liczba rekordów: 9887
# Liczba kolumn: 87 - nie wszystkie będą użyte w analizie

# Kolumny
print(df.columns)
print(df.head())
print(df.describe(include='all'))

"""# BRAKUJĄCE DANE I USUWANIE NIEPOTRZEBNYCH KOLUMN"""

# Usunięcie zawodników bez wyniku
bez_wyniku = df[df['czasnetto'].isna()]
df = df[df['czasnetto'].notna()].copy()

print("Liczba zawodników bez wyniku:", len(bez_wyniku))
print("Liczba zawodników uwzględnionych w analizie:", len(df))

# Analiza braków
missing_data = pd.DataFrame({
    'Liczba braków': df.isnull().sum(),
    'Procent braków (%)': (df.isnull().sum() / len(df) * 100).round(2)
}).sort_values(by='Liczba braków', ascending=True)
print(missing_data)

# Puste kolumny
empty_columns = df.columns[df.isnull().all()].tolist()
print("Liczba pustych kolumn:", len(empty_columns))
print("Puste kolumny:")
print(empty_columns)

# Usunięcie pustych kolumn i z wieloma brakami (>50%)
df = df.dropna(axis=1, thresh=len(df) * 0.5)
print("Liczba kolumn po usunięciu:", len(df.columns))
print("Pozostałe kolumny:")
print(df.columns.tolist())

# Kolumny bez braków
print(missing_data[missing_data['Liczba braków'] == 0])

# Analiza braków po usunięciu pustych kolumn
missing_data = pd.DataFrame({
    'Liczba braków': df.isnull().sum(),
    'Procent braków (%)': (df.isnull().sum() / len(df) * 100).round(2)
}).sort_values(by='Liczba braków', ascending=True)
print(missing_data[missing_data['Liczba braków'] > 0])

# Funkcja pomocnicza
def check_missing(df, column_name):
    if column_name not in df.columns:
        print(f"Kolumna '{column_name}' nie istnieje w zbiorze danych.")
        return

    missing_count = df[column_name].isnull().sum()
    missing_percent = (missing_count / len(df) * 100).round(2)

    print(f"Kolumna: {column_name}")
    print(f"Liczba braków: {missing_count}")
    print(f"Procent braków: {missing_percent}%")

# Kolumny do usunięcia, niepotrzebne do analizy
# UWAGA: zostawiamy 'start' – jest potrzebny do inżynierii cech (koszyk_startowy) i godziny mety
columns_to_drop = [
    'nazwisko', 'imie', 'druzyna', 'mscnetto',
    'czaswsp', 'meta', 'kraj',
    'anonim', 'id_per'
]
df = df.drop(columns=columns_to_drop, errors='ignore')

# Uzupełnienie niepełnych kolumn: miasto (1 brak)
df['miasto'] = df['miasto'].fillna('Nieznane')

print("Liczba kolumn po usunięciu:", len(df.columns))
print("Pozostałe kolumny:")
print(df.columns.tolist())

missing_data = pd.DataFrame({
    'Liczba braków': df.isnull().sum(),
    'Procent braków (%)': (df.isnull().sum() / len(df) * 100).round(2)
}).sort_values(by='Liczba braków', ascending=True)
print(missing_data[missing_data['Liczba braków'] > 0])

# Zapis oczyszczonego zbioru do dalszych etapów (Zadanie 3 – inżynieria cech)
clean_output_file = os.path.join(data_dir, 'dane_oczyszczone_biegnij_warszawo.csv')
df.to_csv(clean_output_file, index=False, encoding='utf-8')
print(f"Zapisano oczyszczony zbiór do: {clean_output_file}")