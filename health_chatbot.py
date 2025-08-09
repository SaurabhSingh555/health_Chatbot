import streamlit as st
import pandas as pd
import random
from streamlit_chat import message

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv('common_diseases_expanded.csv')

df = load_data()

# Hindi responses with emojis
responses = {
    'welcome': [
        "नमस्ते! 👋 मैं आपकी स्वास्थ्य समस्याओं में मदद कर सकता हूँ।",
        "हैलो! 🩺 मैं आपके स्वास्थ्य संबंधी प्रश्नों का उत्तर दे सकता हूँ।",
        "आपका स्वागत है! 🌿 कृपया अपनी स्वास्थ्य समस्या चुनें।"
    ],
    'select_category': "कृपया नीचे से अपनी समस्या की श्रेणी चुनें:",
    'select_disease': "अब कृपया अपना विशिष्ट लक्षण/समस्या चुनें:",
    'thanks': "आपको शीघ्र स्वस्थ होने की कामना करता हूँ! 🙏",
    'ask_more': "क्या आप किसी अन्य समस्या के बारे में जानना चाहते हैं?",
    'goodbye': "धन्यवाद! अच्छा स्वास्थ्य बनाए रखें। 🌟 हमेशा खुश रहें!",
    'help': "मैं आपकी कैसे मदद कर सकता हूँ? नीचे दिए गए विकल्पों में से चुनें।"
}

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
    st.session_state.step = 'welcome'
    st.session_state.category = None
    st.session_state.symptom = None
    st.session_state.show_help = False

# Helper functions
def get_categories():
    return sorted(df['Category'].unique().tolist())

def get_symptoms(category):
    return df[df['Category'] == category]['Symptom'].unique().tolist()

def get_treatment(category, symptom):
    result = df[(df['Category'] == category) & (df['Symptom'] == symptom)]
    return result.iloc[0] if not result.empty else None

def format_treatment(info):
    return f"""
    <div style='background:#f5fbf6;padding:15px;border-radius:10px;margin:10px 0;border-left:5px solid #4CAF50;box-shadow:0 2px 8px rgba(0,0,0,0.1)'>
        <h3 style='color:#2e7d32;border-bottom:1px solid #e0e0e0;padding-bottom:8px'>🩺 {info['Symptom']}</h3>
        <p><b>🔍 कारण:</b> {info['Cause']}</p>
        <p><b>💊 दवाएँ:</b> {info['Medicines (Indian)']}</p>
        <p><b>🏠 घरेलू उपाय:</b> {info['Home Remedies']}</p>
        <p><b>⚠️ सावधानियाँ:</b> {info['Precautions']}</p>
        <p><b>ℹ️ विवरण:</b> {info['Hindi Explanation']}</p>
    </div>
    """

def add_message(role, content, is_html=False):
    st.session_state.conversation.append({"role": role, "content": content, "is_html": is_html})

def reset_conversation():
    st.session_state.conversation = []
    st.session_state.step = 'welcome'
    st.session_state.category = None
    st.session_state.symptom = None
    st.session_state.show_help = False
    welcome_msg = random.choice(responses['welcome'])
    add_message("assistant", welcome_msg)
    add_message("assistant", responses['select_category'])

# App UI
st.set_page_config(page_title="स्वास्थ्य सहायक", page_icon="🌿", layout="wide")

