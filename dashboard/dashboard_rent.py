import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def create_month_yearly(df):
    data_monthly = df.resample('M', on='dteday').agg({
        'cnt': 'sum', 
})
    data_monthly = data_monthly.reset_index()
    data_monthly.rename(columns={
        "cnt": "Jumlah"
    }, inplace= True)
    return data_monthly

def create_season(df):
    season_data = df.groupby(by="season")["cnt"].sum().reset_index()
    nama_musim = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
    season_data["season"] = season_data["season"].replace(nama_musim)
    return season_data

def create_working_day(df):
    data_mean_workingday = df.groupby(by="workingday")["cnt"].mean().reset_index()
    workingday_rename = {1: "Hari Kerja", 0: "Hari Libur"}
    data_mean_workingday["workingday"] = data_mean_workingday["workingday"].replace(workingday_rename)
    return data_mean_workingday

def create_tren(df):
    data_yearly = df.resample('Y', on='dteday').agg({
        'cnt': 'sum',
})
    data_yearly = data_yearly.reset_index()
    data_yearly.rename(columns={
        "cnt": "Jumlah"
    }, inplace=True)
    return data_yearly

def bin_wind(windspeed):
    if windspeed < 0.1:
        return "Angin Pelan"
    elif windspeed < 0.3:
        return "Angin Sedang"
    else:
        return "Angin Kencang"

def create_year(df, year):
    data_2012 = df[df["dteday"].dt.year == year]
    data_2012["Wind Category"] = data_2012["windspeed"].apply(bin_wind)
    data_2012 = data_2012.groupby(by="Wind Category")["cnt"].mean().reset_index()
    return data_2012

def create_weekday(df, year):
    data_weekday_2011 = df[df["dteday"].dt.year == year]
    data_weekday_2011 = data_weekday_2011.groupby(by="weekday")["cnt"].sum().reset_index()
    data_weekday_2011["weekday"] = data_weekday_2011["weekday"].replace(nama_hari)
    return data_weekday_2011

def nlargest(df):
    largest = df.nlargest(3, "cnt").values
    return largest

def colors(df, top_value):
    color = ["orange" if i in top_value else "gray" for i in df["cnt"]]
    return color

nama_hari = {
    0 : "Minggu",
    1 : "Senin",
    2 : "Selasa",
    3 : "Rabu",
    4 : "Kamis",
    5 : "Jum'at",
    6 : "Sabtu"
}

all_df = pd.read_csv('day.csv')

datetime_columns = ["dteday"]
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])


