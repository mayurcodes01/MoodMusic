import streamlit as st
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Create the Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# ---------------- UI ----------------
st.set_page_config(
    page_title="Mood Music Recommender 🎵",
    page_icon="🎧",
    layout="centered"
)

st.title("🎵 Mood Based Music Recommendation")
st.write("Choose your mood and language. I’ll suggest songs just for you.")

# ---------------- MOODS ----------------
st.subheader("1️⃣ Choose your mood")
moods = [
    "Happy",
    "Romantic",
    "Sad",
    "Chill",
    "Energetic",
    "Motivational",
    "Heartbreak",
    "Peaceful"
]
selected_mood = st.radio("", moods, horizontal=True)

# ---------------- LANGUAGE ----------------
st.subheader("2️⃣ Choose language")
language = st.selectbox("", ["Hindi", "Marathi", "English"])

def get_songs(mood, language):
    prompt = (
        f"Recommend exactly 5 songs.\n\n"
        f"Mood: {mood}\n"
        f"Language: {language}\n\n"
        f"Return ONLY in this format:\n"
        f"Song: <song name>\n"
        f"Singer: <singer name>\n"
        f"YouTube: https://www.youtube.com/results?search_query=<song+name+singer>\n"
    )

    try:
        # Use the new client to generate content
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # latest supported model
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
            )
        )
        return response.text
    except Exception as e:
        return f"Error generating songs: {e}"

# ---------------- BUTTON ----------------
st.subheader("3️⃣ Get Recommendations")
if st.button("🎶 Recommend Songs"):
    if not GEMINI_API_KEY:
        st.error("Gemini API key not found. Please set GEMINI_API_KEY.")
    else:
        with st.spinner("Finding the perfect songs..."):
            result = get_songs(selected_mood, language)
            st.success("Here you go 🎧")
            st.markdown(result)
