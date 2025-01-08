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

# Menghilangkan tampilan yang tidak perlu di bawah judul
st.write("")  # Membuat ruang kosong jika ada tampilan yang tidak diinginkan

# Membuat seleksi untuk memilih drama Korea
selected_drama = st.selectbox(
    "Select a Korean Drama:",
    options=df['Name'].values
)

# Menampilkan detail drama yang dipilih
drama_detail = df[df['Name'] == selected_drama].iloc[0]
st.write(f"**Name:** {drama_detail['Name']}")
st.write(f"**Aired Date:** {drama_detail['Aired Date']}")
st.write(f"**Year of Release:** {drama_detail['Year of Release']}")
st.write(f"**Original Network:** {drama_detail['Original Network']}")
st.write(f"**Aired On:** {drama_detail['Aired On']}")
st.write(f"**Number of Episodes:** {drama_detail['Number of Episodes']}")
st.write(f"**Duration:** {drama_detail['Duration']}")
st.write(f"**Content Rating:** {drama_detail['Content Rating']}")
st.write(f"**Rating:** {drama_detail['Rating']}")
st.write(f"**Synopsis:** {drama_detail['Synopsis']}")
st.write(f"**Genre:** {', '.join(drama_detail['Genre'])}")
st.write(f"**Tags:** {drama_detail['Tags']}")
st.write(f"**Director:** {drama_detail['Director']}")
st.write(f"**Screenwriter:** {drama_detail['Screenwriter']}")
st.write(f"**Cast:** {drama_detail['Cast']}")
st.write(f"**Production Companies:** {drama_detail['Production companies']}")

# Footer
st.markdown("**Created using Streamlit** © 2025")
