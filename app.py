import streamlit as st
from data import *

def judul():
    #judul dashboard
    st.title('📊 DASHBOARD COVID-19')
    st.write('Selamat Datang di Dashboard Interaktif Untuk Menganalisis Data COVID-19 Di Indonesia!!!')

st.sidebar.title('Navigation')
menu = st.sidebar.radio("Pilih Halaman",['Home', 'Halaman Data'])


if menu == "Home":
    judul()
   
    #filter
    df= load_data()
    year= select_year()
    location = select_location(df)
    df_filtered = filter_data(df, year, location)
    #kolom1
    kolom1(df_filtered)
    #pie chart
    pie_chart1(df_filtered)
    bar_chart1(df_filtered)
    bar_chart2(df_filtered)
    map_chart(df_filtered)
elif menu == "Halaman Data":
    judul()
    #filter
    df= load_data()
    year= select_year()
    location = select_location(df)
    df_filtered = filter_data(df, year, location)
    show_data(df_filtered)


st.write('---')
st.write('©DASHBOARD_2025 | Ayu Andani - 184230040')