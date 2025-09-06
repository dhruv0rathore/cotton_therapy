# Function calling for appointment booking

# Define the tool schema for appointment booking
import google.generativeai as genai

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

# Function to handle tool calls in the response
def handle_tool_calls(response, prompt):
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
                        
                        # Return the booking confirmation
                        return result
    
    # If no tool call, return None
    return None

# Test function
def test_booking():
    import google.generativeai as genai
    import os
    from dotenv import load_dotenv
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Configure API key
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        return
    
    # Remove quotes if they exist in the API key
    api_key = api_key.strip("'\"")
    
    genai.configure(api_key=api_key)
    
    # Initialize the model - use the flagship model
    model = genai.GenerativeModel('gemini-1.5-flash-8b-latest')
    
    # Test booking functionality
    print("=== Testing Appointment Booking ===\n")
    
    # Test prompt that should trigger booking
    prompt = "I'm feeling anxious and would like to book a session with a therapist."
    
    print(f"User: {prompt}")
    
    # Generate response with tools enabled
    response = model.generate_content(
        f"You're an empathetic therapist. Respond to: '{prompt}'. If the user wants to book a session, use the book_appointment function.",
        tools=tools,
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 1024
        }
    )
    
    # Check for tool calls
    booking_result = handle_tool_calls(response, prompt)
    
    if booking_result:
        print(f"\nBooking successful: {booking_result}")
    else:
        print(f"\nBot response: {response.text}")
        print("\nNo booking was made. The model didn't trigger the booking function.")

if __name__ == "__main__":
    test_booking()