import streamlit as st
import os
from utils import load_patient_data, get_ai_response

# Page configuration
st.set_page_config(
    page_title="Medical Assistant AI",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Main app background and text */
    .stApp {
        background: linear-gradient(to bottom right, #1a1a2e, #16213e);
        color: #e2e2e2;
    }
    
    /* Header styling */
    .stTitle {
        color: #4fd1c5;
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: rgba(22, 33, 62, 0.8);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 15px;
        font-size: 16px;
    }
    
    /* Chat message containers */
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        animation: fadeIn 0.5s ease-out;
    }
    
    /* User message styling */
    .user-message {
        background: rgba(79, 209, 197, 0.1);
        margin-left: 20%;
        border-bottom-right-radius: 5px;
    }
    
    /* Assistant message styling */
    .assistant-message {
        background: rgba(255, 255, 255, 0.05);
        margin-right: 20%;
        border-bottom-left-radius: 5px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #4fd1c5, #38b2ac);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
    }
    
    /* Animation keyframes */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Divider styling */
    hr {
        border-color: rgba(255,255,255,0.1);
    }
    
    /* Form container */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Warning/Error messages */
    .stAlert {
        background: rgba(255, 99, 71, 0.1);
        color: #ff6347;
        border: 1px solid rgba(255, 99, 71, 0.2);
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Header
st.title("🏥 Medical Assistant AI")
st.markdown("---")

# Sidebar for patient data selection
with st.sidebar:
    st.header("Patient Data")
    data_files = os.listdir('data') if os.path.exists('data') else []
    selected_file = st.selectbox(
        "Select patient data file:",
        data_files if data_files else ["No data files found"]
    )

    if selected_file and selected_file != "No data files found":
        patient_data = load_patient_data(os.path.join('data', selected_file))
        st.text_area("Patient Data Preview:", patient_data[:200] + "...", height=150)
    else:
        patient_data = None
        st.error("Please add patient data files to the 'data' folder.")

# Chat interface
st.container()
# Display chat messages
for message in st.session_state.messages:
    with st.container():
        st.markdown(f"""
        <div class="chat-message {'user-message' if message['role'] == 'user' else 'assistant-message'}">
            <b>{'You' if message['role'] == 'user' else '🤖 Assistant'}:</b><br>{message['content']}
        </div>
        """, unsafe_allow_html=True)

# User input
if patient_data:
    # Create a form to handle the input
    with st.form(key='message_form', clear_on_submit=True):
        user_input = st.text_input("Ask about your hospital stay:", key="user_input")
        submit_button = st.form_submit_button("Send")
    
    # Only process if the form is submitted and there's input
    if submit_button and user_input:
        # Prevent duplicate messages
        if not st.session_state.messages or st.session_state.messages[-1]['content'] != user_input:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get AI response
            response = get_ai_response(patient_data, user_input)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Rerun to update chat display
            st.experimental_rerun()

    # Clear chat button (outside the form)
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()
else:
    st.warning("Please select a patient data file to start the conversation.")

# Footer
st.markdown("---")
st.markdown("*This AI assistant provides information based on your medical records. For emergencies, please contact your healthcare provider directly.*") 