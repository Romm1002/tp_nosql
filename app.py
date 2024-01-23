# Importez les bibliothèques nécessaires
import streamlit as st
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["spotify"]
collection_genres = db["artists.genres"]
collection_artists = db["artists"]

# Titre de l'application
st.title("Application Spotify avec Streamlit")

# Choix de la page (Artiste ou Genre)
selected_page = st.sidebar.radio("Sélectionnez une page", ["Artistes", "Genres"])

if selected_page == "Artistes":
     # Page des Artistes
    # Paramètres de pagination pour les artistes
    page_size_artists = 10
    page_number_artists = st.sidebar.number_input("Numéro de la page des artistes", min_value=1, value=1)

    # Calcul de l'index de départ pour les artistes
    start_index_artists = (page_number_artists - 1) * page_size_artists

    # Récupérer les artistes avec pagination
    artists = collection_artists.find({}).skip(start_index_artists).limit(page_size_artists)

    # Afficher les résultats des artistes dans la page principale avec 3 artistes par ligne
    st.subheader("Artistes")
    artist_count = 0

    columns = st.columns(3)

    for artist in artists:
        with columns[artist_count % 3]:
            st.header(artist["name"])
            
            # Affiche l'image associée à l'artiste
            if "images" in artist and len(artist["images"]) > 0:
                first_image = artist["images"][0]
                st.image(first_image["url"], caption="Image 1", use_column_width=True)

            st.write(f"Popularité: {artist['popularity']}")
            st.write(f"Genres: {', '.join(artist['genres'])}")

            st.write("---")

        artist_count += 1

    # Afficher la pagination en bas de la page des artistes
    st.write("---")
    st.write("Page suivante des artistes")

else:
    # Page des Genres
    # Paramètres de pagination pour les genres
    page_size_genres = 10
    page_number_genres = st.sidebar.number_input("Numéro de la page des genres", min_value=1, value=1)

    # Calcul de l'index de départ pour les genres
    start_index_genres = (page_number_genres - 1) * page_size_genres

    # Récupérer les genres avec pagination
    genres = collection_genres.find({}).skip(start_index_genres).limit(page_size_genres)

    # Afficher les résultats des genres dans la page principale
    st.subheader("Genres Musicaux")
    for genre in genres:
        st.header(genre["nom"])
        
        # Vous pouvez afficher d'autres détails spécifiques à vos genres ici

        st.write("---")

    # Afficher la pagination en bas de la page des genres
    st.write("---")
    st.write("Page suivante des genres")
