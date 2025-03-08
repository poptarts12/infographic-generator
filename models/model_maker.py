import google.generativeai as genai
import json

class Gemini_Chat:
    def __init__(self, instruction_prompt, API_key):
        """Initializes the Gemini Chat session and loads configurations."""
        # Configure API
        genai.configure(api_key=API_key)

        # Model configuration
        generation_config = {
            "temperature": 0,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        # Initialize the model with system instructions
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=generation_config,
            system_instruction=instruction_prompt,  # Sent ONCE
        )

        # Create a persistent chat session
        self.chat_session = self.model.start_chat(history=[])

    def send(self, text):
        """Processes a new message while keeping the chat session active."""
        response = self.chat_session.send_message(text)
        
        return response

    def json_checker(text):
        # Try parsing JSON output from Gemini (assuming it's structured)
        try:
            parsed_data = json.loads(text)
            return text
        except json.JSONDecodeError:
            print(f"Warning: Could not parse response as JSON. Raw response:\n{text}")
            return "Fjson"  # Return as plain text if not JSON


