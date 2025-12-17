import streamlit as st
import requests
import os

# ---------------- CONFIG ----------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL = "gemini-pro"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent"

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

language = st.selectbox(
    "",
    ["Hindi", "Marathi", "English"]
)

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

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"{GEMINI_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        return f"API Error {response.status_code}: {response.text}"

    data = response.json()

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return "No recommendations found. Try another mood."

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
