def get_theme_css(theme_settings):
    return f"""
<style>
    /* Main app styling */
    .stApp {{
        background: {theme_settings['background']};
        color: {theme_settings['text']};
    }}
    
    /* Header styling */
    .stTitle {{
        color: #4fd1c5;
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: rgba(22, 33, 62, 0.8);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }}
    
    /* Input field styling */
    .stTextInput > div > div > input {{
        background-color: rgba(255, 255, 255, 0.05);
        color: {theme_settings['text']};
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 15px;
        font-size: 16px;
    }}
    
    /* Chat message containers */
    .chat-message {{
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        animation: fadeIn 0.5s ease-out;
    }}
    
    /* User message styling */
    .user-message {{
        background: rgba(79, 209, 197, 0.1);
        margin-left: 20%;
        border-bottom-right-radius: 5px;
    }}
    
    /* Assistant message styling */
    .assistant-message {{
        background: rgba(255, 255, 255, 0.05);
        margin-right: 20%;
        border-bottom-left-radius: 5px;
    }}
    
    /* Button styling */
    .stButton > button {{
        background: linear-gradient(45deg, #4fd1c5, #38b2ac);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}
    
    /* Form container */
    [data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }}
    
    /* Animation keyframes */
    @keyframes fadeIn {{
        from {{
            opacity: 0;
            transform: translateY(10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
</style>
""" 
