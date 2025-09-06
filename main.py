import os
import time
import google.generativeai as genai
from voice_io import listen_to_user, speak_response
from booking import tools, handle_tool_calls
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure API key
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set. Please add it to your .env file.")

# Configure the API
genai.configure(api_key=api_key)

# Initialize the model
model_name = os.environ.get("MODEL_NAME", "gemini-1.5-flash-8b-latest")  # Get model name from .env or use default
print(f"Using model: {model_name}")
model = genai.GenerativeModel(model_name)

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