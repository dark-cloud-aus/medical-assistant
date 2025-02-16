import streamlit as st
import json
import os

def save_theme(theme_settings):
    """Save theme settings to a JSON file"""
    with open('config/theme.json', 'w') as f:
        json.dump(theme_settings, f)

def load_theme():
    """Load theme settings from JSON file"""
    try:
        with open('config/theme.json', 'r') as f:
            return json.load(f)
    except:
        return {"theme": "dark"}

st.title("⚙️ Settings")

# Theme Settings
st.header("Theme Settings")
themes = {
    "Dark Mode": {
        "background": "linear-gradient(to bottom right, #1a1a2e, #16213e)",
        "text": "#e2e2e2"
    },
    "Light Mode": {
        "background": "linear-gradient(to bottom right, #ffffff, #f0f2f5)",
        "text": "#333333"
    },
    "Soft Pink": {
        "background": "linear-gradient(to bottom right, #fce4ec, #f8bbd0)",
        "text": "#4a4a4a"
    },
    "Ocean Breeze": {
        "background": "linear-gradient(to bottom right, #e0f7fa, #b2ebf2)",
        "text": "#333333"
    },
    "Lavender Dream": {
        "background": "linear-gradient(to bottom right, #f3e5f5, #e1bee7)",
        "text": "#4a4a4a"
    }
}

selected_theme = st.selectbox("Choose your theme", list(themes.keys()))

if st.button("Apply Theme"):
    save_theme({"theme": selected_theme, "settings": themes[selected_theme]})
    st.success("Theme updated! Please refresh the page to see changes.")

# File Upload Section
st.header("File Management")
st.markdown("Upload your medical documents, images, or audio files.")

uploaded_files = st.file_uploader(
    "Upload Files", 
    accept_multiple_files=True,
    type=['pdf', 'png', 'jpg', 'jpeg', 'mp3', 'wav']
)

if uploaded_files:
    for file in uploaded_files:
        # Create data/uploads directory if it doesn't exist
        os.makedirs('data/uploads', exist_ok=True)
        
        # Save the file
        with open(f'data/uploads/{file.name}', 'wb') as f:
            f.write(file.getbuffer())
        st.success(f"Saved: {file.name}") 
