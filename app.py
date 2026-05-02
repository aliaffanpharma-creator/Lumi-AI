import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURATION & DESIGN ---
st.set_page_config(page_title="Lumi - AI Digital Pharmacist", layout="wide")

# Custom CSS to match "Design Tempelate.jpg"
st.markdown("""
    <style>
    .main { background-color: #F8F9FE; }
    .stSidebar { background-color: #FFFFFF; border-right: 1px solid #E0E0E0; }
    .card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .risk-score { color: #FF4B4B; font-size: 48px; font-weight: bold; text-align: center; }
    .sidebar-item { padding: 10px; font-size: 16px; color: #5F6368; }
    .active-item { color: #6C5DD3; font-weight: bold; background: #F3F0FF; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://via.placeholder.com/50", width=50) # Replace with your Lumi Logo
    st.title("Lumi")
    st.markdown('<p class="active-item">🏠 Home</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-item">🔍 Scan Prescription</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-item">💊 My Medicines</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-item">⚠️ Drug Interactions</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-item">🔔 Reminders</p>', unsafe_allow_html=True)

# --- MAIN INTERFACE ---
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Hello, Ali 👋")
    st.write("We're here to help you stay healthy.")
    
    # SCAN SECTION
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Scan Prescription")
        uploaded_file = st.file_uploader("Upload or capture your prescription", type=['jpg', 'png', 'jpeg'])
        
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Prescription Uploaded", use_column_width=True)
            if st.button("Analyze with Lumi AI ✨"):
                st.info("Lumi is analyzing your prescription using Gemini 1.5 Flash...")
                # Here we would call your Gemini Logic
        st.markdown('</div>', unsafe_allow_html=True)

    # RISK SCORE & TABLE (Placeholder data matching your design)
    st.markdown("---")
    res_col1, res_col2 = st.columns([1, 2])
    with res_col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("Prescription Risk Score")
        st.markdown('<p class="risk-score">7.5 <span style="font-size:20px; color:gray;">/10</span></p>', unsafe_allow_html=True)
        st.write("Moderate Risk")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with res_col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("✨ AI Summary (In Simple Words)")
        st.warning("Drug Interactions: 2 interactions found. Dose Adjustment: 1 medicine may need adjustment.")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # SCHEDULE & ADHERENCE
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Today's Schedule")
    st.write("✅ 8:00 AM - Metformin 500mg")
    st.write("⏰ 1:00 PM - Amoxicillin 500mg")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card" style="margin-top:20px;">', unsafe_allow_html=True)
    st.subheader("Adherence Progress")
    st.progress(85)
    st.write("85% - Great job!")
    st.markdown('</div>', unsafe_allow_html=True)
