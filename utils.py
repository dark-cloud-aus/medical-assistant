import os
from openai import OpenAI
from dotenv import load_dotenv
import logging
import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = st.secrets["openai"]["OPENAI_API_KEY"]
if not api_key:
    logger.error("No API key found in Streamlit secrets")
    raise ValueError("OPENAI_API_KEY not found in Streamlit secrets")

client = OpenAI(api_key=api_key)

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
        # Log API key (first few characters)
        logger.info(f"Using API key: {api_key[:10]}...")
        
        system_prompt = """You are a healthcare assistant, designed to provide simple information to patients with low education or special needs during a hospital stay. Only use the information provided in the patient data to answer questions. If the information is not in the patient data, say you don't have that information. Structure your responses under these headings when appropriate:

1) Why am I in hospital?
2) What is happening now?
3) What is going to happen?"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Patient Data: {patient_data}\n\nUser Question: {user_query}"}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            return f"I apologize, but I'm having trouble accessing the AI service. Please try again in a moment. Error: {str(e)}"
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "I apologize, but something went wrong. Please try again later." 
