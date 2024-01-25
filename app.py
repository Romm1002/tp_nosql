import streamlit as st
from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd 

client = MongoClient("mongodb://localhost:27017/")
db = client["spotify"]
collection_genres = db["artists.genres"]
collection_artists = db["artists"]

st.title("API Spotify")

selected_page = st.sidebar.radio("Sélectionnez une page", ["Artistes", "Genres", "Graphiques"])

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
       
elif selected_page == "Graphiques":
    
    # 
    # GRAPHIQUE DES ARTISTES LES PLUS POPULAIRES
    # 
    top_artists = pd.DataFrame(list(collection_artists.find({}, {"_id": 0, "name": 1, "popularity": 1, "genres": 1})))
    top_5_artists = top_artists.nlargest(5, 'popularity')
    st.subheader("Les 5 artistes les plus populaires")
    fig, ax = plt.subplots()
    top_5_artists.plot(kind='bar', x='name', y='popularity', ax=ax, rot=45)
    ax.set_xlabel("Artiste")
    ax.set_ylabel("Popularité")
    ax.set_title("Les 5 artistes les plus populaires")
    st.pyplot(fig)

    st.subheader("Genres des 5 artistes les plus populaires")
    for index, artist in top_5_artists.iterrows() :
        name = artist["name"]
        genres = ', '.join(artist["genres"])
        st.write(f"{name} - {genres}")

    # 
    # GRAPHIQUE DU NOMBRE D'ARTISTES PAR GENRES
    # 

    pipeline = [
        {
            "$unwind": "$genres"
        },
        {
            "$group": {
                "_id": "$genres",
                "artists_count": {"$sum": 1}
            }
        },
        {
            "$sort": {"artists_count": -1}
        },
        {
            "$limit": 5
        }
    ]

    genres_data = pd.DataFrame(list(collection_artists.aggregate(pipeline)))

    st.subheader("Nombre d'artistes par genre (Top 5)")
    fig, ax = plt.subplots()
    genres_data.plot(kind='bar', x='_id', y='artists_count', ax=ax, rot=45)
    ax.set_xlabel("Genre")
    ax.set_ylabel("Nombre d'artistes")
    ax.set_title("Nombre d'artistes par genre musical (Top 5)")
    st.pyplot(fig)

    # 
    # GRAPHIQUE REPARTITION DE LA POPULARTIE DES ARTISTES PAR GENRE
    #
    st.subheader("Répartition des artistes populaires entre les genres")

    genres_data = {genre["nom"]: genre["_id"] for genre in collection_genres.find()}
    genres = genres = list(genres_data.keys())

    selected_genre_name = st.selectbox("Sélectionnez un genre", genres)
    selected_genre_id = genres_data[selected_genre_name]
    if selected_genre_id:
        artists_popularity = pd.DataFrame(db['artists.artists_genres'].aggregate([
            {"$match": {"genre_id":  selected_genre_id}},
            {"$lookup": {"from": "artists", "localField": "artist_id", "foreignField": "_id", "as": "artist"}},
            {"$unwind": "$artist"},
            {"$group": {
                "_id": "$artist.popularity",
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": -1}}
        ]))

        count = artists_popularity["count"].sum()
        st.write(f"{count} artistes dans ce genre")

        
        fig, ax = plt.subplots()
        artists_popularity.sort_values(by='_id', ascending=True).plot(kind='bar', x='_id', y='count', ax=ax, rot=45)
        ax.set_xlabel("Popularité")
        ax.set_ylabel("Artistes")
        ax.set_title("Nombre d'artiste par popularité")
        st.pyplot(fig)




    st.write("---")
    # 
    # GRAPHIQUE REPARTITION DE LA POPULARTIE DES ARTISTES PAR GENRE
    #
    genres_data = {genre["nom"]: genre["_id"] for genre in collection_genres.find().limit(40)}
    genres = genres = list(genres_data.keys())

    selected_genre_name = st.selectbox("Sélectionnez un genre", genres)
    selected_genre_id = genres_data[selected_genre_name]
    if selected_genre_id:
        artists_document = db['artists.artists_genres'].aggregate([
            {"$match": {"genre_id":  selected_genre_id}},
            {"$lookup": {"from": "artists", "localField": "artist_id", "foreignField": "_id", "as": "artist"}},
            {"$unwind": "$artist"},
            {"$sort": {"artist.popularity": -1}}
        ])

        data = [{"_id": doc['artist']['_id'], "popularity": doc['artist']['popularity']} for doc in artists_document]
        st.write(f"{len(data)} artistes dans ce genre")


else:
    st.write("Sélectionnez une page dans la barre latérale.")
