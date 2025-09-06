import streamlit as st
import os
import time
import google.generativeai as genai
from voice_io import speak_response
from booking import tools, handle_tool_calls
from dotenv import load_dotenv

# Page configuration
st.set_page_config(
    page_title="Cotton Therapy",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load environment variables from .env file
load_dotenv()

# Configure API key
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    st.error("GOOGLE_API_KEY is not set. Please add it to your .env file in the project directory.")
    st.stop()

# Configure the API
genai.configure(api_key=api_key)

# Initialize the model
model_name = os.environ.get("MODEL_NAME", "gemini-1.5-flash-8b-latest")
model = genai.GenerativeModel(model_name)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #4CAF50;
    text-align: center;
    margin-bottom: 1rem;
}
.sub-header {
    font-size: 1.2rem;
    color: #555;
    text-align: center;
    margin-bottom: 2rem;
    font-style: italic;
}
/* Chat bubbles - ensure strong contrast on both themes */
.user-bubble,
.bot-bubble {
    padding: 12px 16px;
    margin: 8px 0;
    display: inline-block;
    max-width: 80%;
    line-height: 1.4;
    font-size: 1rem;
    font-weight: 500;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.user-bubble {
    background-color: #E6F4EA; /* slightly deeper than before */
    color: #0B2E13; /* dark text for contrast */
    border-radius: 20px 20px 5px 20px;
}

.bot-bubble {
    background-color: #EDEFF2; /* slightly deeper than before */
    color: #0F172A; /* dark slate text for contrast */
    border-radius: 20px 20px 20px 5px;
}

/* Adapt for dark theme */
@media (prefers-color-scheme: dark) {
  .user-bubble {
    background-color: #1F3B2A; /* darker green tint */
    color: #E6FFEE; /* light text */
  }
  .bot-bubble {
    background-color: #2A2F3A; /* dark slate */
    color: #F8FAFC; /* light text */
  }
}
</style>
""", unsafe_allow_html=True)

# Function to generate empathetic responses
def generate_empathetic_response(user_input):
    prompt = f"""You're an empathetic therapist named Cotton. Respond supportively to: '{user_input}'. 
    Be warm, understanding, and compassionate. Use a conversational tone and keep responses concise.
    If the user expresses interest in booking a session with a human therapist, offer to help them book an appointment."""
    
    # Generate response with tools enabled
    response = model.generate_content(
        prompt,
        tools=tools,
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 1024
        }
    )
    
    # Check if there's a tool call in the response
    booking_result = handle_tool_calls(response, prompt)
    
    if booking_result:
        # Generate a final response that includes the booking confirmation
        final_prompt = f"{prompt}\n\nThe appointment has been booked: {booking_result}"
        final_response = model.generate_content(final_prompt)
        return final_response.text
    
    # If no tool call, return the regular response
    return response.text

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    welcome_message = "Hey, I'm Cotton, your therapy companion. Feel free to spill your thoughts, and I'm here to listen and support you."
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

# Display header
st.markdown('<h1 class="main-header">Cotton Therapy</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your AI therapy companion</p>', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div style="display: flex; justify-content: flex-end;"><div class="user-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="display: flex; justify-content: flex-start;"><div class="bot-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)

# Voice mode toggle
voice_mode = st.sidebar.checkbox("Enable Voice Output", value=False)

# User input
user_input = st.chat_input("Type your message here...")

# Process user input
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    st.markdown(f'<div style="display: flex; justify-content: flex-end;"><div class="user-bubble">{user_input}</div></div>', unsafe_allow_html=True)
    
    # Generate bot response
    with st.spinner("Cotton is thinking..."):
        bot_response = generate_empathetic_response(user_input)
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    
    # Display bot response
    st.markdown(f'<div style="display: flex; justify-content: flex-start;"><div class="bot-bubble">{bot_response}</div></div>', unsafe_allow_html=True)
    
    # Speak response if voice mode is enabled
    if voice_mode:
        speak_response(bot_response)

# Sidebar information
with st.sidebar:
    st.header("About Cotton Therapy")
    st.write("Cotton is an AI therapy companion designed to provide empathetic support and a listening ear.")
    st.write("**Note:** This is not a replacement for professional mental health services.")
    
    st.header("Features")
    st.write("- Text-based chat interface")
    st.write("- Voice output capability")
    st.write("- Appointment booking with human therapists")
    
    st.header("Using Voice Mode")
    st.write("Enable the 'Voice Output' option to have Cotton speak responses aloud.")