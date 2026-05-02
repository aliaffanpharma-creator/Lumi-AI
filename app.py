import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd

# Page Config to match mockup layout
st.set_page_config(page_title="Lumi | AI Digital Pharmacist", layout="wide")

# Link to CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar Navigation (Replicating Design Tempelate.jpg)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/883/883360.png", width=50) # Placeholder Logo
st.sidebar.title("Lumi")
st.sidebar.markdown("---")
menu = ["Home", "Scan Prescription", "My Medicines", "Drug Interactions", "Reminders", "Patient Profile"]
choice = st.sidebar.radio("Menu", menu)

# API Setup - (You'll add your key in Streamlit Secrets)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

if choice == "Home":
    st.title("Hello, Ali 👋")
    st.write("We're here to help you stay healthy.")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Scan Prescription")
        uploaded_file = st.file_uploader("Upload or capture your prescription", type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Prescription Uploaded", use_column_width=True)
            
            if st.button("Analyze with Lumi AI"):
                with st.spinner("Lumi is analyzing safety data..."):
                    # The Prompt: Forcing precision and RAG-style grounding
                    prompt = """
                    You are Lumi, a digital pharmacist. Analyze this prescription image. 
                    1. Extract medicine names and dosages.
                    2. Provide a 'Prescription Risk Score' out of 10.
                    3. Check interactions using global standards (OpenFDA/PNF).
                    4. Explain each medicine in simple English and Urdu.
                    If any text is blurry, state 'UNCLEAR'.
                    Format the output as a JSON-like structure for a dashboard.
                    """
                    response = model.generate_content([prompt, img])
                    st.success("Analysis Complete!")
                    st.markdown(response.text)

    with col2:
        st.markdown("### Today's Schedule")
        st.info("8:00 AM - Metformin 500mg (Taken)")
        st.warning("1:00 PM - Amoxicillin 500mg (Due)")

# Footer Disclaimer (Safety First)
st.markdown("---")
st.caption("⚠️ Lumi is an AI assistant and not a replacement for professional medical advice. Always consult your doctor.")
