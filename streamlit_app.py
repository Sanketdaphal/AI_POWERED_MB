import streamlit as st
import numpy as np
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import colorsys
import re
import numpy.random
import time 

# --- CONFIGURATION (NO IMAGE FETCHING NEEDED) ---

# Load the small spaCy model for better NLP than basic NLTK
# NOTE: The model download is now handled by the .streamlit/install.sh script
@st.cache_resource
def load_nlp_model():
    # If the install.sh script works, this should load instantly
    try:
        nlp = spacy.load("en_core_web_sm")
        return nlp
    except OSError:
        st.error("FATAL ERROR: spaCy model not found. Check install.sh script and Streamlit secrets.")
        st.stop()


nlp = load_nlp_model()
STOP_WORDS = set(stopwords.words('english'))

# --- Rule-Based Color Generation and Style Mapping (UNCHANGED) ---

STYLE_MAPPING = {
    "warm": {"name": "Warm & Rustic", "hue_range": (0, 60), "saturation": 0.8, "value": 0.9, "image_keywords": "wood, sun, earth, cozy"},
    "cool": {"name": "Cool & Serene", "hue_range": (180, 240), "saturation": 0.7, "value": 0.8, "image_keywords": "water, blue, fog, metal, calm"},
    "neutral": {"name": "Neutral & Minimalist", "hue_range": (30, 60), "saturation": 0.1, "value": 0.9, "image_keywords": "grey, white, beige, light, linen"},
    "vibrant": {"name": "Vibrant & Playful", "hue_range": (0, 360), "saturation": 0.9, "value": 1.0, "image_keywords": "pop, colorful, neon, energetic, graphic"},
    "monochrome": {"name": "Monochrome & Elegant", "hue_range": (0, 0), "saturation": 0.0, "value": 0.5, "image_keywords": "black, white, shadow, high contrast"},
    "modern": {"name": "Modern / Geometric", "hue_range": (200, 240), "saturation": 0.5, "value": 0.7, "image_keywords": "clean, line, glass, steel, abstract"},
    "vintage": {"name": "Vintage / Retro", "hue_range": (20, 40), "saturation": 0.6, "value": 0.7, "image_keywords": "faded, film, 70s, texture, old"},
    "luxury": {"name": "Luxury & Opulent", "hue_range": (300, 340), "saturation": 0.5, "value": 0.5, "image_keywords": "gold, marble, velvet, dark, rich"},
    "nature": {"name": "Nature & Organic", "hue_range": (80, 160), "saturation": 0.7, "value": 0.6, "image_keywords": "green, plant, forest, wood, leaf"},
}

DEFAULT_STYLE_KEY = "neutral"

def rgb_to_hex(rgb):
    """Converts an RGB tuple (0-255) to a hex color string."""
    return '#%02x%02x%02x' % tuple(int(c) for c in rgb)

def generate_palette_from_hsv(style_data, num_colors=5):
    """Generates a color palette based on Hue, Saturation, and Value ranges."""
    palette = []
    
    h_min, h_max = style_data["hue_range"]
    if h_min == h_max:
        central_h = 0
    else:
        central_h = np.random.randint(h_min, h_max)
    
    v_values = np.linspace(0.95, 0.35, num_colors)
    s_values = np.linspace(style_data["saturation"]*1.1, style_data["saturation"]*0.7, num_colors)

    for i in range(num_colors):
        h = (central_h + (i * 20)) % 360
        s = np.clip(s_values[i], 0.05, 1.0)
        v = np.clip(v_values[i], 0.2, 1.0)
        
        rgb_tuple = colorsys.hsv_to_rgb(h / 360.0, s, v)
        hex_color = rgb_to_hex([c * 255 for c in rgb_tuple])
        palette.append(hex_color)
        
    return palette

def analyze_brief(brief, selected_mood):
    """Uses spaCy for basic keyword extraction to identify the best style."""
    
    if selected_mood and selected_mood.lower() in STYLE_MAPPING:
        style_key = selected_mood.lower()
    else:
        style_key = DEFAULT_STYLE_KEY

    doc = nlp(brief.lower())
    
    keywords = [token.lemma_ for token in doc if token.pos_ in ["NOUN", "ADJ"] and token.lemma_ not in STOP_WORDS]
    
    for key in STYLE_MAPPING:
        if key in keywords:
            style_key = key
            break

    style_data = STYLE_MAPPING.get(style_key, STYLE_MAPPING[DEFAULT_STYLE_KEY])
    
    # Combined keywords for image search
    image_keywords = f"{brief.split('.')[0]}, {style_data['image_keywords']}"
    
    return style_data, keywords, image_keywords

