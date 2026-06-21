import streamlit as st
import pandas as pd
import speech_recognition as sr
import urllib.parse

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="MoodTune Music DJ",
    page_icon="🎵",
    layout="wide"
)

# ---------------- BLACK THEME ----------------

st.markdown("""
<style>

.stApp{
background-color:#000000;
color:white;
}

h1,h2,h3,p,label{
color:white;
}

.stButton>button{
background:#1DB954;
color:white;
border-radius:12px;
font-size:16px;
}

div[data-baseweb="select"]{
color:black;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATASET ----------------

songs = pd.read_csv("songs.csv")

songs.columns = songs.columns.str.lower()

# ---------------- MOOD DETECTION ----------------

def detect_emotion(text):

    text = text.lower()

    happy = [
        "happy","love","good",
        "great","awesome",
        "joy","excited"
    ]

    sad = [
        "sad","cry",
        "hurt","lonely",
        "depressed"
    ]

    calm = [
        "calm","peace",
        "relax",
        "spiritual"
    ]

    angry = [
        "angry",
        "mad",
        "hate"
    ]

    for i in happy:

        if i in text:

            return "happy"

    for i in sad:

        if i in text:

            return "sad"

    for i in calm:

        if i in text:

            return "calm"

    for i in angry:

        if i in text:

            return "angry"

    return "happy"

# ---------------- RECOMMEND ----------------

def recommend(

emotion,

language,

category,

singer

):

    rec = songs.copy()

    if emotion != "All":

        rec = rec[

        rec["emotion"]

        .str.lower()

        ==

        emotion.lower()

        ]

    if language != "All":

        rec = rec[

        rec["language"]

        .str.lower()

        ==

        language.lower()

        ]

    if category != "All":

        rec = rec[

        rec["category"]

        .str.lower()

        ==

        category.lower()

        ]

    if singer != "All":

        rec = rec[

        rec["artist"]

        .str.lower()

        ==

        singer.lower()

        ]

    if len(rec)==0:

        return None

    return rec.sample(

    min(

    10,

    len(rec)

    )

    )

# ---------------- TITLE ----------------

st.title("🎵 MoodTune Music DJ")

st.write(

"AI Emotion Based Music Recommendation"

)

# ---------------- SIDEBAR ----------------

language = st.sidebar.selectbox(

"Language",

[

"All",

"Hindi",

"Punjabi",

"English"

]

)

category = st.sidebar.selectbox(

"Category",

[

"All",

"party",

"heartbroken",

"travel",

"friendship",

"qawwali",

"romantic",

"motivational",

"sad"

]

)

singer = st.sidebar.selectbox(

"Singer",

["All"]

+

sorted(

songs["artist"]

.unique()

)

)

# ---------------- TEXT INPUT ----------------

st.header("✍ Text Mood")

text = st.text_input(

"How are you feeling today?"

)

if st.button(

"Recommend Songs"

):

    emotion = detect_emotion(text)

    st.success(

    f"Detected Mood : {emotion}"

    )

    rec = recommend(

    emotion,

    language,

    category,

    singer

    )

    if rec is not None:

        for _,row in rec.iterrows():

            st.write(

            "🎵",

            row["song"]

            )

            st.write(

            "🎤",

            row["artist"]

            )

            st.write(

            "😊",

            row["emotion"]

            )

            st.write(

            "🎼",

            row["category"]

            )

            query = urllib.parse.quote(

            f"{row['song']} {row['artist']}"

            )

            youtube_url = (

            "https://www.youtube.com/results?"

            f"search_query={query}"

            )

            st.link_button(

            "▶ Play Song",

            youtube_url

            )

            st.divider()

    else:

        st.warning(

        "No Songs Found"

        )

# ---------------- VOICE INPUT ----------------

st.header("🎤 Voice Mood")

audio = st.file_uploader(

"Upload WAV File",

type=["wav"]

)

if st.button(

"Recommend From Voice"

):

    if audio:

        r = sr.Recognizer()

        with sr.AudioFile(audio) as source:

            data = r.record(source)

        text = r.recognize_google(data)

        st.write(

        "Recognized Text :",

        text

        )

        emotion = detect_emotion(text)

        st.success(

        f"Detected Mood : {emotion}"

        )

        rec = recommend(

        emotion,

        language,

        category,

        singer

        )

        if rec is not None:

            for _,row in rec.iterrows():

                st.write(

                "🎵",

                row["song"]

                )

                st.write(

                "🎤",

                row["artist"]

                )

                st.write(

                "😊",

                row["emotion"]

                )

                st.write(

                "🎼",

                row["category"]

                )

                query = urllib.parse.quote(

                f"{row['song']} {row['artist']}"

                )

                youtube_url = (

                "https://www.youtube.com/results?"

                f"search_query={query}"

                )

                st.link_button(

                "▶ Play Song",

                youtube_url

                )

                st.divider()

        else:

            st.warning(

            "No Songs Found"

            )
