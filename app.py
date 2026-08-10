import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64
import os
import time
from io import BytesIO
import requests  # <-- ADDED to fix NameError

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="HCC Video Generator – Gemini AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #e6f0ff, #d4e4f7) !important;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #0044aa, #0066cc, #3399ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding: 20px 0 5px 0;
    }
    .sub-title {
        text-align: center;
        color: #004488;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 30px;
    }
    .info-box {
        background: rgba(255,255,255,0.7);
        border-radius: 16px;
        padding: 25px;
        border: 1px solid rgba(0,68,170,0.15);
        margin: 15px 0;
    }
    .info-box h3 {
        color: #004488;
        margin-top: 0;
    }
    .script-box {
        background: #f0f7fe;
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #0066cc;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        max-height: 300px;
        overflow-y: auto;
        white-space: pre-wrap;
    }
    .stButton button {
        background: linear-gradient(135deg, #0066cc, #3399ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 12px 40px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s !important;
    }
    .stButton button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 5px 30px rgba(0,68,170,0.3) !important;
    }
    .footer {
        text-align: center;
        padding: 20px 0;
        color: #555;
        font-size: 0.9rem;
        border-top: 1px solid rgba(0,68,170,0.1);
        margin-top: 30px;
    }
    .video-container {
        background: #000;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 40px rgba(0,0,0,0.15);
    }
    .video-container video {
        width: 100%;
        display: block;
    }
    .closing-cards {
        background: #f0f7fe;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #0066cc;
        margin-top: 20px;
    }
    .closing-cards h4 {
        color: #004488;
        margin-top: 0;
    }
    .closing-cards p {
        margin: 6px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown('<div class="main-title">🎬 HCC – CEO Introduction Video</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Jean Charles RJ presents Haiti Culture Connection</div>', unsafe_allow_html=True)

# ---------- SCRIPT (Jean Charles RJ as CEO) ----------
SCRIPT = """HCC : Haiti Culture Connection. Le premier label de l'histoire du HMI. Une initiative novatrice pour la jeunesse productive d'Haïti. Désormais, les jeunes talents haïtiens ont un recours lorsqu'il s'agit de financer leurs projets artistiques @HCC. Avec une équipe engagée dédiée au mentorat des œuvres, à la promotion de notre patrimoine historique et culturel, et au marketing de la culture haïtienne. HCC vise à établir une connexion directe entre tous les artistes haïtiens, en reliant leurs entreprises et entreprises évoluant dans le secteur des arts afin qu'ils grandissent ensemble. Cette connexion directe facilitera les échanges commerciaux au sein du HMI et rapprochera également les artistes et le public - une connexion qui guidera tous les jeunes talents vers leurs objectifs. HCC est le nouveau patrimoine structurel de la culture haïtienne. La culture est la preuve la plus tangible de l'existence de toutes les civilisations."""

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 📋 Script Preview")
    with st.expander("Click to view the full script"):
        st.markdown(f'<div class="script-box">{SCRIPT}</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📞 Contact Info")
    st.markdown("**CEO:** Jean Charles RJ")
    st.markdown("**WhatsApp:** +18094177808")
    st.markdown("**Social Media:** @HCC")
    st.markdown("**Tagline:** 🇭🇹 HCC – Le nouveau patrimoine structurel de la culture haïtienne.")
    st.markdown("---")
    st.markdown("### 🎬 Video Info")
    st.markdown("**Source:** GitHub Repository")
    st.markdown("**Format:** MP4")
    st.markdown("**Size:** 2.62 MB")

# ---------- MAIN CONTENT ----------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="info-box">
        <h3>🎥 CEO Introduction Video</h3>
        <p>Watch Jean Charles RJ, CEO of Haiti Culture Connection, deliver a powerful presentation about the organization's mission and vision.</p>
        <p><strong>Video features:</strong></p>
        <ul>
            <li>Jean Charles RJ in a professional office setting</li>
            <li>Full script delivered in French</li>
            <li>HCC logo and Haitian monuments in the background</li>
            <li>Closing cards with CEO info, WhatsApp, social media, and tagline</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ---------- EMBEDDED VIDEO FROM GITHUB (correct raw URL) ----------
    video_url = "https://raw.githubusercontent.com/Deslandes1/nanobanana-mcp/refs/heads/main/Generate_it_now_because_I_don_.mp4"
    
    st.markdown(f"""
    <div class="video-container">
        <video controls autoplay>
            <source src="{video_url}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
    """, unsafe_allow_html=True)

    # ---------- CLOSING CARDS ----------
    st.markdown("""
    <div class="closing-cards">
        <h4>📋 Closing Cards Information</h4>
        <p><strong>CEO:</strong> Jean Charles RJ</p>
        <p><strong>WhatsApp:</strong> +18094177808</p>
        <p><strong>Social Media:</strong> @HCC</p>
        <p><strong>Tagline:</strong> 🇭🇹 HCC – Le nouveau patrimoine structurel de la culture haïtienne.</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------- DOWNLOAD BUTTON ----------
    st.markdown("### ⬇️ Download Video")
    st.markdown("Click the button below to download the video to your device.")
    
    # Fetch video data using requests (now imported)
    try:
        video_data = requests.get(video_url).content
        st.download_button(
            label="⬇️ Download Video (MP4)",
            data=video_data,
            file_name="HCC_CEO_Jean_Charles_RJ.mp4",
            mime="video/mp4",
            use_container_width=True
        )
    except Exception as e:
        st.warning("Could not fetch video for download. Please try again later.")
        st.error(f"Error: {e}")

with col2:
    st.markdown("""
    <div class="info-box">
        <h3>📌 About This Video</h3>
        <p>This video was generated using the following prompt:</p>
        <hr>
        <p style="font-size:0.85rem; color:#1a2b4c;">
        <strong>Visual Style:</strong> Jean Charles RJ wearing regular eyeglasses and a sleek black suit, sitting confidently at a desk in a modern, elegant office environment. In the background, the polished "Haiti Culture Connection" logo and subtle visual elements of Haitian historical monuments (like the Citadelle) are integrated.
        </p>
        <hr>
        <p style="font-size:0.85rem; color:#1a2b4c;">
        <strong>Audio:</strong> Jean Charles speaks fluently in French with an engaging and inspiring tone, delivering the full HCC presentation script.
        </p>
        <hr>
        <p style="font-size:0.85rem; color:#1a2b4c;">
        <strong>Closing Cards:</strong> CEO: Jean Charles RJ | WhatsApp: +18094177808 | Social Media: @HCC | Tagline: 🇭🇹 HCC – Le nouveau patrimoine structurel de la culture haïtienne.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
    <p>🇭🇹 Haiti Culture Connection – Built by <strong>Gesner Deslandes</strong></p>
    <p>📞 (509)-4738-5663 | ✉️ deslandes78@gmail.com</p>
    <p style="font-size:0.8rem; opacity:0.7;">GlobalInternet.py – Software Solutions</p>
</div>
""", unsafe_allow_html=True)
