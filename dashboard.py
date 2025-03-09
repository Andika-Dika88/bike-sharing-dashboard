import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
day_df = pd.read_csv('main_data.csv')

# Mapping kondisi cuaca
weather_mapping = {
    1: 'Cerah/Berawan',
    2: 'Mendung',
    3: 'Hujan Ringan/Sedang',
    4: 'Hujan Lebat/Salju'
}

day_df['weathersit'] = day_df['weathersit'].map(weather_mapping)

# Streamlit app
st.title('Dashboard Analisis Penyewaan Sepeda 🚲')

# Sidebar untuk filter
st.sidebar.header('Filter Data')
day_type = st.sidebar.radio('Pilih Hari:', ['Semua', 'Hari Kerja', 'Akhir Pekan'])
weather_condition = st.sidebar.multiselect('Pilih Kondisi Cuaca:', options=day_df['weathersit'].dropna().unique())

# Filter data berdasarkan pilihan
if day_type == 'Hari Kerja':
    filtered_df = day_df[day_df['workingday'] == 1]
elif day_type == 'Akhir Pekan':
    filtered_df = day_df[day_df['workingday'] == 0]
else:
    filtered_df = day_df

if weather_condition:
    filtered_df = filtered_df[filtered_df['weathersit'].isin(weather_condition)]

# Simpan salinan dataframe untuk visualisasi cuaca
weather_df = filtered_df.copy()

# Visualisasi 1: Pola penyewaan casual vs registered
st.subheader('Pola Penyewaan Casual vs Registered')
filtered_df = filtered_df.melt(id_vars=['workingday', 'cnt'], value_vars=['casual', 'registered'], 
                                var_name='user_type', value_name='count')
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='workingday', y='count', hue='user_type', data=filtered_df, estimator='mean', errorbar='sd', ax=ax)
ax.set_xticklabels(['Akhir Pekan', 'Hari Kerja'])
ax.set_xlabel('Tipe Hari')
ax.set_ylabel('Jumlah Penyewaan Rata-rata')
ax.set_title('Penyewaan Casual vs Registered pada Hari Kerja & Akhir Pekan')
st.pyplot(fig)

# Visualisasi 2: Korelasi cuaca dan jumlah penyewaan
st.subheader('Korelasi Cuaca dan Jumlah Penyewaan')
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.boxplot(x='weathersit', y='cnt', data=weather_df, ax=ax2)
ax2.set_xlabel('Kondisi Cuaca')
ax2.set_ylabel('Jumlah Penyewaan')
ax2.set_title('Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
st.pyplot(fig2)

# Insight
st.subheader('Insight')
st.write(
    "Dari visualisasi di atas, terlihat bahwa pengguna registered lebih aktif menyewa sepeda di hari kerja, "
    "sedangkan pengguna casual lebih banyak menyewa di akhir pekan. Selain itu, kondisi cuaca juga berdampak "
    "signifikan pada jumlah penyewaan, di mana cuaca yang lebih baik cenderung meningkatkan penyewaan." 
)

st.write("Cobalah eksplorasi lebih jauh dengan mengubah filter di sidebar!")

# Jalankan dengan: streamlit run namafile.py

# 🚀 Siap dicoba? Atau ada yang mau disesuaikan lagi? 😉
