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
st.markdown("Korean drama recommendation for you")

# Load dataset
df = load_data()

# Membuat selectbox untuk memilih drama Korea
selected_drama = st.selectbox(
    "Select a Korean Drama:",
    options=df['Name'].values
)

# Menampilkan detail drama yang dipilih
drama_detail = df[df['Name'] == selected_drama].iloc[0]

# Cek kolom dan tampilkan informasi jika kolom ada
st.write(f"**Name:** {drama_detail['Name']}")
st.write(f"**Aired Date:** {drama_detail['Aired Date']}" if 'Aired Date' in drama_detail else "**Aired Date:** Data not available")
st.write(f"**Year of Release:** {drama_detail['Year of Release']}" if 'Year of Release' in drama_detail else "**Year of Release:** Data not available")
st.write(f"**Original Network:** {drama_detail['Original Network']}" if 'Original Network' in drama_detail else "**Original Network:** Data not available")
st.write(f"**Aired On:** {drama_detail['Aired On']}" if 'Aired On' in drama_detail else "**Aired On:** Data not available")
st.write(f"**Number of Episodes:** {drama_detail['Number of Episodes']}" if 'Number of Episodes' in drama_detail else "**Number of Episodes:** Data not available")
st.write(f"**Duration:** {drama_detail['Duration']}" if 'Duration' in drama_detail else "**Duration:** Data not available")
st.write(f"**Content Rating:** {drama_detail['Content Rating']}" if 'Content Rating' in drama_detail else "**Content Rating:** Data not available")
st.write(f"**Rating:** {drama_detail['Rating']}" if 'Rating' in drama_detail else "**Rating:** Data not available")
st.write(f"**Synopsis:** {drama_detail['Synopsis']}" if 'Synopsis' in drama_detail else "**Synopsis:** Data not available")
st.write(f"**Genre:** {', '.join(drama_detail['Genre'])}" if 'Genre' in drama_detail else "**Genre:** Data not available")
st.write(f"**Tags:** {drama_detail['Tags']}" if 'Tags' in drama_detail else "**Tags:** Data not available")
st.write(f"**Director:** {drama_detail['Director']}" if 'Director' in drama_detail else "**Director:** Data not available")
st.write(f"**Screenwriter:** {drama_detail['Screenwriter']}" if 'Screenwriter' in drama_detail else "**Screenwriter:** Data not available")
st.write(f"**Cast:** {drama_detail['Cast']}" if 'Cast' in drama_detail else "**Cast:** Data not available")
st.write(f"**Production Companies:** {drama_detail['Production companies']}" if 'Production companies' in drama_detail else "**Production Companies:** Data not available")

# Rekomendasi drama berdasarkan genre yang sama
st.subheader("Recommended Korean Dramas:")
recommended_drama = df[df['Genre'].apply(lambda genres: any(genre in drama_detail['Genre'] for genre in genres))].sort_values(by='Rating', ascending=False).head(5)

st.write(f"Recommended dramas with genre {', '.join(drama_detail['Genre'])}:")
st.dataframe(recommended_drama[['Name', 'Rating', 'Number of Episodes', 'Genre']])

# Footer
st.markdown("**Made with Streamlit** © 2025")
