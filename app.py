import streamlit as st
import pandas as pd

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
st.write(f"**Aired Date:** {drama_detail['Aired Date'] if 'Aired Date' in drama_detail else 'Data not available'}")
st.write(f"**Year of Release:** {drama_detail['Year of release'] if 'Year of release' in drama_detail else 'Data not available'}")
st.write(f"**Original Network:** {drama_detail['Original Network'] if 'Original Network' in drama_detail else 'Data not available'}")
st.write(f"**Aired On:** {drama_detail['Aired On'] if 'Aired On' in drama_detail else 'Data not available'}")
st.write(f"**Number of Episodes:** {drama_detail['Number of Episodes'] if 'Number of Episodes' in drama_detail else 'Data not available'}")
st.write(f"**Duration:** {drama_detail['Duration'] if 'Duration' in drama_detail else 'Data not available'}")
st.write(f"**Content Rating:** {drama_detail['Content Rating'] if 'Content Rating' in drama_detail else 'Data not available'}")
st.write(f"**Rating:** {drama_detail['Rating'] if 'Rating' in drama_detail else 'Data not available'}")
st.write(f"**Synopsis:** {drama_detail['Synopsis'] if 'Synopsis' in drama_detail else 'Data not available'}")
st.write(f"**Genre:** {', '.join(drama_detail['Genre'])}")
st.write(f"**Tags:** {drama_detail['Tags'] if 'Tags' in drama_detail else 'Data not available'}")
st.write(f"**Director:** {drama_detail['Director'] if 'Director' in drama_detail else 'Data not available'}")
st.write(f"**Screenwriter:** {drama_detail['Screenwriter'] if 'Screenwriter' in drama_detail else 'Data not available'}")
st.write(f"**Cast:** {drama_detail['Cast'] if 'Cast' in drama_detail else 'Data not available'}")
st.write(f"**Production Companies:** {drama_detail['Production companies'] if 'Production companies' in drama_detail else 'Data not available'}")

# Rekomendasi drama berdasarkan genre yang sama
st.subheader("Recommended K-Dramas:")
recommended_drama = df[df['Genre'].apply(lambda genres: any(genre in drama_detail['Genre'] for genre in genres))].sort_values(by='Rating', ascending=False).head(5)

st.write(f"Recommendations based on genres: {', '.join(drama_detail['Genre'])}:")
st.dataframe(recommended_drama[['Name', 'Rating', 'Number of Episodes', 'Genre']])

# Footer
st.markdown("**Created with Streamlit** © 2025")