# --- Streamlit UI Layout ---

st.set_page_config(layout="wide", page_title="AI Moodboard Generator")

st.title("💡 AI-Powered Moodboard Generator")
st.subheader("Group : D_For_Design - Transform your design briefs into vibrant moodboards!")
st.markdown("---")

col_input, col_config = st.columns([3, 1])

with col_input:
    # --- FIX 1: Use value="" and placeholder to prevent default text analysis ---
    design_brief = st.text_area(
        "**1. Enter your Natural Language Design Brief**",
        value="", # CHANGED: Empty value
        placeholder="e.g., 'A high-end, luxury brand website with rich, dark colors and a modern, geometric font scheme.'", # NEW: Placeholder added
        height=120
    )

mood_options = list(STYLE_MAPPING.keys())
with col_config:
    st.markdown("**2. Optional: Select a Base Mood**")
    selected_mood = st.selectbox(
        label="Mood Category",
        options=[""] + [m.capitalize() for m in mood_options],
        index=0,
        help="This forces the AI toward a primary mood category (Warm, Cool, etc.)."
    )
    
    if st.button("**Generate Moodboard**", use_container_width=True, type="primary"):
        st.session_state['run_generation'] = True
    else:
        if 'run_generation' not in st.session_state:
            st.session_state['run_generation'] = False

st.markdown("---")

# --- Moodboard Output ---

if st.session_state.get('run_generation') and design_brief:
    
    with st.spinner("Analyzing brief, generating color palette, and preparing visual blueprint..."):
        
        # Core logic: NLP and Style Mapping
        style_data, keywords, image_prompt = analyze_brief(design_brief, selected_mood)
        
        # Color Generation (Rule-based)
        palette = generate_palette_from_hsv(style_data)
        
    
    st.header(f"✨ Generated Moodboard: {style_data['name']}")
    st.markdown(f"> **Keywords Extracted:** *{', '.join(keywords[:10])}*")
    
    # 1. Color Palette Display
    st.subheader("🎨 Color Palette")
    cols = st.columns(len(palette))
    for i, color in enumerate(palette):
        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    background-color: {color};
                    width: 100%;
                    height: 80px;
                    border-radius: 6px;
                    display: flex;
                    align-items: flex-end;
                    justify-content: center;
                    padding: 4px;
                ">
                    <code style="background-color: rgba(0,0,0,0.1); padding: 2px 4px; border-radius: 3px; color: #FFFFFF;">{color}</code>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("---")
    
    # 2. Visual Strategy Blueprint (NEW SECTION: Clean Markdown)
    st.subheader("📝 Visual Strategy Blueprint")
    st.markdown("---") 
    
    primary_color_hex = palette[0]
    color_list_text = ', '.join(palette)

    final_ai_prompt = (
        f"Generate an abstract design concept for a {style_data['name']} moodboard. "
        f"Key stylistic elements: {style_data['image_keywords']}. "
        f"Original theme: {design_brief}. "
        f"Primary colors to include are the hex codes: {color_list_text}. "
        "Focus on texture, composition, and lighting."
    )

    # Display the Style Breakdown and Keywords using clean Markdown
    st.markdown(f"""
    **Style Analysis:**
    * **Category:** <span style="color: {primary_color_hex}; font-weight: bold;">{style_data['name']}</span>
    * **Original Theme:** {design_brief}
    * **Visual Keywords:** {style_data['image_keywords'].replace(',', ', ')}
    * **Color Palette:** {color_list_text}
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("**Primary Image Prompt (Ready for DALL-E/Imagen):**")
    
    # Use st.code for a native, clean, copy-paste block for the AI model
    st.code(final_ai_prompt, language='markdown') 

    st.markdown("---")

    # 3. Refinement/Feedback
    st.subheader("Refinement & Next Steps")
    col_refine_1, col_refine_2 = st.columns(2)
    with col_refine_1:
        if st.button("🔄 **Regenerate Moodboard** (Reruns logic for variation)"):
             st.session_state['run_generation'] = True
             st.experimental_rerun()
    with col_refine_2:
        st.button("👍 **Save to Project** (Future Feature)")

elif st.session_state.get('run_generation') and not design_brief:
    st.warning("Please enter a design brief to generate the moodboard.")
