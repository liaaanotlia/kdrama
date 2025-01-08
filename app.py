from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd

# Menyiapkan data (contoh)
df = pd.read_csv("korean_dramas_preprocessed.csv")

# Menggunakan MultiLabelBinarizer untuk genre
mlb = MultiLabelBinarizer()
genre_encoded = mlb.fit_transform(df['Genre'])
genre_df = pd.DataFrame(genre_encoded, columns=mlb.classes_)

# Menggunakan One-Hot Encoding untuk cast
cast_encoded = df['Cast'].str.get_dummies(sep=', ')
cast_df = cast_encoded

# Gabungkan kedua fitur
features = pd.concat([genre_df, cast_df], axis=1)

# Terapkan KNN
knn = NearestNeighbors(n_neighbors=5, metric='cosine')
knn.fit(features)

# Pilih drama yang dipilih pengguna
selected_drama_index = df[df['Name'] == selected_drama].index[0]
selected_drama_features = features.iloc[selected_drama_index].values.reshape(1, -1)

# Temukan 5 tetangga terdekat
distances, indices = knn.kneighbors(selected_drama_features)

# Tampilkan hasil rekomendasi
recommended_dramas = df.iloc[indices[0]]
st.write("Recommended Dramas based on KNN:")
st.dataframe(recommended_dramas[['Name', 'Rating', 'Number of Episodes', 'Genre', 'Cast']])
