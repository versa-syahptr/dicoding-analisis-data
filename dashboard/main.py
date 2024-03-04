import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# standar waktu
WAKTU = {
    "Dini Hari": range(0, 5), # 00:00 - 04:59
    "Pagi": range(5, 11),     # 05:00 - 10:59
    "Siang": range(11, 15),   # 11:00 - 14:59
    "Sore": range(15, 19),    # 15:00 - 18:59
    "Malam": range(19, 24)    # 19:00 - 23:59
}
CUACA = ['Cerah', 'Mendung', 'Hujan Ringan', 'Hujan Deras']

def create_by_hour(df: pd.DataFrame):
    mean_hourly = df.groupby(by="hr")["cnt"].mean()
    mean_hourly.rename_axis('Jam', inplace=True)
    mean_hourly.rename('Rata-rata Peminjaman', inplace=True)
    return mean_hourly

def create_by_weather(df: pd.DataFrame):
    weather = df.groupby(by="weathersit")["cnt"].mean()
    # memastikan semua cuaca ada
    if len(weather) < 4:
        for i in range(1, 5):
            if i not in weather.index:
                weather[i] = 0
    return weather

def create_time_plot(hourly: pd.DataFrame):
    fig, ax = plt.subplots()
    total_per_waktu = {}
    for waktu, jam in WAKTU.items():
        total_per_waktu[waktu] = hourly[jam].sum()
    ax.pie(total_per_waktu.values(), labels=total_per_waktu.keys(), autopct='%1.1f%%', )
    return fig

def create_weather_plot(df: pd.DataFrame):
    fig, ax = plt.subplots()
    # total_per_cuaca = df.groupby(by="weathersit")["cnt"].sum()
    ax.pie(df, labels=CUACA, autopct='%1.1f%%')
    return fig

hour_df = pd.read_csv("hour_clean.csv")
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

day_df = pd.read_csv("day_clean.csv")
day_df["dteday"] = pd.to_datetime(day_df["dteday"])

mean_hourly = create_by_hour(hour_df)

st.title("Proyek Analisis Dataset Bike Sharing")

with st.sidebar:
    st.title("Data Diri")
    st.text("Nama : Versa Syahputra Santo")
    st.text("Dicoding Username: versa-syahptr")



st.subheader("Rata-rata Peminjaman Sepeda per Jam")
st.bar_chart(mean_hourly, use_container_width=True, )

st.subheader("Rata-rata Peminjaman Sepeda per Waktu")
fig = create_time_plot(mean_hourly)
st.pyplot(fig)

# markdown 
"**Standar pembagian waktu:**"
"""- Dini hari &nbsp;:   `00.00 - 04.59`
- Pagi &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : `05.00 - 10.59`
- Siang &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: `11.00 - 14.59`
- Sore &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: `15.00 - 18.59`
- Malam &nbsp;&nbsp;&nbsp;&nbsp;: `19.00 - 23.59`"""

st.subheader('Rata-rata Peminjaman Sepeda per Jam Pada Berbagai Cuaca')
weather_hour = create_by_weather(hour_df)
fig = create_weather_plot(weather_hour)
st.pyplot(fig)

st.subheader("Rata-rata Peminjaman Sepeda per Hari pada Berbagai Cuaca")
weather_day = create_by_weather(day_df)
fig = create_weather_plot(weather_day)
st.pyplot(fig)


