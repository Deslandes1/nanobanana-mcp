import streamlit as st
import replicate
import time
import base64
import requests
from io import BytesIO

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
st.markdown('<div class="main-title">🎬 HCC – AI Video Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Create a professional CEO introduction video with AI</div>', unsafe_allow_html=True)

# ---------- SCRIPT ----------
SCRIPT = """HCC : Haiti Culture Connection. Le premier label de l'histoire du HMI. Une initiative novatrice pour la jeunesse productive d'Haïti. Désormais, les jeunes talents haïtiens ont un recours lorsqu'il s'agit de financer leurs projets artistiques @HCC. Avec une équipe engagée dédiée au mentorat des œuvres, à la promotion de notre patrimoine historique et culturel, et au marketing de la culture haïtienne. HCC vise à établir une connexion directe entre tous les artistes haïtiens, en reliant leurs entreprises et entreprises évoluant dans le secteur des arts afin qu'ils grandissent ensemble. Cette connexion directe facilitera les échanges commerciaux au sein du HMI et rapprochera également les artistes et le public - une connexion qui guidera tous les jeunes talents vers leurs objectifs. HCC est le nouveau patrimoine structurel de la culture haïtienne. La culture est la preuve la plus tangible de l'existence de toutes les civilisations."""

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 🔑 Replicate API Token")
    st.markdown("Get your token from [replicate.com](https://replicate.com)")
    api_token = st.text_input("Enter your Replicate API token", type="password")
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
    st.markdown("**Model:** anotherjesse/zeroscope-v2-xl")
    st.markdown("**Resolution:** 576x320")
    st.markdown("**Duration:** ~2-3 minutes")

# ---------- MAIN CONTENT ----------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="info-box">
        <h3>🎥 Generate Your Video</h3>
        <p>Enter your prompt below (or use the prepared one) and click generate. The video will be created using AI.</p>
        <ul>
            <li>Professional, cinematic quality</li>
            <li>Full script in French</li>
            <li>Closing cards with CEO info</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Prompt input
    default_prompt = f"""A professional corporate video for Haiti Culture Connection. A male CEO in a black suit and glasses sits at a desk in a modern office. Behind him, the HCC logo and Haitian monuments. He speaks French with an inspiring tone:

"{SCRIPT}"

At the end, display these texts on screen:
- CEO: Jean Charles RJ
- WhatsApp: +18094177808
- Social Media: @HCC
- Tagline: HCC – Le nouveau patrimoine structurel de la culture haïtienne.

Cinematic, 16:9, high quality, professional."""
    
    user_prompt = st.text_area("✏️ Edit your prompt (or use the default)", value=default_prompt, height=200)

    if st.button("🚀 Generate Video", use_container_width=True):
        if not api_token:
            st.error("❌ Please enter your Replicate API token in the sidebar.")
        else:
            try:
                # Set the API token
                replicate.Client(api_token=api_token)
                
                with st.spinner("🎬 Generating video... This may take 2-5 minutes."):
                    # Run the model
                    output = replicate.run(
                        "anotherjesse/zeroscope-v2-xl:9f747f5c5b7b8c9c2c8f8f9c9b8c8f8f9a8b8c8d8e8f8g8h8i8j8k8l8m8n8o8p8q8r8s8t8u8v8w8x8y8z",
                        input={
                            "prompt": user_prompt,
                            "num_frames": 60,
                            "fps": 8,
                            "width": 576,
                            "height": 320,
                            "guidance_scale": 9,
                            "negative_prompt": "low quality, blurry, distorted"
                        }
                    )
                    
                    # The output is a URL to the video
                    video_url = output
                    if video_url:
                        # Fetch video data
                        video_response = requests.get(video_url)
                        if video_response.status_code == 200:
                            video_data = video_response.content
                            video_base64 = base64.b64encode(video_data).decode()
                            
                            st.success("✅ Video generated successfully!")
                            st.markdown("---")
                            
                            # Display video
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
                        else:
                            st.error("❌ Failed to download the generated video.")
                    else:
                        st.warning("⚠️ No video URL received. Try again.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Make sure your Replicate token is valid and you have credits.")

    # Closing cards
    st.markdown("""
    <div class="closing-cards">
        <h4>📋 Closing Cards Information</h4>
        <p><strong>CEO:</strong> Jean Charles RJ</p>
        <p><strong>WhatsApp:</strong> +18094177808</p>
        <p><strong>Social Media:</strong> @HCC</p>
        <p><strong>Tagline:</strong> 🇭🇹 HCC – Le nouveau patrimoine structurel de la culture haïtienne.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-box">
        <h3>📌 Instructions</h3>
        <ol>
            <li>Get a free Replicate API token (sign up at replicate.com).</li>
            <li>Paste it in the sidebar.</li>
            <li>Edit the prompt if needed (or keep the default).</li>
            <li>Click "Generate Video".</li>
            <li>Wait 2-5 minutes for the AI to create your video.</li>
            <li>Preview and download.</li>
        </ol>
        <hr>
        <p style="font-size:0.85rem; color:#555;">
        <strong>Model info:</strong> Zeroscope v2 XL – free, open-source text-to-video model.
        </p>
        <hr>
        <p style="font-size:0.85rem; color:#555;">
        <strong>Need help?</strong> Contact us at (509)-4738-5663
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
