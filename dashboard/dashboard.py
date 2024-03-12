import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# mengatur judul halaman web 
st.set_page_config(page_title="Bike Sharing")

# memuat dataset
day_df = pd.read_csv("https://raw.githubusercontent.com/maersyifaaa/Proyek-Analisis-Data/main/dataset/cleaned_day.csv")

# memuat dataframe
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
day_df.set_index(["dteday"], inplace=True)

# membuat judul sebagai header halaman
st.title('Bike Sharing Dashboard :sparkles:')

# menambahkan informasi jumlah peminjam sepeda 
col1, col2, col3 = st.columns(3)

with col1:
    registered_users = day_df['registered'].sum()
    st.metric("Registered Users", value=registered_users)
with col2:
    casual_users = day_df['casual'].sum()
    st.metric("Casual Users", value=casual_users)
with col3:
    total_rental_bikes = day_df['cnt'].sum()
    st.metric("Total Rental Bikes", value=total_rental_bikes)

st.markdown("---")

# --- Bike Sharing Count by Month ---
# Membuat judul sebagai header halaman
st.subheader("Bike Sharing - Count by Month")

# Membuat DataFrame bulanan 'month_df'
def create_month_df(day_df):
    month_df = day_df.groupby(pd.Grouper(freq="M")).agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    month_df.index = month_df.index.strftime("%b-%Y")
    month_df = month_df.reset_index()
    month_df = month_df.rename(columns={
        "dteday": "monthyr",
        "casual": "casual users",
        "registered": "registered users",
        "cnt": "total rental bikes"
    })
    return month_df

# Membuat DataFrame bulan
month_df = create_month_df(pd.DataFrame(day_df))

# Membuat slider tahun
year = st.slider("Tentukan Tahun", 2011, 2012, step=1)

# Memotong DataFrame untuk hanya menggunakan tahun yang dipilih
df_selected_year = month_df[month_df['monthyr'].str.endswith(str(year))]

# Membuat histogram
fig, ax = plt.subplots(figsize=(15, 6))
ax.plot(
    df_selected_year["monthyr"],
    df_selected_year["total rental bikes"],
    marker='o', 
    linewidth=2,
    color='skyblue'
)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)

# Mengatur label sumbu x dan y
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Total Users', fontsize=12)

# Mengatur format tanggal di sumbu x
plt.xticks(rotation=0)

# Menampilkan plot
st.pyplot(fig)


# --- Bike Sharing Count by Season ---
# membuat judul sebagai header halaman
st.subheader("Bike Sharing - Count by Season")

# membuat DataFrame bulanan 'season_df'
def create_season_df(day_df):
    season_df = day_df.groupby('season').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    season_df = season_df.reset_index()
    season_df = season_df.rename(columns={
        "casual": "casual users",
        "registered": "registered users",
        "cnt": "total rental bikes"
    })
    return season_df

# membuat DataFrame musim
season_df = create_season_df(pd.DataFrame(day_df))

# Membuat daftar warna yang berbeda untuk setiap bar
colors = ['#d26025', '#ee6f68', '#ffbe4f', '#8aafff']

# Membuat histogram
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(season_df['season'], 
       season_df['total rental bikes'],
       color=colors)

ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)

# Mengatur label sumbu x dan y
ax.set_xlabel('Season', fontsize=12)
ax.set_ylabel('Total Users', fontsize=12)

# Mengatur format tanggal di sumbu x
plt.xticks(rotation=0)

# Menampilkan plot
st.pyplot(fig)

# Membuat caption
st.caption('Copyright (c), created by Maersyifaa Macira Balqis A. G')