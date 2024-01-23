# Importez les bibliothèques nécessaires
import streamlit as st
import pymongo
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["spotify"]
collection_albums = db["collection_albums"]
collection_categories = db["collection_categories"]

# Titre de l'application
st.title("Application Spotify avec Streamlit")

# Section pour récupérer les albums depuis l'API Spotify et les insérer dans la collection d'albums MongoDB
with st.sidebar:
    st.header("Paramètres pour les albums")
    # Ajoutez ici les éléments nécessaires pour récupérer les albums depuis l'API Spotify
    # Vous pouvez utiliser des widgets comme st.text_input, st.selectbox, etc.

# Section pour récupérer les catégories depuis l'API Spotify et les insérer dans la collection de catégories MongoDB
with st.sidebar:
    st.header("Paramètres pour les catégories")
    # Ajoutez ici les éléments nécessaires pour récupérer les catégories depuis l'API Spotify
    # Vous pouvez utiliser des widgets comme st.text_input, st.selectbox, etc.

# Affichez les résultats des albums dans la page principale
st.subheader("Résultats des albums")
# Exemple : Affichez tous les albums de la collection d'albums MongoDB
albums = collection_albums.find({})
for album in albums:
    st.write(album)

# Affichez les résultats des catégories dans la page principale
st.subheader("Résultats des catégories")
# Exemple : Affichez toutes les catégories de la collection de catégories MongoDB
categories = collection_categories.find({})
for category in categories:
    st.write(category)

# Section pour créer des graphes ou afficher d'autres informations
st.subheader("Graphes et informations supplémentaires")
# Ajoutez ici du code pour créer des graphes ou afficher des informations supplémentaires

# Exécutez l'application avec la commande streamlit run dans votre terminal
