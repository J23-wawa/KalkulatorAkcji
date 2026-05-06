import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kalkulator Marży Akcji", layout="wide")

st.title("📈 Symulator Zysku z Akcji")

# Pasek boczny - Dane wejściowe
st.sidebar.header("1. Dane zakupu")
nazwa = st.sidebar.text_input("Nazwa akcji", "Apple")
ilosc = st.sidebar.number_input("Ilość akcji", min_value=1, value=10)
cena_zakupu_waluta = st.sidebar.number_input("Cena zakupu (w walucie)", min_value=0.01, value=150.0)
kurs_zakupu = st.sidebar.number_input("Kurs waluty przy zakupie", min_value=0.0001, value=4.0000, format="%.4f")
prowizja_zakupu = st.sidebar.number_input("Prowizja zakupu (PLN)", min_value=0.0, value=19.0)

st.sidebar.header("2. Parametry sprzedaży")
bazowy_kurs_sprzedazy = st.sidebar.number_input("Rynkowy kurs waluty (przyszły)", min_value=0.0001, value=4.1000, format="%.4f")
prowizja_sprzedazy = st.sidebar.number_input("Prowizja sprzedaży (PLN)", min_value=0.0, value=prowizja_zakupu)

# Logika marży bankowej (1%)
efektywny_kurs_sprzedazy = bazowy_kurs_sprzedazy * 0.99 

# Obliczenia kosztów
koszt_calkowity_pln = (ilosc * cena_zakupu_waluta * kurs_zakupu) + prowizja_zakupu

st.subheader(f"Analiza dla: {nazwa}")
c1, c2, c3 = st.columns(3)
c1.metric("Koszt zakupu", f"{koszt_calkowity_pln:,.2f} PLN")
c2.metric("Kurs rynkowy", f"{bazowy_kurs_sprzedazy:.4f}")
c3.metric("Kurs po marży (-1%)", f"{efektywny_kurs_sprzedazy:.4f}")

# Generowanie danych do tabeli
wyniki = []
for procent in range(1, 11):
    wzrost = 1 + (procent / 100)
    przyszla_cena_waluta = cena_zakupu_waluta * wzrost
    
    wartosc_sprzedazy_pln = (ilosc * przyszla_cena_waluta * efektywny_kurs_sprzedazy) - prowizja_sprzedazy
    zysk_netto = wartosc_sprzedazy_pln - koszt_calkowity_pln
    marza_proc = (zysk_netto / koszt_calkowity_pln) * 100
    
    wyniki.append({
        "Wzrost ceny akcji": f"+{procent}%",
        "Cena akcji (waluta)": round(przyszla_cena_waluta, 2),
        "Wartość w PLN": round(wartosc_sprzedazy_pln, 2),
        "Zysk netto (PLN)": round(zysk_netto, 2),
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

# Wyświetlanie sformatowanej tabeli
st.dataframe(
    df.style.apply(style_rows, axis=1).format({
        "Wartość w PLN": "{:,.2f}",
        "Zysk netto (PLN)": "{:,.2f}",
        "Realna marża": "{:.2f}%"
    }),
    use_container_width=True
)
