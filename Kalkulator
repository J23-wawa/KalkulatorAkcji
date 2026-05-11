import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kalkulator Marży Akcji", layout="wide")

st.title("📈 Symulator Zysku z Akcji")

# --- SEKCJA DANYCH WEJŚCIOWYCH (3 WIERSZE) ---

# Wiersz 1: Podstawowe informacje o akcji
r1_c1, r1_c2, r1_c3 = st.columns(3)
nazwa = r1_c1.text_input("Nazwa akcji", "Apple")
ilosc = r1_c2.number_input("Ilość akcji", min_value=1, value=10)
cena_zakupu_waluta = r1_c3.number_input("Cena zakupu (w walucie)", min_value=0.01, value=150.0)

# Wiersz 2: Koszty i kursy zakupu
r2_c1, r2_c2, r2_c3 = st.columns(3)
kurs_zakupu = r2_c1.number_input("Kurs waluty przy zakupie", min_value=0.0001, value=4.0000, format="%.4f")
prowizja_zakupu = r2_c2.number_input("Prowizja zakupu (PLN)", min_value=0.0, value=19.0)
prowizja_sprzedazy = r2_c3.number_input("Prowizja sprzedaży (PLN)", min_value=0.0, value=prowizja_zakupu)

# Wiersz 3: Parametry sprzedaży
r3_c1, r3_c2, r3_c3 = st.columns(3)
bazowy_kurs_sprzedazy = r3_c1.number_input("Rynkowy kurs waluty (przyszły)", min_value=0.0001, value=4.1000, format="%.4f")
# Pozostałe kolumny zostawiamy puste dla zachowania symetrii lub można tam dodać inne opcje
r3_c2.write("") 
r3_c3.write("")

st.divider()

# --- LOGIKA OBLICZEŃ ---

# Logika marży bankowej (1%)
efektywny_kurs_sprzedazy = bazowy_kurs_sprzedazy * 0.99 

# Obliczenia kosztów
koszt_calkowity_pln = (ilosc * cena_zakupu_waluta * kurs_zakupu) + prowizja_zakupu
laczna_prowizja = prowizja_zakupu + prowizja_sprzedazy

# --- WYNIKI I ANALIZA ---

st.subheader(f"Analiza dla: {nazwa}")
res1, res2, res3 = st.columns(3)
res1.metric("Koszt zakupu", f"{koszt_calkowity_pln:,.2f} PLN")
res2.metric("Kurs rynkowy", f"{bazowy_kurs_sprzedazy:.4f}")
res3.metric("Kurs po marży (-1%)", f"{efektywny_kurs_sprzedazy:.4f}")

# Generowanie danych do tabeli (zakres 3% - 15%)
wyniki = []
for procent in range(3, 16):
    wzrost = 1 + (procent / 100)
    przyszla_cena_waluta = cena_zakupu_waluta * wzrost
    
    # Wartość sprzedaży w PLN po kursie z marżą banku
    wartosc_sprzedazy_pln = (ilosc * przyszla_cena_waluta * efektywny_kurs_sprzedazy) - prowizja_sprzedazy
    zysk_netto = wartosc_sprzedazy_pln - koszt_calkowity_pln
    marza_proc = (zysk_netto / koszt_calkowity_pln) * 100
    
    wyniki.append({
        "Cena akcji": round(przyszla_cena_waluta, 2),
        "Wzrost ceny": f"+{procent}%",
        "Wartość w PLN": round(wartosc_sprzedazy_pln, 2),
        "Prowizja (suma)": round(laczna_prowizja, 2),
        "Zysk netto": round(zysk_netto, 2),
        "Realna marża": round(marza_proc, 2)
    })

df = pd.DataFrame(wyniki)

# Funkcja kolorująca wiersze
def style_rows(row):
    color = ''
    if row['Realna marża'] > 8:
        color = 'background-color: #2ecc71; color: white'  # Zielony
    elif row['Realna marża'] > 3:
        color = 'background-color: #f1c40f; color: black'  # Żółty
    return [color] * len(row)

# Wyświetlanie tabeli
st.dataframe(
    df.style.apply(style_rows, axis=1).format({
        "Cena akcji": "{:.2f}",
        "Wartość w PLN": "{:,.2f}",
        "Prowizja (suma)": "{:,.2f}",
        "Zysk netto": "{:,.2f}",
        "Realna marża": "{:.2f}%"
    }),
    use_container_width=True,
    height=500
)
