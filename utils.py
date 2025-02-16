import os
from openai import OpenAI
import logging
import streamlit as st
from config import SYSTEM_PROMPT

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

__all__ = ['load_patient_data', 'get_ai_response', 'get_patient_name']

def get_patient_name(patient_data):
    """Extract patient's first name from data"""
    try:
        for line in patient_data.split('\n'):
            if line.startswith('First Name:'):
                return line.split(':')[1].strip()
    except:
        return "Patient"  # Default fallback
    return "Patient"  # Default fallback

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
        
        # Load hospital information
        hospital_info = load_patient_data('data/hospital.txt')
        
        # Create OpenAI client
        client = OpenAI(
            api_key=api_key,
            timeout=60.0
        )
        
        # Prepare messages using system prompt from config
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"Hospital Information: {hospital_info}\n\nPatient Data: {patient_data}\n\nUser Question: {user_query}"
            }
        ]
        
        # Make API call
        try:
            completion = client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=messages,
                temperature=0.1,
                max_tokens=500
            )
            
            return completion.choices[0].message.content
            
        except Exception as api_error:
            st.error(f"OpenAI API Error: {str(api_error)}")
            return f"API Error: {str(api_error)}"
            
    except Exception as e:
        st.error(f"General Error: {str(e)}")
        return f"Error: {str(e)}" 
