import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

MODEL = genai.GenerativeModel("gemini-1.5-flash")  # SDK model

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

# ---------------- FUNCTION ----------------
def get_songs(mood, language):
    prompt = f"""
Recommend exactly 5 songs.

Mood: {mood}
Language: {language}

Return ONLY in this format:

Song: <song name>
Singer: <singer name>
YouTube: https://www.youtube.com/results?search_query=<song+name+singer>
"""
    try:
        response = MODEL.generate_content(
            prompt=prompt,
            temperature=0.7,
            max_output_tokens=500
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
