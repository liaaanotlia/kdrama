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

# Styling untuk cast dan genre
st.markdown("""
    <style>
        .recommendation-container {
            display: flex;
            flex-wrap: wrap;
        }
        .recommendation-item {
            padding: 10px 20px;
            margin: 5px;
            background-color: #f0f0f5;
            border-radius: 15px;
            font-weight: bold;
        }
        .recommendation-item:hover {
            background-color: #dcdcfb;
        }
    </style>
""", unsafe_allow_html=True)

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
st.write(f"**Year of Release:** {drama_detail['Year of release']}")
st.write(f"**Number of Episodes:** {drama_detail['Number of Episodes']}")
st.write(f"**Duration:** {drama_detail['Duration']}")
st.write(f"**Content Rating:** {drama_detail['Content Rating']}")
st.write(f"**Rating:** {drama_detail['Rating']}")
st.write(f"**Synopsis:** {drama_detail['Synopsis']}")
st.write(f"**Genre:** {', '.join(drama_detail['Genre'])}")
st.write(f"**Cast:** {drama_detail['Cast']}")

# Rekomendasi drama berdasarkan genre yang sama
st.subheader("Recommended K-Dramas based on Genre:")
recommended_drama_by_genre = df[df['Genre'].apply(lambda genres: any(genre in drama_detail['Genre'] for genre in genres))].sort_values(by='Rating', ascending=False).head(5)

st.write(f"Recommendations based on genres: {', '.join(drama_detail['Genre'])}:")
st.dataframe(recommended_drama_by_genre[['Name', 'Rating', 'Number of Episodes', 'Genre']])

# Rekomendasi drama berdasarkan cast yang sama
st.subheader("Recommended K-Dramas based on Cast:")

# Menampilkan rekomendasi cast dalam bentuk yang lebih menarik
recommended_drama_by_cast = df[df['Cast'].apply(lambda cast: any(actor in drama_detail['Cast'] for actor in cast.split(', ')))].sort_values(by='Rating', ascending=False).head(5)

# Menampilkan rekomendasi dengan tampilan rounded
st.markdown(f'<div class="recommendation-container">', unsafe_allow_html=True)
for index, row in recommended_drama_by_cast.iterrows():
    st.markdown(f'<div class="recommendation-item">{row["Name"]} - Rating: {row["Rating"]}</div>', unsafe_allow_html=True)
st.markdown(f'</div>', unsafe_allow_html=True)

# Footer
st.markdown("**Created with Streamlit** © 2025")
