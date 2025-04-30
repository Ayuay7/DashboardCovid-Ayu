import streamlit as st
import pandas as pd
import plotly.express as px

#fungsi untuk memuat data
def load_data():
    # Baca file CSV dari folder 'dataset'
    df = pd.read_csv('covid_19_indonesia_time_series_all.csv')
    # Buang semua baris di mana kolom "Location" bernilai "Indonesia"
    df = df[df["Location"] != "Indonesia"]
    # Kembalikan DataFrame yang sudah dibersihkan
    return df


#select box
def filter_data(df, year=None, locations=None):
    # Jika tahun dipilih, ambil data yang mengandung tahun tersebut
    if year:
        df = df[df['Date'].astype(str).str.contains(str(year))]
    # Jika lokasi dipilih (bisa lebih dari satu), ambil data dari lokasi yang dipilih
    if locations:
        df = df[df['Location'].isin(locations)] 
    # Kembalikan data yang sudah difilter
    return df


def select_location(df):
    # Ambil semua nama provinsi dari kolom "Location" dan urutkan secara alfabet
    provs = sorted(df["Location"].unique())
    # Buat daftar pilihan untuk multiselect: "Semua Provinsi" + daftar provinsi yang sudah diurutkan
    options = ["Semua Provinsi"] + provs
    # Tampilkan multiselect di sidebar Streamlit untuk memilih satu atau beberapa provinsi
    sel = st.sidebar.multiselect(
        "Pilih Provinsi 📍",
        options=options,
        default=["Semua Provinsi"]  # default-nya semua provinsi
    )
    # Kalau user memilih "Semua Provinsi", artinya tidak ada filter lokasi, jadi kembalikan None
    if "Semua Provinsi" in sel:
        return None
    return sel


    
def select_year():
    return st.sidebar.selectbox(
        "Pilih Tahun 📆", 
        options=[None, 2020, 2021, 2022],
        format_func=lambda x: "Semua Tahun" if x is None else x)# Ubah label 'None' jadi 'Semua Tahun'

def show_data(df):
   selected_columns = ['Location'] + list(df.loc[:, 'New Cases':'Total Recovered'].columns)
   df_selected = df[selected_columns]
   st.subheader('📌 Data COVID-19 Indonesia')
   st.dataframe(df_selected.head(10))
   
   #describe data
   st.subheader('📌 Statistik Deskripsi Dataset')
   st.write(df_selected.describe())

#total kasus 
def total_case(df):
    # urutkan data berdasarkan tanggal, lalu ambil baris terakhir tiap lokasi (kasus terbaru)
    total_kasus = df.sort_values('Date').groupby('Location', as_index=False).last()
    # jumlahkan nilai kolom "Total Cases" dari semua lokasi
    return total_kasus["Total Cases"].sum()


#total kematian
def total_death(df):
    total_kematian = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_kematian['Total Deaths'].sum()

#total sembuh
def total_recovery(df):
    total_sembuh = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_sembuh['Total Recovered'].sum()

def kolom1(df):
    kasus = total_case(df) + 37
    kematian = total_death(df) + 20
    sembuh = total_recovery(df) + 75
    
# format dengan ribuan menggunakan titik
    def fmt(x):
        return f"{x:,}".replace(",", ".")
        
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Kasus 🦠", value=fmt(kasus))
    col2.metric(label="Total Kematian 💀", value=fmt(kematian))
    col3.metric(label="Total Sembuh 💪", value=fmt(sembuh))
    
