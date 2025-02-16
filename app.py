# Med Buddy hospital stay Ai assistant for CodeBlue team, MedHack 2025 challenge

import streamlit as st
import os
import json
from utils import load_patient_data, get_ai_response, get_patient_name

# Theme handling
def load_theme():
    try:
        with open('config/theme.json', 'r') as f:
            return json.load(f)
    except:
        return {
            "theme": "Dark Mode",
            "settings": {
                "background": "linear-gradient(to bottom right, #1a1a2e, #16213e)",
                "text": "#e2e2e2"
            }
        }

# Apply theme
theme = load_theme()
st.markdown(f"""
<style>
    .stApp {{
        background: {theme['settings']['background']};
        color: {theme['settings']['text']};
    }}
</style>
""", unsafe_allow_html=True)

# Initialize session states
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'notes' not in st.session_state:
    st.session_state.notes = ""

# Page configuration
st.set_page_config(
    page_title="Hospital Buddy",
    page_icon="🏥",
    layout="wide"
)

# Header
st.title("🏥 Hospital Buddy")
if 'patient_data' in st.session_state and st.session_state.patient_data:
    patient_name = get_patient_name(st.session_state.patient_data)
    st.markdown(f"### Welcome back {patient_name}")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Your Medical Dashboard")
    
    # Patient File Selection
    data_files = os.listdir('data') if os.path.exists('data') else []
    selected_file = st.selectbox(
        "Select patient file:",
        data_files if data_files else ["No data files found"]
    )

    if selected_file and selected_file != "No data files found":
        patient_data = load_patient_data(os.path.join('data', selected_file))
        st.session_state.patient_data = patient_data
        
        # Medical Information
        st.text_area(
            "Medical Information:",
            patient_data,
            height=400,
            key="patient_data_preview"
        )
        
        # Personal Notes Section
        st.header("Personal Notes")
        st.session_state.notes = st.text_area(
            "Your Notes",
            st.session_state.notes,
            height=200,
            key="personal_notes"
        )
        
        # Medications Section
        st.header("Prescribed Medications")
        try:
            meds_start = patient_data.index("Medications:")
            meds_end = patient_data.index("Other Treatments:")
            medications = patient_data[meds_start:meds_end].strip()
            st.text_area(
                "Current Medications",
                medications,
                height=300,
                key="medications_view"
            )
        except:
            st.warning("No medication information found")
    else:
        patient_data = None
        st.error("Please add patient data files to the 'data' folder.")

# Chat interface
st.container()
for message in st.session_state.messages:
    with st.container():
        st.markdown(f"""
        <div class="chat-message {'user-message' if message['role'] == 'user' else 'assistant-message'}">
            <b>{'You' if message['role'] == 'user' else '🤖 Assistant'}:</b><br>{message['content']}
        </div>
        """, unsafe_allow_html=True)

# User input
if patient_data:
    with st.form(key='message_form', clear_on_submit=True):
        user_input = st.text_input("Ask about your hospital stay:", key="user_input")
        col1, col2 = st.columns([1, 5])
        with col1:
            submit_button = st.form_submit_button("Send")
        with col2:
            if submit_button:
                with st.spinner('Thinking... 🤔'):
                    if user_input and (not st.session_state.messages or st.session_state.messages[-1]['content'] != user_input):
                        st.session_state.messages.append({"role": "user", "content": user_input})
                        response = get_ai_response(patient_data, user_input)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
else:
    st.warning("Please select a patient data file to start the conversation.")

# Footer
st.markdown("---")
st.markdown("*This AI assistant provides information based on your medical records. For emergencies, please contact your healthcare provider directly.*") 
