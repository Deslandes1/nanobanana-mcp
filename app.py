import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64
import os
import time
from io import BytesIO

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
    </style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown('<div class="main-title">🎬 HCC – Video Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Powered by Gemini AI · Create cinematic CEO introduction videos</div>', unsafe_allow_html=True)

# ---------- SCRIPT & PROMPT ----------
SCRIPT = """HCC : Haiti Culture Connection. Le premier label de l'histoire du HMI. Une initiative novatrice pour la jeunesse productive d'Haïti. Désormais, les jeunes talents haïtiens ont un recours lorsqu'il s'agit de financer leurs projets artistiques @HCC. Avec une équipe engagée dédiée au mentorat des œuvres, à la promotion de notre patrimoine historique et culturel, et au marketing de la culture haïtienne. HCC vise à établir une connexion directe entre tous les artistes haïtiens, en reliant leurs entreprises et entreprises évoluant dans le secteur des arts afin qu'ils grandissent ensemble. Cette connexion directe facilitera les échanges commerciaux au sein du HMI et rapprochera également les artistes et le public - une connexion qui guidera tous les jeunes talents vers leurs objectifs. HCC est le nouveau patrimoine structurel de la culture haïtienne. La culture est la preuve la plus tangible de l'existence de toutes les civilisations."""

PROMPT = f"""
Generate a high-end, professional cinematic video featuring Jean Charles RJ as the CEO of Haiti Culture Connection. 

**Visual Style:**
- Jean Charles RJ is wearing regular eyeglasses and a sleek black suit
- He is sitting confidently at a desk in a modern, elegant office environment
- A single laptop is open before him
- In the background, the polished "Haiti Culture Connection" logo and subtle visual elements of Haitian historical monuments (like the Citadelle) are integrated
- Professional lighting, cinematic quality, 16:9 aspect ratio

**Audio/Speech:**
- Jean Charles speaks fluently in French with an engaging and inspiring tone
- He delivers the following script naturally:

"{SCRIPT}"

**Closing Cards (On-screen text):**
- CEO: Jean Charles RJ
- WhatsApp: +18094177808
- Social Media: @HCC
- Tagline: 🇭🇹 HCC – Le nouveau patrimoine structurel de la culture haïtienne.

**Requirements:**
- High-resolution (1080p or higher)
- Professional, corporate, inspirational tone
- Smooth transitions
- Subtle background music (elegant, inspiring)
- The video should look like a professional corporate announcement from a major organization.
"""

# ---------- SIDEBAR: API KEY ----------
with st.sidebar:
    st.markdown("## 🔑 Gemini API Key")
    st.markdown("Enter your Google Gemini API key to generate the video.")
    api_key = st.text_input("API Key", type="password", placeholder="Paste your API key here...")
    st.markdown("---")
    st.markdown("### 📋 Script Preview")
    with st.expander("Click to view the full script"):
        st.markdown(f'<div class="script-box">{SCRIPT}</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📞 Contact Info")
    st.markdown("**CEO:** Jean Charles RJ")
    st.markdown("**WhatsApp:** +18094177808")
    st.markdown("**Social Media:** @HCC")
    st.markdown("**Tagline:** 🇭🇹 HCC – Le nouveau patrimoine structurel de la culture haïtienne.")

# ---------- MAIN CONTENT ----------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="info-box">
        <h3>🎯 Generate Your Video</h3>
        <p>This tool uses Google Gemini AI to generate a professional, cinematic video of Jean Charles RJ presenting Haiti Culture Connection.</p>
        <p><strong>What you'll get:</strong></p>
        <ul>
            <li>High-quality cinematic video (1080p)</li>
            <li>Jean Charles RJ speaking the full script in French</li>
            <li>Professional office background with HCC logo & Haitian monuments</li>
            <li>Closing cards with CEO info, WhatsApp, social media, and tagline</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Video generation button
    if st.button("🎬 Generate Video", use_container_width=True):
        if not api_key:
            st.error("❌ Please enter your Gemini API key in the sidebar.")
        else:
            try:
                # Configure Gemini
                genai.configure(api_key=api_key)
                
                with st.spinner("🎬 Generating your video... This may take 1-3 minutes."):
                    # Create the video generation request
                    model = genai.GenerativeModel('gemini-2.0-flash-exp')
                    
                    # For video generation, we need to use the generate_content with video generation enabled
                    # Note: Gemini video generation is still evolving; this uses the latest capabilities
                    response = model.generate_content(
                        PROMPT,
                        generation_config=genai.types.GenerationConfig(
                            response_modalities=["VIDEO"],
                            temperature=0.7,
                            max_output_tokens=2048,
                        )
                    )
                    
                    # Process the response
                    if hasattr(response, 'candidates') and response.candidates:
                        for candidate in response.candidates:
                            if hasattr(candidate, 'content') and candidate.content:
                                for part in candidate.content.parts:
                                    if hasattr(part, 'inline_data') and part.inline_data:
                                        video_data = part.inline_data.data
                                        video_base64 = base64.b64encode(video_data).decode()
                                        
                                        st.markdown("### ✅ Video Generated Successfully!")
                                        st.markdown("---")
                                        
                                        # Display the video
                                        st.markdown(f"""
                                        <div class="video-container">
                                            <video controls autoplay>
                                                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                                                Your browser does not support the video tag.
                                            </video>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        
                                        # Download button
                                        st.download_button(
                                            label="⬇️ Download Video (MP4)",
                                            data=video_data,
                                            file_name="HCC_CEO_Jean_Charles_RJ.mp4",
                                            mime="video/mp4",
                                            use_container_width=True
                                        )
                                        
                                        # Display closing cards info
                                        st.markdown("---")
                                        st.markdown("""
                                        <div style="background: #f0f7fe; padding: 20px; border-radius: 12px; border: 1px solid #0066cc;">
                                            <h4 style="color: #004488;">📋 Closing Cards Information</h4>
                                            <p><strong>CEO:</strong> Jean Charles RJ</p>
                                            <p><strong>WhatsApp:</strong> +18094177808</p>
                                            <p><strong>Social Media:</strong> @HCC</p>
                                            <p><strong>Tagline:</strong> 🇭🇹 HCC – Le nouveau patrimoine structurel de la culture haïtienne.</p>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        break
                    else:
                        st.warning("⚠️ No video data received. The Gemini API may not support video generation in your region yet.")
                        st.info("💡 Try using the 'video generation' capability in Google AI Studio instead.")
                        
            except Exception as e:
                st.error(f"❌ Error generating video: {str(e)}")
                st.info("💡 Make sure your API key is valid and has video generation enabled.")
                st.info("📌 If video generation isn't available, try using Google AI Studio directly with the same prompt.")

with col2:
    st.markdown("""
    <div class="info-box">
        <h3>📌 Instructions</h3>
        <ol>
            <li>Enter your Gemini API key in the sidebar</li>
            <li>Click "Generate Video"</li>
            <li>Wait 1-3 minutes for generation</li>
            <li>Preview and download your video</li>
        </ol>
        <br>
        <h4>🔑 Getting an API Key</h4>
        <p>1. Go to <a href="https://ai.google.dev/" target="_blank">Google AI Studio</a></p>
        <p>2. Create an account or sign in</p>
        <p>3. Generate an API key with video generation enabled</p>
        <br>
        <h4>💡 Alternative</h4>
        <p>If video generation isn't available via API yet, use <a href="https://aistudio.google.com/" target="_blank">Google AI Studio</a> directly with the same prompt.</p>
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
