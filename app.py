import streamlit as st
import requests
import os

# ---------------- CONFIG ----------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-1.5-flash:generateContent"
)

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
    "Happy 😊",
    "Romantic ❤️",
    "Sad 😔",
    "Chill 🌙",
    "Energetic ⚡",
    "Motivational 🔥",
    "Heartbreak 💔",
    "Peaceful 🌸"
]

selected_mood = st.radio("", moods, horizontal=True)

# ---------------- LANGUAGE ----------------
st.subheader("2️⃣ Choose language")

language = st.selectbox(
    "",
    ["Hindi", "Marathi", "English"]
)

# ---------------- BUTTON ----------------
st.subheader("3️⃣ Get Recommendations")

def get_songs(mood, language):
    prompt = f"""
    Suggest 5 {language} songs for the mood "{mood}".

    For each song, provide:
    - Song name
    - Singer
    - YouTube search link

    Format strictly like this:

    1. Song Name - Singer
       YouTube: link

    Keep it clean and simple.
    """

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
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

    response.raise_for_status()
    data = response.json()

    return data["candidates"][0]["content"]["parts"][0]["text"]

if st.button("🎶 Recommend Songs"):
    if not GEMINI_API_KEY:
        st.error("Gemini API key not found.")
    else:
        with st.spinner("Finding the perfect songs..."):
            try:
                result = get_songs(selected_mood, language)
                st.success("Here you go 🎧")
                st.markdown(result)
            except Exception as e:
                st.error("Something went wrong. Please try again.")
