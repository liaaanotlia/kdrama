import streamlit as st
import pandas as pd

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("korean_dramas_preprocessed.csv")
    
    # Print column names to check for any mismatch
    st.write(df.columns)
    
    # Splitting genres separated by space
    df['Genre'] = df['Genre'].apply(lambda x: x.split())  # Splitting genres based on space
    return df

# App Title
st.title("K-Drama Recommendation")
st.markdown("Korean drama recommendations for you")

# Load dataset
df = load_data()

# Check if the columns exist
required_columns = ['Name', 'Aired Date', 'Year of release', 'Original Network', 'Aired On', 
                    'Number of Episodes', 'Duration', 'Content Rating', 'Rating', 'Synopsis', 
                    'Genre', 'Tags', 'Director', 'Screenwriter', 'Cast', 'Production companies']

missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    st.error(f"Missing columns: {', '.join(missing_columns)}")
else:
    # Select a Korean Drama
    selected_drama = st.selectbox(
        "Select a Korean Drama:",
        options=df['Name'].values
    )

    # Display details of selected drama
    drama_detail = df[df['Name'] == selected_drama].iloc[0]

    # Handle potential missing values gracefully
    st.write(f"**Drama Name:** {drama_detail['Name']}")
    st.write(f"**Aired Date:** {drama_detail.get('Aired Date', 'N/A')}")
    st.write(f"**Year of Release:** {drama_detail.get('Year of release', 'N/A')}")
    st.write(f"**Original Network:** {drama_detail.get('Original Network', 'N/A')}")
    st.write(f"**Aired On:** {drama_detail.get('Aired On', 'N/A')}")
    st.write(f"**Number of Episodes:** {drama_detail.get('Number of Episodes', 'N/A')}")
    st.write(f"**Duration:** {drama_detail.get('Duration', 'N/A')}")
    st.write(f"**Content Rating:** {drama_detail.get('Content Rating', 'N/A')}")
    st.write(f"**Rating:** {drama_detail.get('Rating', 'N/A')}")
    st.write(f"**Synopsis:** {drama_detail.get('Synopsis', 'N/A')}")
    st.write(f"**Genre(s):** {', '.join(drama_detail['Genre'])}")
    st.write(f"**Tags:** {drama_detail.get('Tags', 'N/A')}")
    st.write(f"**Director:** {drama_detail.get('Director', 'N/A')}")
    st.write(f"**Screenwriter:** {drama_detail.get('Screenwriter', 'N/A')}")
    st.write(f"**Cast:** {drama_detail.get('Cast', 'N/A')}")
    st.write(f"**Production Companies:** {drama_detail.get('Production companies', 'N/A')}")

    # Recommend dramas based on similar genres
    st.subheader("Recommended Korean Dramas:")
    recommended_drama = df[df['Genre'].apply(lambda genres: any(genre in drama_detail['Genre'] for genre in genres))].sort_values(by='Rating', ascending=False).head(5)

    st.write(f"Recommended dramas with genre(s) {', '.join(drama_detail['Genre'])}:")
    st.dataframe(recommended_drama[['Name', 'Rating', 'Number of Episodes', 'Genre']])

# Footer
st.markdown("**Created using Streamlit** © 2025")