# Custom CSS
st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #f9f9f9;
    }
    
    /* Chat messages */
    .stChatMessage {
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 8px;
        max-width: 85%;
    }
    
    .stChatMessage.user {
        background-color: #e3f2fd;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }
    
    .stChatMessage.assistant {
        background-color: #f1f8e9;
        margin-right: auto;
        border-bottom-left-radius: 4px;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        margin: 5px 0;
        text-align: left;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        transition: all 0.3s;
        background-color: white;
    }
    
    .stButton>button:hover {
        background-color: #f0f4ff;
        border-color: #4CAF50;
        transform: translateY(-2px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Header */
    .header {
        background: linear-gradient(135deg, #4CAF50, #2E7D32);
        color: white;
        padding: 1.5rem;
        border-radius: 0 0 12px 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Info cards */
    .info-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #4CAF50;
    }
    
    /* Responsive columns */
    @media (max-width: 768px) {
        .column {
            width: 100% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1 style="color:white;margin:0;">🌿 स्वास्थ्य सहायक चैटबॉट</h1>
    <p style="color:white;margin:0;opacity:0.8;">आपका व्यक्तिगत स्वास्थ्य सहायक</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;margin-bottom:20px;">
        <h3>🩺 स्वास्थ्य सहायक</h3>
        <p>आपकी सामान्य स्वास्थ्य समस्याओं का समाधान</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 नया चैट शुरू करें", use_container_width=True):
        reset_conversation()
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div class="info-card">
        <h4>ℹ️ चैटबॉट के बारे में</h4>
        <p>यह चैटबॉट सामान्य स्वास्थ्य समस्याओं के बारे में जानकारी प्रदान करता है।</p>
        <p>कृपया ध्यान दें: यह पेशेवर चिकित्सा सलाह का विकल्प नहीं है।</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align:center;margin-top:20px;font-size:0.8em;color:#666;">
        <p>© 2025 स्वास्थ्य सहायक</p>
    </div>
    """, unsafe_allow_html=True)

# Initial greeting
if st.session_state.step == 'welcome' and not st.session_state.conversation:
    welcome_msg = random.choice(responses['welcome'])
    add_message("assistant", welcome_msg)
    add_message("assistant", responses['select_category'])
    st.session_state.step = 'category_selection'
    st.rerun()

# Display conversation
for i, msg in enumerate(st.session_state.conversation):
    if msg["role"] == "user":
        message(msg["content"], is_user=True, key=f"user_{i}")
    else:
        if msg.get("is_html", False):
            st.markdown(msg["content"], unsafe_allow_html=True)
        else:
            message(msg["content"], key=f"assistant_{i}")

# Category selection
if st.session_state.step == 'category_selection':
    st.markdown(f"**{responses['select_category']}**")
    cols = st.columns(2)
    categories = get_categories()
    
    for i, category in enumerate(categories):
        with cols[i%2]:
            if st.button(f"📁 {category}", key=f"cat_{i}"):
                st.session_state.category = category
                add_message("user", f"श्रेणी: {category}")
                add_message("assistant", f"आपने चुना: {category}")
                add_message("assistant", responses['select_disease'])
                st.session_state.step = 'symptom_selection'
                st.rerun()

# Symptom selection
elif st.session_state.step == 'symptom_selection':
    st.markdown(f"**{responses['select_disease']}**")
    symptoms = get_symptoms(st.session_state.category)
    cols = st.columns(2)
    
    for i, symptom in enumerate(symptoms):
        with cols[i%2]:
            if st.button(f"🔍 {symptom}", key=f"symp_{i}"):
                st.session_state.symptom = symptom
                add_message("user", f"लक्षण: {symptom}")
                treatment = get_treatment(st.session_state.category, symptom)
                if treatment is not None:
                    add_message("assistant", format_treatment(treatment), is_html=True)
                    add_message("assistant", responses['thanks'])
                    add_message("assistant", responses['ask_more'])
                    st.session_state.step = 'restart'
                    st.rerun()

# Restart conversation
elif st.session_state.step == 'restart':
    st.markdown("**क्या आप किसी अन्य समस्या के बारे में जानना चाहते हैं?**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ हाँ, नई समस्या पूछें", key="yes_new"):
            add_message("user", "हाँ, नई समस्या पूछें")
            add_message("assistant", responses['select_category'])
            st.session_state.step = 'category_selection'
            st.session_state.category = None
            st.session_state.symptom = None
            st.rerun()
    with col2:
        if st.button("❌ नहीं, चैट समाप्त करें", key="no_end"):
            add_message("user", "नहीं, चैट समाप्त करें")
            add_message("assistant", responses['goodbye'])
            st.session_state.step = 'end'
            st.rerun()

# End state
elif st.session_state.step == 'end':
    if st.button("🔄 नया चैट शुरू करें", key="restart_end"):
        reset_conversation()
        st.rerun()

# Add some empty space at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)
