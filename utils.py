import os
from openai import OpenAI
from dotenv import load_dotenv
import logging
import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_openai_client():
    """Initialize and return OpenAI client"""
    try:
        api_key = st.secrets["openai"]["OPENAI_API_KEY"]
        if not api_key:
            logger.error("No API key found in Streamlit secrets")
            raise ValueError("OPENAI_API_KEY not found in Streamlit secrets")
        
        # Log first few characters of API key for debugging
        logger.info(f"Using API key starting with: {api_key[:8]}...")
        
        return OpenAI(api_key=api_key)
    except Exception as e:
        logger.error(f"Error initializing OpenAI client: {str(e)}")
        st.error(f"Failed to initialize OpenAI client: {str(e)}")
        raise

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
        # Initialize client for this request
        client = get_openai_client()
        
        system_prompt = """You are a healthcare assistant, designed to provide simple information to patients with low education or special needs during a hospital stay. Only use the information provided in the patient data to answer questions. If the information is not in the patient data, say you don't have that information. Structure your responses under these headings when appropriate:

1) Why am I in hospital?
2) What is happening now?
3) What is going to happen?"""
        
        try:
            # Log the attempt to call OpenAI
            logger.info("Attempting to call OpenAI API...")
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Patient Data: {patient_data}\n\nUser Question: {user_query}"}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Log successful response
            logger.info("Successfully received response from OpenAI")
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            error_msg = f"Error calling OpenAI API: {str(e)}"
            logger.error(error_msg)
            st.error(error_msg)  # This will show in the UI
            return f"I apologize, but I'm having trouble accessing the AI service. Error: {str(e)}"
            
    except Exception as e:
        error_msg = f"Unexpected error in get_ai_response: {str(e)}"
        logger.error(error_msg)
        st.error(error_msg)  # This will show in the UI
        return "I apologize, but something went wrong. Please check the error message above." 
