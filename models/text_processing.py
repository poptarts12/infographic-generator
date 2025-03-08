from models import instruction_prompts, model_maker

class NLP_model():
    def __init__(self):
        self.instructions = instruction_prompts.Instrucsion_for_nlp
        self.api_key = "AIzaSyC2uKvtdzQfw11BZ_9RaNxvmEax71CioxQ"
        self.model = model_maker.Gemini_Chat(self.instructions,self.api_key)
        self.response_status = {"status": 1, "message": ""}


    #if there is no problem with the message the message will be sent in the dict
    def NLP_procces(self,text) -> str:
        response = self.model.send(text)
        self.resp_check(response.text)
        after_check_response = self.response_status
        return after_check_response
        
    def resp_check(self,response) -> dict:
        """Validates the response and checks for errors."""
        self.response_status["message"] = response.strip() #if there no problems the response will be sent back
        self.response_status["status"] = 1 # start from true
        if not self.response_status["message"]:
            self.response_status["message"] = "Error: Empty response from NLP model."
            self.response_status["status"] = 0

        elif self.response_status["message"] == "False":
            self.response_status["message"] = "Client Error: Client is writing but not in Hebrew"
            self.response_status["status"] = 0

        elif self.response_status["message"] == "Information False":
            self.response_status["message"] = "Client Error: The text is in Hebrew but not relevant to the context"
            self.response_status["status"] = 0

        elif self.response_status["message"] == "Fjson":
            self.response_status["message"] = "NLP model: problem with json stuff"
            self.response_status["status"] = 0


