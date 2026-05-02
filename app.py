import streamlit as st
from PIL import Image
import pytesseract
from transformers import pipeline
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="Lumi AI Pharmacist", layout="wide")

# --- SIDEBAR ---
st.sidebar.title("✨ Lumi")
menu = st.sidebar.radio("", [
    "Home", "Scan Prescription", "My Medicines",
    "Drug Interactions", "Reminders", "AI Chat"
])

# --- AI MODEL ---
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="google/flan-t5-base")

generator = load_model()

# --- OCR FUNCTION ---
def extract_text(image):
    return pytesseract.image_to_string(image)

# --- FAKE SAFETY ENGINE ---
def analyze_meds(text):
    meds = []
    lines = text.split("\n")
    for line in lines:
        if len(line) > 3:
            meds.append(line.strip())
    return meds[:4]

def risk_score():
    return round(random.uniform(5, 9), 1)

# --- HOME ---
if menu == "Home":
    st.title("Hello, Ali 👋")
    st.subheader("Your AI Digital Pharmacist")

    st.markdown("## Scan Prescription")
    uploaded = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])

    if uploaded:
        image = Image.open(uploaded)
        st.image(image, width=300)

        text = extract_text(image)
        meds = analyze_meds(text)

        st.markdown("## Prescription Risk Score")
        score = risk_score()
        st.metric("Risk Score", f"{score}/10")

        st.markdown("## Medicines")

        for m in meds:
            st.write(f"💊 {m}")

        st.markdown("## AI Summary")
        prompt = f"Explain these medicines simply: {meds}"
        response = generator(prompt, max_length=100)[0]["generated_text"]
        st.write(response)

# --- CHAT ---
if menu == "AI Chat":
    st.title("💬 Ask Lumi")

    user_input = st.text_input("Ask about your medicine")

    if user_input:
        response = generator(user_input, max_length=100)[0]["generated_text"]
        st.write(response)
