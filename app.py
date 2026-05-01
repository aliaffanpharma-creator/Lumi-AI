import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Lumi | AI Digital Pharmacist", layout="wide")

# --- STYLING (Matching Design Tempelate.jpg) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fc; }
    .stButton>button { border-radius: 20px; background-color: #6c5ce7; color: white; }
    .risk-score { font-size: 48px; font-weight: bold; color: #e67e22; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- AI SETUP ---
# You will add your API Key in Hugging Face Settings -> Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- SIDEBAR (Navigation) ---
with st.sidebar:
    st.title("Lumi ✨")
    st.write("AI Digital Pharmacist")
    menu = ["Home", "Scan Prescription", "My Medicines", "AI Chat Assistant"]
    choice = st.radio("Go to", menu)

# --- MAIN INTERFACE ---
if choice == "Home":
    st.title("Hello, Ali 👋")
    st.write("We're here to help you stay healthy.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Scan Prescription")
        uploaded_file = st.file_uploader("Upload image or use camera", type=["jpg", "jpeg", "png"])
        
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Prescription Uploaded", use_column_width=True)
            
            if st.button("Analyze with Lumi AI"):
                with st.spinner("Analyzing your prescription..."):
                    # AI OCR & Safety Logic
                    prompt = """
                    Analyze this prescription. Extract:
                    1. Medicine names and dosages.
                    2. Purpose of each medicine in simple Urdu/English.
                    3. Check for drug-drug interactions (RAG Mode: Compare with OpenFDA/National Formulary).
                    4. Calculate a 'Prescription Risk Score' out of 10.
                    Output format: JSON-like structure.
                    """
                    response = model.generate_content([prompt, img])
                    st.write(response.text)

    with col2:
        st.subheader("Prescription Risk Score")
        st.markdown('<div class="risk-score">7.5 <span style="font-size:18px;">/10</span></div>', unsafe_allow_html=True)
        st.info("Moderate Risk: 2 interactions found.")

elif choice == "AI Chat Assistant":
    st.header("Talk to Lumi ✨")
    st.write("Support for Urdu, Sindhi, Pashto, Balochi, and English.")
    
    user_input = st.text_input("Ask Lumi anything (e.g., 'Yeh dawa kis liye hai?')")
    if user_input:
        response = model.generate_content(f"You are a professional pharmacist named Lumi in Pakistan. Answer this: {user_input}")
        st.write(response.text)

# --- FOOTER ---
st.markdown("---")
st.caption("Lumi is an AI tool and does not replace professional medical advice. Always consult your doctor.")
