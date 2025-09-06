# Cotton Therapy Bot MVP

An empathetic therapy chatbot with voice capabilities and appointment booking functionality, powered by Google's Gemini AI.

## Features

- **Empathetic Conversations**: Uses Gemini 1.5 Pro for natural, supportive responses
- **Voice Interaction**: Speak with the bot and hear its responses
- **Text Mode**: Traditional text-based chat interface
- **Appointment Booking**: Mock functionality to book sessions with human therapists

## Setup Instructions

### 1. Environment Setup

```bash
# Clone the repository (if applicable)
# git clone <repository-url>

# Navigate to the project directory
cd therapy_bot_mvp

# Create and activate a virtual environment
python -m venv venv

# On Windows
.\venv\Scripts\activate

# On macOS/Linux
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. API Key Setup

1. Get a Google AI API key from [Google AI Studio](https://ai.google.dev/)
2. Run the API key setup script:

```bash
python setup_api_key.py
```

Follow the prompts to enter your API key. This will create or update the .env file in the parent directory.

Alternatively, you can manually set the environment variable:

```bash
# On Windows
set GOOGLE_API_KEY=your_api_key_here

# On macOS/Linux
# export GOOGLE_API_KEY=your_api_key_here
```

### 3. Test API Connection

Before running the full application, test your API connection:

```bash
python test_api.py
```

## Running the Application

```bash
python main.py
```

## Usage

- Type your messages and press Enter to chat in text mode
- Type 'voice' to switch to voice input mode
- Type 'text' to switch back to text mode
- Type 'exit' to quit the application

## Component Testing

Test individual components:

```bash
# Test voice input/output
python voice_io.py

# Test appointment booking
python booking.py
```

## Project Structure

- `main.py`: Main application entry point
- `bot.py`: Core chatbot logic (alternative entry point)
- `voice_io.py`: Voice input/output functionality
- `booking.py`: Appointment booking functionality
- `test_api.py`: API connection test

## Future Enhancements

- Fine-tune on therapy datasets
- Integrate with real calendar APIs (e.g., Calendly)
- Add Twilio integration for phone calls
- Implement user authentication and session history