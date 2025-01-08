import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("korean_dramas_preprocessed.csv")
    
    # Menghapus spasi di sekitar nama kolom
    df.columns = df.columns.str.strip()  # Hapus spasi yang tidak terlihat
    df['Genre'] = df['Genre'].apply(lambda x: x.split())  # Memisahkan genre berdasarkan spasi
    return df

# Judul Aplikasi
st.title("K-Drama Recommendation")
st.markdown("Korean drama recommendation for you")

# Load dataset
df = load_data()

# Membuat dropdown untuk memilih drama Korea
selected_drama = st.selectbox(
    "Select a Korean Drama:",
    options=df['Name'].values
)

# Menampilkan detail drama yang dipilih
drama_detail = df[df['Name'] == selected_drama].iloc[0]

st.write(f"**Name:** {drama_detail['Name']}")
st.write(f"**Year of Release:** {drama_detail['Year of release'] if 'Year of release' in drama_detail else 'Data not available'}")
st.write(f"**Number of Episodes:** {drama_detail['Number of Episodes'] if 'Number of Episodes' in drama_detail else 'Data not available'}")
st.write(f"**Duration:** {drama_detail['Duration'] if 'Duration' in drama_detail else 'Data not available'}")
st.write(f"**Content Rating:** {drama_detail['Content Rating'] if 'Content Rating' in drama_detail else 'Data not available'}")
st.write(f"**Rating:** {drama_detail['Rating'] if 'Rating' in drama_detail else 'Data not available'}")
st.write(f"**Synopsis:** {drama_detail['Synopsis'] if 'Synopsis' in drama_detail else 'Data not available'}")
st.write(f"**Genre:** {', '.join(drama_detail['Genre'])}")
st.write(f"**Cast:** {drama_detail['Cast'] if 'Cast' in drama_detail else 'Data not available'}")

# Menghitung fitur untuk KNN (genre dan cast)
def get_features(drama):
    # Menggunakan genre dan cast sebagai fitur numerik
    genre_features = [1 if genre in drama_detail['Genre'] else 0 for genre in df['Genre'].explode().unique()]
    cast_features = [1 if actor in drama_detail['Cast'].split(', ') else 0 for actor in df['Cast'].str.split(', ').explode().unique()]
    return np.array(genre_features + cast_features)

# Menyiapkan data fitur untuk KNN
all_drama_features = np.array([get_features(drama) for _, drama in df.iterrows()])

# Membangun model KNN
knn = NearestNeighbors(n_neighbors=6, metric='cosine')  # Menggunakan cosine similarity
knn.fit(all_drama_features)

# Mencari rekomendasi berdasarkan drama yang dipilih
drama_features = get_features(drama_detail)
distances, indices = knn.kneighbors([drama_features])

# Menampilkan rekomendasi
st.subheader("Recommended K-Dramas:")
recommended_indices = indices[0][1:]  # Menghindari diri sendiri (indeks 0)
recommended_drama = df.iloc[recommended_indices]

st.write("Here are the top 5 recommendations based on your selected drama:")
st.dataframe(recommended_drama[['Name', 'Rating', 'Number of Episodes', 'Genre', 'Cast']])

# Footer
st.markdown("**Created with Streamlit** © 2025")
