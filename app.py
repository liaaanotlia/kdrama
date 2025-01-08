import streamlit as st
import pandas as pd

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("korean_dramas_preprocessed.csv")
    
    # Memisahkan genre yang dipisahkan oleh spasi
    df['Genre'] = df['Genre'].apply(lambda x: x.split())  # Memisahkan genre berdasarkan spasi
    return df

# Judul Aplikasi
st.title("K-Drama Recommendation")
st.markdown("Korean drama recomendation for you")

# Load dataset
df = load_data()

# Sidebar untuk filter
st.sidebar.header("Filter Data")
selected_genre = st.sidebar.multiselect(
    "Pilih Genre:",
    options=[genre for genres in df['Genre'] for genre in genres],  # Flatten the list of genres
    default=[genre for genres in df['Genre'] for genre in genres]  # Default: semua genre
)

selected_rating = st.sidebar.slider(
    "Rating Minimum:",
    min_value=float(df['Rating'].min()),
    max_value=float(df['Rating'].max()),
    value=(df['Rating'].min())
)

# Filter data berdasarkan input pengguna
filtered_data = df[
    df['Genre'].apply(lambda genres: any(genre in selected_genre for genre in genres)) & 
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
st.write(f"**Genre:** {', '.join(drama_detail['Genre'])}")
st.write(f"**Jumlah Episode:** {drama_detail['Number of Episodes']}")
st.write(f"**Durasi:** {drama_detail['Duration']}")
st.write(f"**Sinopsis:** {drama_detail['Synopsis']}")

# Rekomendasi drama berdasarkan genre yang sama
st.subheader("Rekomendasi Drama Korea")
recommended_drama = df[df['Genre'].apply(lambda genres: any(genre in drama_detail['Genre'] for genre in genres))].sort_values(by='Rating', ascending=False).head(5)

st.write(f"Rekomendasi drama dengan genre {', '.join(drama_detail['Genre'])}:")
st.dataframe(recommended_drama[['Name', 'Rating', 'Number of Episodes', 'Genre']])

# Footer
st.markdown("**Dibuat menggunakan Streamlit** © 2025")
