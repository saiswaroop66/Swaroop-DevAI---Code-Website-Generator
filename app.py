import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("🤖 Swaroop DevAI - Code & Website Generator")

prompt = st.text_area("What would you like to build?")

# -----------------------------
# MODE SELECTOR
# -----------------------------
mode = st.selectbox("Choose Mode", ["Auto", "Website Builder", "Code Generator"])


# -----------------------------
# INTENT DETECTION
# -----------------------------
def detect_intent(text):
    text = text.lower()

    website_keywords = [
        "website", "landing page", "portfolio",
        "html", "css", "frontend", "ui"
    ]

    if any(word in text for word in website_keywords):
        return "website"

    return "code"


# -----------------------------
# WEBSITE GENERATOR
# -----------------------------
def generate_website(user_prompt):
    return client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""
You are a senior frontend developer.

Create a COMPLETE working website for:

{user_prompt}

Return format:

INDEX.HTML:
...
STYLE.CSS:
...
SCRIPT.JS:
...

Rules:
- Fully responsive
- Clean modern UI
- No external libraries
"""
            }
        ]
    ).choices[0].message.content


# -----------------------------
# CODE GENERATOR
# -----------------------------
def generate_code(user_prompt):
    return client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""
Generate complete working code for:

{user_prompt}

Rules:
- Only return clean, runnable code
- No extra explanation
"""
            }
        ]
    ).choices[0].message.content


# -----------------------------
# MAIN BUTTON
# -----------------------------
if st.button("Generate"):

    if not prompt:
        st.warning("Please enter a prompt")
    else:

        # Decide mode
        if mode == "Auto":
            intent = detect_intent(prompt)
        elif mode == "Website Builder":
            intent = "website"
        else:
            intent = "code"

        # -------------------------
        # WEBSITE MODE
        # -------------------------
        if intent == "website":
            response = generate_website(prompt)

            st.subheader("🌐 Generated Website Code")
            st.code(response, language="markdown")

        # -------------------------
        # CODE MODE
        # -------------------------
        else:
            response = generate_code(prompt)

            st.subheader("💻 Generated Code")
            st.code(response)