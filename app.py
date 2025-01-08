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

# Pilih drama Korea
selected_drama = st.selectbox(
    "Pilih Drama Korea:",
    options=df['Name'].values
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
st.subheader("Rekomendasi Drama Korea:")
recommended_drama = df[df['Genre'].apply(lambda genres: any(genre in drama_detail['Genre'] for genre in genres))].sort_values(by='Rating', ascending=False).head(5)

st.write(f"Rekomendasi drama dengan genre {', '.join(drama_detail['Genre'])}:")
st.dataframe(recommended_drama[['Name', 'Rating', 'Number of Episodes', 'Genre']])

# Footer
st.markdown("**Dibuat menggunakan Streamlit** © 2025")
