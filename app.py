import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

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

# Fungsi untuk menghitung cosine similarity antara dua list of strings
def cosine_sim(text1, text2):
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0, 1]

# Rekomendasi berdasarkan genre yang sama (menggunakan cosine similarity)
st.subheader("Recommended K-Dramas based on Genre:")
genre_similarities = []

for _, row in df.iterrows():
    genre_similarity = cosine_sim(' '.join(drama_detail['Genre']), ' '.join(row['Genre']))
    genre_similarities.append(genre_similarity)

df['Genre Similarity'] = genre_similarities
recommended_drama_by_genre = df.sort_values(by='Genre Similarity', ascending=False).head(5)
st.write(f"Recommendations based on genres: {', '.join(drama_detail['Genre'])}:")
st.dataframe(recommended_drama_by_genre[['Name', 'Rating', 'Number of Episodes', 'Genre']])

# Rekomendasi berdasarkan cast yang sama (menggunakan cosine similarity)
st.subheader("Recommended K-Dramas based on Cast:")
cast_similarities = []

for _, row in df.iterrows():
    cast_similarity = cosine_sim(drama_detail['Cast'], row['Cast'])
    cast_similarities.append(cast_similarity)

df['Cast Similarity'] = cast_similarities
recommended_drama_by_cast = df.sort_values(by='Cast Similarity', ascending=False).head(5)
st.write(f"Recommendations based on cast: {', '.join(drama_detail['Cast'].split(', '))}:")
st.dataframe(recommended_drama_by_cast[['Name', 'Rating', 'Number of Episodes', 'Cast']])

# Rekomendasi berdasarkan genre dan cast yang sama (menggunakan cosine similarity)
st.subheader("Recommended K-Dramas based on Genre and Cast:")

# Menghitung kesamaan berdasarkan genre dan cast dengan menggabungkan keduanya
combined_similarities = []

for _, row in df.iterrows():
    genre_similarity = cosine_sim(' '.join(drama_detail['Genre']), ' '.join(row['Genre']))
    cast_similarity = cosine_sim(drama_detail['Cast'], row['Cast'])
    combined_similarity = genre_similarity + cast_similarity  # Gabungkan genre dan cast similarity
    combined_similarities.append(combined_similarity)

df['Combined Similarity'] = combined_similarities
recommended_drama_by_genre_and_cast = df.sort_values(by='Combined Similarity', ascending=False).head(5)
st.write(f"Recommendations based on genres: {', '.join(drama_detail['Genre'])} and cast: {', '.join(drama_detail['Cast'].split(', '))}:")
st.dataframe(recommended_drama_by_genre_and_cast[['Name', 'Rating', 'Number of Episodes', 'Genre', 'Cast']])

# Footer
st.markdown("**Created with Streamlit** © 2025")
