import streamlit as st
import google.generativeai as genai
import base64
import time
import requests
import json

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="HCC Video Generator",
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
        width: 100%;
    }
    .stButton button:hover {
        transform: scale(1.02) !important;
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
        margin-top: 15px;
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
    .prompt-box {
        background: #f8f9fa;
        border: 1px solid #dde1e6;
        border-radius: 8px;
        padding: 15px;
        font-family: monospace;
        font-size: 0.85rem;
        white-space: pre-wrap;
        max-height: 300px;
        overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown('<div class="main-title">🎬 HCC – CEO Introduction Video</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Generate a professional video with Jean Charles RJ</div>', unsafe_allow_html=True)

# ---------- SCRIPT ----------
SCRIPT = """HCC : Haiti Culture Connection. Le premier label de l'histoire du HMI. Une initiative novatrice pour la jeunesse productive d'Haïti. Désormais, les jeunes talents haïtiens ont un recours lorsqu'il s'agit de financer leurs projets artistiques @HCC. Avec une équipe engagée dédiée au mentorat des œuvres, à la promotion de notre patrimoine historique et culturel, et au marketing de la culture haïtienne. HCC vise à établir une connexion directe entre tous les artistes haïtiens, en reliant leurs entreprises et entreprises évoluant dans le secteur des arts afin qu'ils grandissent ensemble. Cette connexion directe facilitera les échanges commerciaux au sein du HMI et rapprochera également les artistes et le public - une connexion qui guidera tous les jeunes talents vers leurs objectifs. HCC est le nouveau patrimoine structurel de la culture haïtienne. La culture est la preuve la plus tangible de l'existence de toutes les civilisations."""

PROMPT = f"""Generate a high-end, professional cinematic video featuring Jean Charles RJ as the CEO of Haiti Culture Connection.

**Visual Style:**
- Jean Charles RJ wearing regular eyeglasses and a sleek black suit
- Sitting confidently at a desk in a modern, elegant office environment
- In the background, the polished "Haiti Culture Connection" logo and subtle visual elements of Haitian historical monuments (like the Citadelle) are integrated
- Professional lighting, cinematic quality, 16:9 aspect ratio
- Smooth transitions, inspiring atmosphere

**Audio/Speech:**
- Jean Charles speaks fluently in French with an engaging and inspiring tone
- He delivers the following script naturally:

"{SCRIPT}"

**Closing Cards (on-screen text at the end):**
- CEO: Jean Charles RJ
- WhatsApp: +18094177808
- Social Media: @HCC
- Tagline: 🇭🇹 HCC – Le nouveau patrimoine structurel de la culture haïtienne.

**Requirements:**
- High-resolution (1080p or higher)
- Professional, corporate, inspirational tone
- Subtle background music (elegant, inspiring)
- The video should look like a professional corporate announcement.
- Duration: approximately 60-90 seconds.
"""

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 🔑 Gemini API Key")
    api_key = st.text_input("Enter your API key", type="password")
    st.markdown("---")
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
    st.markdown("### 🎬 Generation Info")
    st.markdown("**Model:** Gemini 2.0 Flash (text-to-video)")
    st.markdown("**Resolution:** 1080p")
    st.markdown("**Duration:** ~60-90 seconds")

# ---------- MAIN CONTENT ----------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="info-box">
        <h3>🎥 Generate Your Video</h3>
        <p>Use the power of Gemini AI to create a professional introduction video of Jean Charles RJ, CEO of Haiti Culture Connection.</p>
        <ul>
            <li>Jean Charles RJ in a modern office with HCC branding</li>
            <li>Full script delivered in French</li>
            <li>Professional closing cards with CEO info and contacts</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ---------- GENERATION BUTTON ----------
    if st.button("🚀 Generate Video", use_container_width=True):
        if not api_key:
            st.error("❌ Please enter your Gemini API key in the sidebar.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.0-flash-exp')
                
                with st.spinner("🎬 Generating your video... This may take 2-4 minutes."):
                    # Remove unsupported 'response_modalities' argument
                    response = model.generate_content(
                        PROMPT,
                        generation_config=genai.types.GenerationConfig(
                            temperature=0.7,
                            max_output_tokens=2048,
                        )
                    )
                    
                    # Check if video data is present
                    video_data = None
                    if hasattr(response, 'candidates') and response.candidates:
                        for candidate in response.candidates:
                            if hasattr(candidate, 'content') and candidate.content:
                                for part in candidate.content.parts:
                                    if hasattr(part, 'inline_data') and part.inline_data:
                                        # This might be video data
                                        video_data = part.inline_data.data
                                        break
                    
                    if video_data:
                        st.success("✅ Video generated successfully!")
                        st.markdown("---")
                        
                        video_base64 = base64.b64encode(video_data).decode()
                        st.markdown(f"""
                        <div class="video-container">
                            <video controls autoplay>
                                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                                Your browser does not support the video tag.
                            </video>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.download_button(
                            label="⬇️ Download Video (MP4)",
                            data=video_data,
                            file_name="HCC_CEO_Jean_Charles_RJ.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )
                        
                        st.markdown("""
                        <div class="closing-cards">
                            <h4>📋 Closing Cards Information</h4>
                            <p><strong>CEO:</strong> Jean Charles RJ</p>
                            <p><strong>WhatsApp:</strong> +18094177808</p>
                            <p><strong>Social Media:</strong> @HCC</p>
                            <p><strong>Tagline:</strong> 🇭🇹 HCC – Le nouveau patrimoine structurel de la culture haïtienne.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Fallback: provide the prompt for AI Studio
                        st.warning("⚠️ Video generation via API may not be fully supported yet. However, you can use the same prompt in Google AI Studio to generate the video for free.")
                        st.markdown("---")
                        st.markdown("### 📋 Copy this prompt to AI Studio")
                        st.markdown(f'<div class="prompt-box">{PROMPT}</div>', unsafe_allow_html=True)
                        st.markdown("""
                        <br>
                        <a href="https://aistudio.google.com/" target="_blank">
                            <button style="background: #0066cc; color: white; border: none; padding: 12px 30px; border-radius: 30px; font-weight: 600; cursor: pointer;">
                                🔗 Open Google AI Studio
                            </button>
                        </a>
                        """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Error generating video: {str(e)}")
                st.info("💡 Make sure your API key is valid. If video generation via API is not available, use the prompt above in Google AI Studio.")

with col2:
    st.markdown("""
    <div class="info-box">
        <h3>📌 Prompt Details</h3>
        <p><strong>Visual Style:</strong></p>
        <ul>
            <li>Jean Charles RJ wearing eyeglasses and black suit</li>
            <li>Modern office setting with laptop</li>
            <li>HCC logo and Citadelle in background</li>
        </ul>
        <p><strong>Audio:</strong></p>
        <ul>
            <li>Full script in French</li>
            <li>Engaging, inspiring tone</li>
        </ul>
        <p><strong>Closing Cards:</strong></p>
        <ul>
            <li>CEO, WhatsApp, Social Media, Tagline</li>
        </ul>
        <hr>
        <p style="font-size:0.8rem; color:#555;">This prompt was crafted to match your exact specifications.</p>
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
