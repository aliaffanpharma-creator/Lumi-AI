import streamlit as st
from PIL import Image
import easyocr
import google.generativeai as genai
import os
import random

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Lumi AI Pharmacist", layout="wide")

# ---------------- GEMINI SETUP ----------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "AI response error. Please try again."

# ---------------- OCR ----------------
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

def extract_text(image):
    result = reader.readtext(image)
    text = " ".join([res[1] for res in result])
    return text

# ---------------- BASIC MED EXTRACTION ----------------
def extract_medicines(text):
    lines = text.split()
    meds = []
    for word in lines:
        if len(word) > 4:
            meds.append(word)
    return list(set(meds))[:5]

# ---------------- RISK SCORE (SMARTER MOCK) ----------------
def generate_risk():
    score = round(random.uniform(5.5, 8.8), 1)
    if score > 8:
        level = "High Risk"
    elif score > 6.5:
        level = "Moderate Risk"
    else:
        level = "Low Risk"
    return score, level

# ---------------- SIDEBAR ----------------
st.sidebar.title("✨ Lumi")
menu = st.sidebar.radio("Navigation", [
    "Home",
    "Scan Prescription",
    "AI Chat"
])

# ---------------- HOME ----------------
if menu == "Home":
    st.title("Hello, Ali 👋")
    st.subheader("Your AI Digital Pharmacist")

    st.info("Upload a prescription to analyze medicines, risks, and safety.")

# ---------------- SCAN ----------------
if menu == "Scan Prescription":
    st.title("📄 Scan Prescription")

    uploaded = st.file_uploader("Upload Prescription Image", type=["png","jpg","jpeg"])

    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption="Uploaded Prescription", use_column_width=True)

        with st.spinner("Reading prescription..."):
            text = extract_text(image)

        st.subheader("🧾 Extracted Text")
        st.write(text if text else "No text detected")

        meds = extract_medicines(text)

        # Risk Score
        score, level = generate_risk()
        st.subheader("⚠️ Prescription Risk Score")
        st.metric(label="Risk Score", value=f"{score}/10", delta=level)

        # AI Explanation
        st.subheader("🧠 AI Summary")
        prompt = f"""
        You are a medical assistant.
        Explain these medicines simply and safely: {meds}

        Include:
        - What each medicine is for
        - How to take it
        - Any important warnings
        Keep it simple for patients.
        """
        summary = ask_gemini(prompt)
        st.write(summary)

        # Medicine List
        st.subheader("💊 Detected Medicines")
        for m in meds:
            st.write(f"• {m}")

# ---------------- CHAT ----------------
if menu == "AI Chat":
    st.title("💬 Ask Lumi")

    user_input = st.text_input("Ask about your medicine (English or Urdu)")

    if user_input:
        prompt = f"""
        You are Lumi, a safe medical assistant.

        Answer clearly and safely:
        {user_input}

        If unsure, advise consulting a doctor.
        """
        response = ask_gemini(prompt)
        st.write(response)
