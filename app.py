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

# Input untuk memilih drama Korea
st.subheader("Pilih Drama Korea")
selected_drama = st.selectbox(
    "Pilih Drama:",
    options=df['Name'].unique()
)

# Menampilkan detail drama yang dipilih
drama_detail = df[df['Name'] == selected_drama].iloc[0]
st.write(f"**Nama Drama:** {drama_detail['Name']}")
st.write(f"**Rating:** {drama_detail['Rating']}")
st.write(f"**Genre:** {drama_detail['Genre']}")
st.write(f"**Jumlah Episode:** {drama_detail['Number of Episodes']}")
st.write(f"**Durasi:** {drama_detail['Duration']}")
st.write(f"**Sinopsis:** {drama_detail['Synopsis']}")

# Rekomendasi drama berdasarkan genre yang sama
st.subheader("Rekomendasi Drama Korea")
recommended_drama = df[df['Genre'] == drama_detail['Genre']].sort_values(by='Rating', ascending=False).head(5)

st.write(f"Rekomendasi drama dengan genre {drama_detail['Genre']}:")
st.dataframe(recommended_drama[['Name', 'Rating', 'Number of Episodes', 'Genre']])

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
