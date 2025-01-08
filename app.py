import streamlit as st
import pandas as pd

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("korean_dramas_preprocessed.csv")
    return df

# Judul Aplikasi
st.title("K-Drama Dashboard")
st.markdown("Dashboard ini menampilkan informasi dan statistik K-Drama berdasarkan dataset hasil preprocessing.")

# Load dataset
df = load_data()

# Sidebar untuk filter
st.sidebar.header("Filter Data")
selected_genre = st.sidebar.multiselect(
    "Pilih Genre:",
    options=df['Genre'].unique(),
    default=df['Genre'].unique()
)

selected_rating = st.sidebar.slider(
    "Rating Minimum:",
    min_value=float(df['Rating'].min()),
    max_value=float(df['Rating'].max()),
    value=(df['Rating'].min())
)

# Filter data berdasarkan input pengguna
filtered_data = df[
    (df['Genre'].isin(selected_genre)) & 
    (df['Rating'] >= selected_rating)
]

# Tampilkan dataset yang difilter
st.subheader("Dataset Filtered")
st.write(f"Jumlah drama yang sesuai filter: {len(filtered_data)}")
st.dataframe(filtered_data)

# Statistik Rating
st.subheader("Statistik Rating")
st.bar_chart(df['Rating'].value_counts().sort_index())

# Statistik Jumlah Episode
st.subheader("Statistik Jumlah Episode")
st.bar_chart(df['Number of Episodes'].value_counts().sort_index())

# Menampilkan detail data
st.subheader("Detail Data")
if st.checkbox("Tampilkan semua data K-Drama"):
    st.write(df)

# Footer
st.markdown("**Dibuat menggunakan Streamlit** © 2025")
