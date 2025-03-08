from models import instruction_prompts, model_maker


class translator_model():
    def __init__(self):
        self.instructions = instruction_prompts.Instrucsion_for_translator
        self.api_key = "AIzaSyCEykNXCTFGrESKB8iF_dwjG4tSoYstQQM"
        self.model = model_maker.Gemini_Chat(self.instructions,self.api_key)
        self.response_status = {"status": 1, "message": ""}


    #if there is no problem with the message the message will be sent in the dict
    def translation_procces(self,text) -> str:
        response = self.model.send(text)
        self.resp_check(response.text)
        return self.response_status
        
    def resp_check(self,response) -> dict:
        """Validates the response and checks for errors."""
        self.response_status["message"] = response.strip() #if there no problems the response will be sent back
        self.response_status["status"] = 1 # start from true

        if not response:
            self.response_status["message"] = "Error: Empty response from translator model."
            self.response_status["status"] = 0

        elif response == "Fjson":
            self.response_status["message"] = "translator model: problem with json stuff"
            self.response_status["status"] = 0

