import streamlit as st
import pandas as pd
import random

# डेटासेट लोड करें
@st.cache_data
def load_data():
    return pd.read_csv('common_diseases_expanded.csv')

df = load_data()

# हिंदी प्रतिक्रियाएं
responses = {
    'welcome': [
        "नमस्ते! मैं आपकी स्वास्थ्य समस्याओं में मदद कर सकता हूँ।",
        "हैलो! मैं आपके स्वास्थ्य संबंधी प्रश्नों का उत्तर दे सकता हूँ।",
        "आपका स्वागत है! कृपया अपनी स्वास्थ्य समस्या चुनें।"
    ],
    'select_category': "कृपया अपनी समस्या की श्रेणी चुनें:",
    'select_disease': "कृपया अपना लक्षण/समस्या चुनें:",
    'thanks': "आपको शीघ्र स्वस्थ होने की कामना करता हूँ!",
    'ask_more': "क्या आप किसी अन्य समस्या के बारे में जानना चाहते हैं?"
}

# सेशन स्टेट इनिशियलाइज़ करें
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
    st.session_state.step = 'welcome'
    st.session_state.category = None
    st.session_state.symptom = None

# हेल्पर फंक्शन्स
def get_categories():
    return sorted(df['Category'].unique().tolist())

def get_symptoms(category):
    return df[df['Category'] == category]['Symptom'].unique().tolist()

def get_treatment(category, symptom):
    result = df[(df['Category'] == category) & (df['Symptom'] == symptom)]
    return result.iloc[0] if not result.empty else None

def format_treatment(info):
    return f"""
    <div style='background:#f8f9fa;padding:15px;border-radius:10px;margin:10px 0;border-left:5px solid #4CAF50'>
        <h3 style='color:#2e7d32'>{info['Symptom']}</h3>
        <p><b>🗨️ कारण:</b> {info['Cause']}</p>
        <p><b>💊 दवाएँ:</b> {info['Medicines (Indian)']}</p>
        <p><b>🏠 घरेलू उपाय:</b> {info['Home Remedies']}</p>
        <p><b>⚠️ सावधानियाँ:</b> {info['Precautions']}</p>
        <p><b>ℹ️ विवरण:</b> {info['Hindi Explanation']}</p>
    </div>
    """

def add_message(role, content):
    st.session_state.conversation.append({"role": role, "content": content})

# ऐप UI
st.title("🌿 स्वास्थ्य सहायक चैटबॉट")
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        margin: 5px 0;
        text-align: left;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #f0f0f0;
        border-color: #4CAF50;
    }
    [data-testid="stMarkdownContainer"] p { margin: 0.5em 0; }
    .stChatMessage { padding: 12px 16px; }
</style>
""", unsafe_allow_html=True)

# कन्वर्सेशन डिस्प्ले
for msg in st.session_state.conversation:
    with st.chat_message(msg["role"]):
        if '<div' in msg["content"]:
            st.markdown(msg["content"], unsafe_allow_html=True)
        else:
            st.markdown(msg["content"])

# इनिशियल ग्रीटिंग
if st.session_state.step == 'welcome' and not st.session_state.conversation:
    welcome_msg = random.choice(responses['welcome'])
    add_message("assistant", welcome_msg)
    add_message("assistant", responses['select_category'])
    st.session_state.step = 'category_selection'
    st.rerun()

# कैटेगरी सिलेक्शन बटन
if st.session_state.step == 'category_selection':
    cols = st.columns(2)
    for i, category in enumerate(get_categories()):
        with cols[i%2]:
            if st.button(f"📁 {category}"):
                st.session_state.category = category
                add_message("user", f"श्रेणी: {category}")
                add_message("assistant", f"आपने चुना: {category}")
                add_message("assistant", responses['select_disease'])
                st.session_state.step = 'symptom_selection'
                st.rerun()

# सिम्पटम सिलेक्शन बटन
elif st.session_state.step == 'symptom_selection':
    symptoms = get_symptoms(st.session_state.category)
    cols = st.columns(2)
    for i, symptom in enumerate(symptoms):
        with cols[i%2]:
            if st.button(f"🔍 {symptom}"):
                st.session_state.symptom = symptom
                add_message("user", f"लक्षण: {symptom}")
                treatment = get_treatment(st.session_state.category, symptom)
                if treatment is not None:
                    add_message("assistant", format_treatment(treatment))
                    add_message("assistant", responses['thanks'])
                    add_message("assistant", responses['ask_more'])
                    st.session_state.step = 'restart'
                    st.rerun()

# रीस्टार्ट कन्वर्सेशन बटन
elif st.session_state.step == 'restart':
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ हाँ (किसी अन्य समस्या के बारे में पूछें)"):
            add_message("user", "हाँ")
            add_message("assistant", responses['select_category'])
            st.session_state.step = 'category_selection'
            st.session_state.category = None
            st.session_state.symptom = None
            st.rerun()
    with col2:
        if st.button("❌ नहीं (चैट समाप्त करें)"):
            add_message("user", "नहीं")
            add_message("assistant", "धन्यवाद! अच्छा स्वास्थ्य बनाए रखें। 🙏")
            st.session_state.step = 'end'
            st.rerun()