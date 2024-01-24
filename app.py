import streamlit as st
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["spotify"]
collection_genres = db["artists.genres"]
collection_artists = db["artists"]

st.title("Application Spotify avec Streamlit")

selected_page = st.sidebar.radio("Sélectionnez une page", ["Artistes", "Genres"])

if selected_page == "Artistes":
    page_size_artists = 12
    page_number_artists = st.sidebar.number_input("Numéro de la page des artistes", min_value=1, value=1)

    start_index_artists = (page_number_artists - 1) * page_size_artists

    artists = collection_artists.find({}).skip(start_index_artists).limit(page_size_artists)

    st.subheader("Artistes")
    artist_count = 0

    columns = st.columns(3)

    for artist in artists:
        with columns[artist_count % 3]:
            st.header(artist["name"])
            
            if "images" in artist and len(artist["images"]) > 0:
                first_image = artist["images"][0]
                st.image(first_image["url"], use_column_width=True)

            st.write(f"Popularité: {artist['popularity']}")
            st.write(f"Genres: {', '.join(artist['genres'])}")

            st.write("---")

        artist_count += 1

    st.write("---")

elif selected_page == "Genres":
    page_size_genres = 10
    page_number_genres = st.sidebar.number_input("Numéro de la page des genres", min_value=1, value=1)

    start_index_genres = (page_number_genres - 1) * page_size_genres

    genres = collection_genres.find({}).skip(start_index_genres).limit(page_size_genres)

    st.subheader("Genres Musicaux")
    for genre in genres:
        st.header(genre["nom"]) 
         
        top_artist_document = db['artists.artists_genres'].aggregate([
            {"$match": {"genre_id":  genre['_id']}},
            {"$lookup": {"from": "artists", "localField": "artist_id", "foreignField": "_id", "as": "artist"}},
            {"$unwind": "$artist"},
            {"$sort": {"artist.popularity": -1}},
            {"$limit": 1}
        ])
        artist = next(top_artist_document, None)
        st.write("Top artiste:", artist["artist"]["name"])
        st.write("Popularité de l'artiste:", artist["artist"]["popularity"])
        
        st.write("---")
