# Cotton Therapy — AI Therapy Companion

**Live App Deployed on Streamlit:** [https://cottontherapy0.streamlit.app/](https://cottontherapy0.streamlit.app/)

## Overview

Cotton Therapy is an empathetic therapy companion that supports reflective conversations, offers optional voice responses, and can mock-book sessions with a human therapist via function calling. It is powered by Google’s Gemini models.

## Features

  * **Empathetic Chat:** Supportive, concise responses designed for active listening.
  * **Voice Output:** Toggle on to hear responses via text-to-speech (gTTS).
  * **Mock Booking:** The model can trigger a `book_appointment` tool to simulate scheduling with a therapist.
  * **Dual UX:** Streamlit web app and a CLI (optional) for local chats.

## Architecture

  * `app.py` — Streamlit UI and chat flow with optional voice output.
  * `main.py` — CLI chatbot entry point and shared response generation.
  * `booking.py` — Function-calling tool schema and handler for `book_appointment`.
  * `voice_io.py` — Voice input (microphone) and text-to-speech playback (MP3).
  * `requirements.txt` — Python dependencies.
  * `.env` — Environment configuration (`GOOGLE_API_KEY`, `MODEL_NAME`).

## Quick Start (Local)

### Prerequisites

  * Python 3.10+ recommended.
  * A Google AI API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
  * **Windows note:** Microphone tests may require `PyAudio`. If it's problematic, you can still use the Streamlit app with voice output (no mic needed).

### Steps

1.  **Clone and enter the project**

    ```bash
    git clone https://github.com/dhruv0rathore/cotton_therapy
    cd cotton_therapy
    ```

2.  **Create `.env` file**
    Create a `.env` file in the project root with the following content:

    ```env
    GOOGLE_API_KEY=your_api_key_here
    MODEL_NAME=gemini-1.5-flash-latest
    ```

3.  **Create and use a virtual environment**

    ```bash
    python -m venv venv
    ```

      * **Windows PowerShell:** `.\venv\Scripts\Activate.ps1`
          * If you see an execution policy error, run PowerShell as Admin and execute: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`. Then activate again.
      * **Upgrade pip (recommended):** `python -m pip install --upgrade pip`

4.  **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Streamlit app**

    ```bash
    streamlit run app.py
    ```

      * If you see “Port 8501 is already in use”, run: `streamlit run app.py --server.port 8502`

## How to Use

  * Send a message in the chat box and press Enter.
  * For booking, try: `“Book an appointment with Dr. Smith at 5pm”`.
  * For voice output, toggle the “Enable Voice Output” switch in the sidebar to hear responses.

## Security and Privacy

  * This project is for demonstration and prototyping purposes only.
  * Do not share sensitive personal information.
  * Keep your `GOOGLE_API_KEY` private and never commit it to version control.

## Development Notes

### Consistency

  * All entry points load environment variables via `python-dotenv` and expect `GOOGLE_API_KEY` in the `.env` file.
  * The model name is configurable through the `MODEL_NAME` environment variable (default: `gemini-1.5-flash-latest`).

### Function Calling

  * `booking.py` exposes a tool schema for `book_appointment`.
  * The model may return a tool call; we handle it via `handle_tool_calls()` and stitch the result into the final answer.

### Voice I/O

  * `voice_io.py` uses `gTTS` to generate an MP3 and plays it using the system's default handler.
  * Microphone input relies on `SpeechRecognition` + `PyAudio`. This is optional—text chat and TTS work without it.

## Troubleshooting

  * **Port already in use:** Run `streamlit run app.py --server.port 8502`.
  * **`GOOGLE_API_KEY` missing:** Ensure a `.env` file exists in the root directory with the `GOOGLE_API_KEY` variable set. In Streamlit Cloud, you must set this in the app's Secrets.
  * **`PyAudio` on Windows:** If `PyAudio` installation fails, skip local voice input tests. The Streamlit app's voice output will still function correctly.
  * **Blank or faint chat bubbles:** We enforce high-contrast styles for both light and dark modes. If your browser theme makes bubbles hard to read, perform a hard refresh (Ctrl+F5). If needed, the contrast can be increased further in the CSS styles.

## License

This project is licensed under the MIT License.

## Contributions

Issues and pull requests are welcome. For UI issues, please include steps to reproduce and screenshots.