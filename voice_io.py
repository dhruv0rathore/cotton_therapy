import speech_recognition as sr
from gtts import gTTS
import os
import platform
import time

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

# Test function
def test_voice_io():
    print("=== Testing Voice I/O ===\n")
    
    # Test text-to-speech
    print("Testing text-to-speech...")
    test_text = "Hello, I'm Cotton, your therapy companion. Can you hear me clearly?"
    speak_response(test_text)
    time.sleep(3)  # Wait for the audio to finish
    
    # Test speech recognition
    print("\nTesting speech recognition...")
    print("Please say something when prompted.")
    time.sleep(1)
    user_input = listen_to_user()
    
    if user_input:
        print("\nSpeech recognition test successful!")
        response = f"I heard you say: {user_input}"
        print(f"Responding with: '{response}'")
        speak_response(response)
    else:
        print("\nSpeech recognition test failed. Please check your microphone settings.")

if __name__ == "__main__":
    test_voice_io()