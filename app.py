import streamlit as st
import pandas as pd

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("korean_dramas_preprocessed.csv")
    
    # Splitting genres separated by space
    df['Genre'] = df['Genre'].apply(lambda x: x.split())  # Splitting genres based on space
    return df

# App Title
st.title("K-Drama Recommendation")
st.markdown("Korean drama recommendations for you")

# Load dataset
df = load_data()

# Select a Korean Drama
selected_drama = st.selectbox(
    "Select a Korean Drama:",
    options=df['Name'].values
)

# Display details of selected drama
drama_detail = df[df['Name'] == selected_drama].iloc[0]

st.write(f"**Drama Name:** {drama_detail['Name']}")
st.write(f"**Aired Date:** {drama_detail['Aired Date']}")
st.write(f"**Year of Release:** {drama_detail['Year of Release']}")
st.write(f"**Original Network:** {drama_detail['Original Network']}")
st.write(f"**Aired On:** {drama_detail['Aired On']}")
st.write(f"**Number of Episodes:** {drama_detail['Number of Episodes']}")
st.write(f"**Duration:** {drama_detail['Duration']}")
st.write(f"**Content Rating:** {drama_detail['Content Rating']}")
st.write(f"**Rating:** {drama_detail['Rating']}")
st.write(f"**Synopsis:** {drama_detail['Synopsis']}")
st.write(f"**Genre(s):** {', '.join(drama_detail['Genre'])}")
st.write(f"**Tags:** {drama_detail['Tags']}")
st.write(f"**Director:** {drama_detail['Director']}")
st.write(f"**Screenwriter:** {drama_detail['Screenwriter']}")
st.write(f"**Cast:** {drama_detail['Cast']}")
st.write(f"**Production Companies:** {drama_detail['Production companies']}")

# Recommend dramas based on similar genres
st.subheader("Recommended Korean Dramas:")
recommended_drama = df[df['Genre'].apply(lambda genres: any(genre in drama_detail['Genre'] for genre in genres))].sort_values(by='Rating', ascending=False).head(5)

st.write(f"Recommended dramas with genre(s) {', '.join(drama_detail['Genre'])}:")
st.dataframe(recommended_drama[['Name', 'Rating', 'Number of Episodes', 'Genre']])

# Footer
st.markdown("**Created using Streamlit** © 2025")
