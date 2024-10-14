import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


st.set_page_config(layout="wide")


st.markdown("""
    <style>
    /* Change font globally */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
        background-color: #f0f2f6; /* light background color */
    }

    /* Fill page more and reduce margins */
    .css-18e3th9 {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* Center and enlarge headers */
    .css-1q8dd3e {
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
    }

    /* Style text */
    .stText {
        font-size: 1.2rem;
    }

    /* Style columns and images */
    .stImage {
        max-width: 90%; /* reduce image size */
    }
    </style>
""", unsafe_allow_html=True)



CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"


client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:17]:  
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters

st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #ff7e5f, #feb47b); 
        color: white; /* Change text color for better visibility 
    }
    .stButton>button {
        background-color: #ff4757; /* Button background color 
        color: white; /* Button text color */
    }
    .stSelectbox>div>div {
        background-color: rgba(255, 255, 255, 0.2); 
        color: white; 
    }
    h1 {
        color: lightblue; 
        font-family: 'Arial', sans-serif; 
        font-size: 3em; 
        text-align: center; 
    }
    </style>
    """,
    unsafe_allow_html=True
)


# st.markdown("<h1>Sound Like Me</h1>", unsafe_allow_html=True)

# st.header('SoundLikeMe')


st.image("F:\Music_Recommender_System-main\LOGO-removebg-preview.png") 
music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

music_list = music['song'].values
selected_movie = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_movie)
    
  
    for i in range(0, 16, 4):
        cols = st.columns(4)  
        for idx, col in enumerate(cols):
            with col:
                st.text(recommended_music_names[i + idx])
                st.image(recommended_music_posters[i + idx], use_column_width=True)
