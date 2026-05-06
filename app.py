import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kalkulator Marży Akcji", layout="wide")

st.title("📈 Symulator Zysku z Akcji")

# Pasek boczny - Dane wejściowe
st.sidebar.header("Dane zakupu")
nazwa = st.sidebar.text_input("Nazwa akcji", "Apple")
ilosc = st.sidebar.number_input("Ilość akcji", min_value=1, value=10)
cena_zakupu_waluta = st.sidebar.number_input("Cena zakupu (w walucie)", min_value=0.01, value=150.0)
kurs_zakupu = st.sidebar.number_input("Kurs waluty przy zakupie", min_value=0.01, value=4.0)
prowizja_zakupu = st.sidebar.number_input("Prowizja zakupu (PLN)", min_value=0.0, value=19.0)

st.sidebar.header("Parametry sprzedaży")
kurs_sprzedazy = st.sidebar.number_input("Przyszły kurs waluty", min_value=0.01, value=4.10)
prowizja_sprzedazy = st.sidebar.number_input("Prowizja sprzedaży (PLN)", min_value=0.0, value=prowizja_zakupu)

# Obliczenia bazowe
koszt_calkowity_pln = (ilosc * cena_zakupu_waluta * kurs_zakupu) + prowizja_zakupu

st.subheader(f"Analiza dla: {nazwa}")
col1, col2 = st.columns(2)
col1.metric("Całkowity koszt zakupu", f"{koszt_calkowity_pln:,.2f} PLN")

# Generowanie skali zysku 1-10%
wyniki = []
for procent in range(1, 11):
    wzrost = 1 + (procent / 100)
    przyszla_cena_waluta = cena_zakupu_waluta * wzrost
    wartosc_sprzedazy_pln = (ilosc * przyszla_cena_waluta * kurs_sprzedazy) - prowizja_sprzedazy
    zysk_netto = wartosc_sprzedazy_pln - koszt_calkowity_pln
    marza = (zysk_netto / koszt_calkowity_pln) * 100
    
    wyniki.append({
        "Wzrost ceny (%)": f"{procent}%",
        "Przyszła cena (waluta)": f"{przyszla_cena_waluta:.2f}",
        "Wartość sprzedaży (PLN)": f"{wartosc_sprzedazy_pln:,.2f}",
        "Zysk netto (PLN)": f"{zysk_netto:,.2f}",
        "Marża (%)": f"{marza:.2f}%"
    })

df_wyniki = pd.DataFrame(wyniki)
st.table(df_wyniki)