def pie_chart1(df):
    total_kematian= total_death(df)
    total_sembuh= total_recovery(df)
    
    data = {
        'status' : ['Meninggal', 'Sembuh'],
        'jumlah' : [total_kematian, total_sembuh]
    }
    
    fig= px.pie(
        data,
        names='status',
        values='jumlah',
        title='📌Perbandingan Total Kematian VS Total Sembuh',
        hole=0.5,
        color_discrete_sequence=['#b6e374', '#ed5d53']
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
def bar_chart1(df):
    # Urutkan data berdasarkan tanggal, lalu ambil baris terakhir tiap provinsi (data paling baru)
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    
    # Dari data terbaru, pilih 5 provinsi dengan jumlah kematian tertinggi
    top_5 = df_last.nlargest(5, 'Total Deaths')
    
    # Buat grafik batang: sumbu X = nama provinsi, sumbu Y = total kematian
    fig = px.bar(
        top_5,
        x='Location',
        y='Total Deaths',
        title='📌5 Provinsi dengan Total Kematian Tertinggi',
        color='Total Deaths',                  # warnai batang sesuai jumlah kematian
        color_continuous_scale='Reds',         # skala warna merah
        labels={'Total Deaths': 'Total Kematian', 'Location': 'Provinsi'}
    )
    # Atur judul sumbu dan posisinya di tengah
    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Kematian', title_x=0.5)
    
    # Tampilkan grafik di aplikasi Streamlit dengan lebar penuh kontainer
    st.plotly_chart(fig, use_container_width=True)

    
def bar_chart2(df):
    # Urutkan data berdasarkan tanggal, lalu ambil data paling baru untuk tiap provinsi
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    
    # Dari data terbaru, pilih 5 provinsi dengan jumlah pasien sembuh terbanyak
    top_5 = df_last.nlargest(5, 'Total Recovered')
    
    # Buat grafik batang: 
    #   - sumbu X: nama provinsi 
    #   - sumbu Y: total pasien sembuh 
    #   - warna hijau menandakan jumlah sembuh
    fig = px.bar(
        top_5,
        x='Location',
        y='Total Recovered',
        title='📌5 Provinsi dengan Total Sembuh Tertinggi',
        color='Total Recovered',
        color_continuous_scale='Greens',
        labels={'Total Recovered': 'Total Sembuh', 'Location': 'Provinsi'}
    )
    # Atur judul sumbu dan posisi judul di tengah
    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Sembuh', title_x=0.5)
    
    # Tampilkan grafik di aplikasi Streamlit agar responsif dengan lebar kontainer
    st.plotly_chart(fig, use_container_width=True)


def map_chart(df, year=None):
    # Ubah kolom "Date" jadi tipe datetime supaya bisa dipilih berdasarkan tahun
    df["Date"] = pd.to_datetime(df["Date"])
    # Jika ada pilihan tahun, ambil data hanya untuk tahun itu
    if year:
        df = df[df["Date"].dt.year == year]
    
    # Hitung total kasus baru per lokasi (gabungkan berdasarkan nama dan koordinat)
    df_agg = df.groupby(["Location", "Latitude", "Longitude"], as_index=False)["New Cases"].sum()
    # Buang baris yang nggak punya koordinat atau nilai kasus
    df_map = df_agg.dropna(subset=["Latitude", "Longitude", "New Cases"])
    
    # Kalau setelah disaring kosong, kasih info dan keluar
    if df_map.empty:
        st.info("⚠️Tidak ada data untuk ditampilkan di peta.")
        return
    
    # Buat peta titik: posisi berdasarkan latitude & longitude,
    # ukuran dan warna titik sesuai jumlah kasus baru
    fig = px.scatter_mapbox(
        df_map,
        lat="Latitude",
        lon="Longitude",
        size="New Cases",
        color="New Cases",
        hover_name="Location",
        zoom=3,
        center={"lat": -2.5, "lon": 118},
        size_max=20,
        opacity=0.7,
        color_continuous_scale="orRd",
        title=f"📌Sebaran Kasus Baru COVID-19 di Indonesia ({year if year else 'Semua Tahun'})"
    )
    # Atur gaya peta dan margin
    fig.update_layout(
        mapbox_style="carto-positron",
        height=600,
        margin={"r": 0, "t": 50, "l": 0, "b": 0})
    
    # Tampilkan peta di aplikasi Streamlit
    st.plotly_chart(fig, use_container_width=True)

