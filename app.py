import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kalkulator Marży Akcji", layout="wide")

st.title("📈 Symulator Zysku z Akcji")
st.info("Obliczenia uwzględniają 1% marży banku doliczanej do kursu wymiany przy sprzedaży.")

# Pasek boczny - Dane wejściowe
st.sidebar.header("1. Dane zakupu")
nazwa = st.sidebar.text_input("Nazwa akcji", "Apple")
ilosc = st.sidebar.number_input("Ilość akcji", min_value=1, value=10)
cena_zakupu_waluta = st.sidebar.number_input("Cena zakupu (w walucie)", min_value=0.01, value=150.0)
kurs_zakupu = st.sidebar.number_input("Kurs waluty przy zakupie", min_value=0.01, value=4.0)
prowizja_zakupu = st.sidebar.number_input("Prowizja zakupu (PLN)", min_value=0.0, value=19.0)

st.sidebar.header("2. Parametry sprzedaży")
bazowy_kurs_sprzedazy = st.sidebar.number_input("Rynkowy kurs waluty (przyszły)", min_value=0.01, value=4.10)
prowizja_sprzedazy = st.sidebar.number_input("Prowizja sprzedaży (PLN)", min_value=0.0, value=prowizja_zakupu)

# Logika marży bankowej (1%)
# Przy sprzedaży akcji i wymianie waluty na PLN, bank stosuje kurs o 1% gorszy dla klienta
efektywny_kurs_sprzedazy = bazowy_kurs_sprzedazy * 0.99 

# Obliczenia bazowe kosztów
koszt_calkowity_pln = (ilosc * cena_zakupu_waluta * kurs_zakupu) + prowizja_zakupu

st.subheader(f"Analiza dla: {nazwa}")
c1, c2, c3 = st.columns(3)
c1.metric("Koszt zakupu (PLN)", f"{koszt_calkowity_pln:,.2f} PLN")
c2.metric("Kurs rynkowy", f"{bazowy_kurs_sprzedazy:.4f}")
c3.metric("Kurs po marży banku (-1%)", f"{efektywny_kurs_sprzedazy:.4f}", delta="-1%")

# Generowanie skali zysku 1-10%
wyniki = []
for procent in range(1, 11):
    wzrost = 1 + (procent / 100)
    przyszla_cena_waluta = cena_zakupu_waluta * wzrost
    
    # Wartość sprzedaży z uwzględnieniem marży banku na kursie
    wartosc_sprzedazy_pln = (ilosc * przyszla_cena_waluta * efektywny_kurs_sprzedazy) - prowizja_sprzedazy
    zysk_netto = wartosc_sprzedazy_pln - koszt_calkowity_pln
    marza_procentowa = (zysk_netto / koszt_calkowity_pln) * 100
    
    wyniki.append({
        "Wzrost ceny akcji": f"+{procent}%",
        "Cena akcji (waluta)": f"{przyszla_cena_waluta:.2f}",
        "Wartość w PLN (po marży)": f"{wartosc_sprzedazy_pln:,.2f}",
        "Zysk netto (PLN)": f"{zysk_netto:,.2f}",
        "Realna marża całościowa": f"{marza_procentowa:.2f}%"
    })

df_wyniki = pd.DataFrame(wyniki)
st.table(df_wyniki)
