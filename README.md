# Cotton Therapy Bot MVP

An empathetic therapy chatbot with voice capabilities and appointment booking functionality, powered by Google's Gemini AI.

## Features

- **Empathetic Conversations**: Uses Gemini 1.5 for natural, supportive responses
- **Voice Interaction**: Speak with the bot and hear its responses
- **Text Mode**: Traditional text-based chat interface
- **Appointment Booking**: Mock functionality to book sessions with human therapists

## Setup Instructions

### 1. Environment Setup

```bash
# Navigate to the project directory
cd therapy_bot_mvp

# (Optional) Create and activate a virtual environment
python -m venv venv

# On Windows
.\\venv\\Scripts\\activate

# On macOS/Linux
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

Create a file named `.env` in the project directory with the following content:

```env
GOOGLE_API_KEY=your_api_key_here
MODEL_NAME=gemini-1.5-flash-8b-latest
```

You can get an API key from [Google AI Studio](https://ai.google.dev/).

### 3. Verify API Connection (optional quick check)

You can do a quick smoke test by running the CLI app and sending a simple prompt (see below). If you get a response, your API key is set correctly.

## Running the Application

### Option A: Streamlit UI

```bash
streamlit run app.py
```

- Type your messages and press Enter to chat in text mode
- Toggle "Enable Voice Output" in the sidebar to hear responses
- Type messages like "Book an appointment with Dr. Smith at 5pm" to trigger the booking tool

### Option B: CLI Chatbot

```bash
python main.py
```

- Type 'voice' to switch to voice input mode (requires working microphone and PyAudio)
- Type 'text' to switch back to text input mode
- Type 'exit' to quit the application

## Component Testing

Test individual components:

```bash
# Test voice input/output (requires microphone and system audio)
python voice_io.py

# Test appointment booking tool-calls
python booking.py
```

## Project Structure

- `main.py`: CLI application entry point
- `app.py`: Streamlit UI application entry point
- `voice_io.py`: Voice input/output functionality
- `booking.py`: Appointment booking tool schema and utilities

## Notes

- If you encounter PyAudio installation issues on Windows and only need text chat and TTS, you can skip voice input tests. Streamlit voice output (gTTS) does not require PyAudio.
- Ensure your system can play MP3 files from the default handler for TTS playback.

## Future Enhancements

- Fine-tune on therapy datasets
- Integrate with real calendar APIs (e.g., Calendly)
- Add Twilio integration for phone calls
- Implement user authentication and session history