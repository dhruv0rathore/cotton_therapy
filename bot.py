import os
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import platform
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="../.env")

# Configure API key
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it with your Google AI API key.")

# Remove quotes if they exist in the API key
api_key = api_key.strip("'\"")

genai.configure(api_key=api_key)

# Initialize the model - use the flagship model
model = genai.GenerativeModel('gemini-1.0-pro')

# Define the tool schema for appointment booking
tools = [
    {
        "function_declarations": [
            {
                "name": "book_appointment",
                "description": "Book a therapy appointment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "therapist_name": {"type": "string", "description": "Name of the therapist"},
                        "time_slot": {"type": "string", "description": "Time slot for the appointment"}
                    },
                    "required": ["therapist_name", "time_slot"]
                }
            }
        ]
    }
]

# Mock function for booking appointments
def book_appointment(therapist_name, time_slot):
    print(f"Booking appointment with {therapist_name} at {time_slot}")
    return f"Successfully booked an appointment with {therapist_name} at {time_slot}. You'll receive a confirmation email shortly."

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
    if hasattr(response, 'candidates') and len(response.candidates) > 0:
        candidate = response.candidates[0]
        if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
            for part in candidate.content.parts:
                if hasattr(part, 'function_call'):
                    # Extract function call parameters
                    function_name = part.function_call.name
                    if function_name == "book_appointment":
                        args = part.function_call.args
                        therapist_name = args.get("therapist_name", "")
                        time_slot = args.get("time_slot", "")
                        
                        # Call the booking function
                        result = book_appointment(therapist_name, time_slot)
                        
                        # Generate a final response that includes the booking confirmation
                        final_prompt = f"{prompt}\n\nThe appointment has been booked: {result}"
                        final_response = model.generate_content(final_prompt)
                        return final_response.text
    
    # If no tool call, return the regular response
    return response.text

# Function to listen to user's voice input
def listen_to_user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError:
        print("Could not request results from speech recognition service.")
        return ""

# Function to speak the bot's response
def speak_response(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    
    # Play the audio file based on the operating system
    if platform.system() == "Darwin":  # macOS
        os.system("afplay response.mp3")
    elif platform.system() == "Linux":
        os.system("mpg123 response.mp3")
    else:  # Windows
        os.system("start response.mp3")

# Main function to run the chatbot
def main():
    print("=== Cotton Therapy Bot ===")
    print("Type 'exit' to quit or 'voice' to switch to voice input mode")
    
    mode = "text"  # Default mode is text input
    
    # Welcome message
    welcome_message = "Hey, I'm Cotton, your therapy companion. Feel free to spill your thoughts, and I'm here to listen and support you."
    print(f"Bot: {welcome_message}")
    speak_response(welcome_message)
    
    while True:
        if mode == "text":
            user_input = input("You: ")
            
            if user_input.lower() == "exit":
                print("Bot: Take care! Remember I'm here whenever you need to talk.")
                break
            elif user_input.lower() == "voice":
                mode = "voice"
                print("Bot: Switching to voice input mode. Speak clearly into your microphone.")
                continue
        else:  # voice mode
            user_input = listen_to_user()
            
            if user_input.lower() == "exit":
                print("Bot: Take care! Remember I'm here whenever you need to talk.")
                break
            elif user_input.lower() == "text":
                mode = "text"
                print("Bot: Switching to text input mode.")
                continue
            elif not user_input:  # If speech recognition failed
                continue
        
        # Generate response
        bot_response = generate_empathetic_response(user_input)
        print(f"Bot: {bot_response}")
        
        # Speak the response
        speak_response(bot_response)
        
        # Add a small delay for natural conversation flow
        time.sleep(1)

if __name__ == "__main__":
    main()