min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("5320247.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

#Declaration Variabel to Visualization
data_month_yearly = create_month_yearly(main_df)
data_season = create_season(main_df)
data_working_day = create_working_day(main_df)
data_tren = create_tren(main_df)
data_2011 = create_year(main_df, 2011)
data_2012 = create_year(main_df, 2012)
data_weekday_2011 = create_weekday(main_df, 2011)
data_weekday_2012 = create_weekday(main_df, 2012)
nlargest_data2011 = nlargest(data_weekday_2011)
nlargest_data2012 = nlargest(data_weekday_2012)
colors_2011 = colors(data_weekday_2011, nlargest_data2011)
colors_2012 = colors(data_weekday_2012, nlargest_data2012)

st.header('Visualization Collection Dashboard :sparkles:')

st.subheader("Data Trend")

with st.expander("Trend Sepeda Pada Tahun 2011-2012"):
    total_orders = data_month_yearly["Jumlah"].sum()
    highest_rent_date = data_month_yearly.groupby("dteday")["Jumlah"].sum().idxmax()

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
    data_month_yearly["dteday"],
    data_month_yearly["Jumlah"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
 
    st.pyplot(fig)
    st.write(f"Jumlah Perental Sepeda Pada 2011-2012 Sebanyak: {total_orders}.")
    st.write(f"Titik Tertinggi Perentalan Sepeda Terjadi Pada: {highest_rent_date}")


with st.expander("Jumlah Perentalan Sepeda Berdasarkan Musimnya"):
   fig, ax = plt.subplots(figsize=(16,8))
   max_value = data_season["cnt"].max()
   colors = ["#72BCD4" if cnt < max_value else "#D47272" for cnt in data_season["cnt"]]

   sns.barplot(data=data_season, x="season", y="cnt", palette=colors)
   ax.ticklabel_format(style='plain', axis='y')
   ax.set_title("Jumlah Perentalan Sepeda Berdasarkan Musim", fontsize=15)
   ax.tick_params(axis="x", labelsize=12)
   ax.set_ylabel("Jumlah")
   ax.set_xlabel(" ")

   st.pyplot(fig)
   st.markdown(
    f"""
    <div style="text-align: center;">
        Winter Season: {data_season.loc[data_season['season'] == "Winter", "cnt"].values[0]} <br>
        Spring Season: {data_season.loc[data_season['season'] == "Spring", "cnt"].values[0]} <br>
        <b>Summer Season: {data_season.loc[data_season['season'] == "Summer", "cnt"].values[0]}</b> <br>
        Fall Season  : {data_season.loc[data_season['season'] == "Fall", "cnt"].values[0]} <br>
        Dari Data Tersebut Dapat Disimpulkan Bahwa Perentalan Terbanyak Terjadi Paling Banyak Pada Season Summer Disusul Spring, Fall dan Terakhir Winter
    </div>
    """,
    unsafe_allow_html=True)

with st.expander("Jumlah Rata-Rata Perentalan Sepeda Berdasarkan Hari Kerja vs Akhir Pekan"):
    fig, ax = plt.subplots(figsize=(16,8))
    max_value = data_working_day["cnt"].max()
    colors = ["#72BCD4" if cnt < max_value else "#D47272" for cnt in data_working_day["cnt"]]

    sns.barplot(data=data_working_day, x="workingday", y="cnt", palette=colors)
    ax.set_title("Jumlah Rata-Rata Perentalan Sepeda Berdasarkan Hari Kerja vs Akhir Pekan")
    ax.tick_params(axis="x", labelsize=12)
    ax.set_xlabel("Hari Kerja vs Akhir Pekan")
    ax.set_ylabel(" ")
    st.pyplot(fig)
    st.write(
        f"""Rata-Rata Perentalan Sepeda Pada Hari Kerja dan Hari Libur
        \nHari Kerja: {int(data_working_day.loc[data_working_day["workingday"] == "Hari Libur", "cnt"].values[0])} \n
        \n**Hari Libur: {int(data_working_day.loc[data_working_day["workingday"] == "Hari Kerja", "cnt"].values[0])}**""")

tren_tahun = ((data_tren["Jumlah"][1] - data_tren["Jumlah"][0]) / data_tren["Jumlah"][0]) * 100
with st.expander("Jumlah Kenaikan Tren Sepeda Pada Tahun 2011-2012"):
    fig, ax = plt.subplots(figsize=(16,8))
    max_value = data_tren["Jumlah"].max()
    colors = ["#72BCD4" if cnt < max_value else "#D47272" for cnt in data_tren["Jumlah"]]

    sns.barplot(data=data_tren, x="dteday", y="Jumlah", palette=colors)
    ax.text(1, data_tren["Jumlah"][1] + 50000, f"⬆ {round(tren_tahun,1)}%", ha='center', fontsize=12, color='orange', fontweight='bold')
    ax.set_title("Jumlah Kenaikan Tren Rental Sepeda Pada Tahun 2011-2012")
    ax.tick_params(axis="x", labelsize=12)
    ax.set_xlabel("Tren Rental Sepeda 2011-2012")
    ax.set_ylabel(" ")
    st.pyplot(fig)
    st.write(f"Jumlah Kenaikan Tren Bersepeda Dari 2011-2012 Sebanyak: **{int(tren_tahun)}%**")

with st.expander("Persentase Rental Sepeda Berdasarkan Kategori Kecepatan Angin Pada Data 2011-2012"):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    axes[0].pie(
    x=data_2011["cnt"], 
    labels=data_2011["Wind Category"], 
    autopct='%.2f%%'
    )
    axes[0].set_title("Tahun 2011")

    axes[1].pie(
    x=data_2012["cnt"], 
    labels=data_2012["Wind Category"], 
    autopct='%.2f%%'
    )
    axes[1].set_title("Tahun 2012")

    fig.suptitle("Perbandingan Persentase Rental Sepeda Berdasarkan Kategori Kecepatan Angin")
    plt.subplots_adjust(top=0.5)  
    plt.tight_layout()
    st.pyplot(fig)
    col1, col2 = st.columns(2)

    with col1:
        st.write("<p style='text-align: center;'><b>Angin Pelan: 38,50%</b></p>", unsafe_allow_html=True)
        st.write("<p style='text-align: center;'>Angin Sedang: 35,10%</p>", unsafe_allow_html=True)
        st.write("<p style='text-align: center;'>Angin Kencang: 26,40%</p>", unsafe_allow_html=True)
    
    with col2:
        st.write("<p style='text-align: center;'><b>Angin Pelan: 38,50%</b></p>", unsafe_allow_html=True)
        st.write("<p style='text-align: center;'>Angin Sedang: 35,10%</p>", unsafe_allow_html=True)
        st.write("<p style='text-align: center;'>Angin Kencang: 26,40%</p>", unsafe_allow_html=True)


with st.expander("Jumlah Perental Berdasarkan Hari Senin-Minggu"):
    fig, axes = plt.subplots(1, 2, figsize=(10,4))

    sns.barplot(data=data_weekday_2011, x="cnt", y="weekday", ax=axes[0], palette=colors_2011)
    axes[0].set_title("Tahun 2011")
    axes[0].set_xlabel(" ")
    axes[0].set_ylabel(" ")

    sns.barplot(data=data_weekday_2012, x="cnt", y="weekday", ax=axes[1], palette=colors_2012)
    axes[1].set_title("Tahun 2012")
    axes[1].set_xlabel(" ")
    axes[1].set_ylabel(" ")

    fig.suptitle("Perbandingan Kepadatan Hari Pada 2011 dan 2012")
    st.pyplot(fig)

    col1, col2 = st.columns(2)

    with col1:
        st.write("<p style='text-align: center;'>Dari Gambar Tersebut Dapat Disimpulkan Bahwa Hari <b>Senin, Selasa, Jumat</b> Dengan Jumlah Perental Terbanyak Pada Tahun 2011</p>", unsafe_allow_html=True)

    with col2:
        st.write("<p style='text-align: center;'>Dari Gambar Tersebut Dapat Disimpulkan Bahwa Hari <b>Rabu, Kamis, Jumat</b> Dengan Jumlah Perental Terbanyak Pada Tahun 2011</p>", unsafe_allow_html=True)
