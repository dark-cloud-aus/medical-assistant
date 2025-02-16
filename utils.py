import os
from openai import OpenAI
import logging
import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_patient_data(file_path):
    """Load patient data from a text file"""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "No patient data found."

def get_ai_response(patient_data, user_query):
    """Get response from OpenAI GPT-4"""
    try:
        # Get API key from Streamlit secrets
        api_key = st.secrets["openai"]["OPENAI_API_KEY"]
        
        # Create OpenAI client
        client = OpenAI(
            api_key=api_key,
            timeout=60.0
        )
        
        # Prepare messages with instruction to not repeat the question
        messages = [
            {
                "role": "system",
                "content": "You are a healthcare assistant, designed to provide simple information to patients. Provide direct answers without repeating the question. Structure your responses under these headings when appropriate: 1) Why am I in hospital? 2) What is happening now? 3) What is going to happen?"
            },
            {
                "role": "user",
                "content": f"Patient Data: {patient_data}\n\nUser Question: {user_query}"
            }
        ]
        
        # Make API call
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return completion.choices[0].message.content
            
        except Exception as api_error:
            st.error(f"OpenAI API Error: {str(api_error)}")
            return f"API Error: {str(api_error)}"
            
    except Exception as e:
        st.error(f"General Error: {str(e)}")
        return f"Error: {str(e)}" 
