from models import text_processing, translation 
from core.infographic_maker import InfographicGenerator
import json
import os
import subprocess



inkscape_path  = r"C:\Program Files\Inkscape\bin\inkscape.exe"

file_path = os.path.dirname(__file__)
class ChatManager:
    def __init__(self):
        # Initialize the models only once at startup
        self.nlp_model = text_processing.NLP_model()
        self.translator = translation.translator_model()
        
        # Job storage: keys are job_ids, values are statuses (e.g. "working on it", "completed", or "error: ...")
        self.jobs = {}
        
        # Optionally store results (e.g., image filenames) in a separate dictionary
        # keyed by job_id
        self.job_results = {}

    def process_job(self, job_id, text):
        """
        Processes an incoming text by running NLP analysis, translation,
        and then generating infographics. The job status is updated
        as the work proceeds.
        """
        try:

            # Set initial status
            self.jobs[job_id] = "working on it"
            
            # NLP processing
            hebrew_text_data = self.nlp_model.NLP_procces(text)
            if hebrew_text_data["status"] == 0:
                self.jobs[job_id] = f"error: {hebrew_text_data['message']}"
                return False

            # Translation processing
            translations = self.translator.translation_procces(hebrew_text_data["message"].strip())
            message_status, translations_message = translations["status"], translations["message"]

            if message_status == 1:
                # Prepare merged JSON from Hebrew and translations
                formatted_hebrew_json = {"hebrew": clean_json(hebrew_text_data["message"])}
                translations_dict = clean_json(translations_message)
                merged_json = {**formatted_hebrew_json, **translations_dict}
                
                language_map = {
                    "hebrew":  "generated/infographic_hebrew.png",
                    "arabic":  "generated/infographic_arabic.png",
                    "english": "generated/infographic_english.png",
                    "russian": "generated/infographic_russian.png",
                }
            else:
                self.jobs[job_id] = f"error: {translations_message}"
                return False

            # Create infographic for each language
            for lang, filename in language_map.items():
                try:
                    # Create an instance for the specific language
                    generator = InfographicGenerator(lang)
                    generator.create_infographic(filename, merged_json[lang])
                except KeyError:
                    self.jobs[job_id] = f"error: missing data for language '{lang}'"
                    return False

            # Optionally store the filenames in job_results for retrieval later
            self.job_results[job_id] = {
                "hebrew": "generated/infographic_hebrew.svg",
                "arabic": "generated/infographic_arabic.svg",
                "english": "generated/infographic_english.svg",
                "russian": "generated/infographic_russian.svg"
            }

            #convert to svg
            for lang in language_map.keys():
                input_file = os.path.normpath(os.path.join(file_path, language_map[lang]))
                output_file = os.path.normpath(os.path.join(file_path, self.job_results[job_id][lang]))
                self.convert_to_svg(input_file, output_file)
                
        except Exception as e:
            self.jobs[job_id] = f"error: {e}"
            return False

        # Mark job as done
        self.jobs[job_id] = "completed"

        return True
    
    def get_status(self, job_id):
        """
        Returns the current status of the given job.
        """
        return self.jobs.get(job_id, "Job not found")

    def get_result(self, job_id):
        """
        Returns a dictionary of the four image filenames if the job is complete,
        or None if the job is not finished or not found.
        """
        if self.jobs.get(job_id) == "completed":
            # Return the previously stored filenames
            return self.job_results.get(job_id)
        else:
            return None

    def convert_to_svg(self, input_path, output_path):
        command = [
            inkscape_path,
            input_path,
            "--export-type=svg",
            "--export-plain-svg",
            f"--export-filename={output_path}"
        ]
        print(command)

        try:
            subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print("Error Output:", e.stderr)
            raise e



def clean_json(text_data):
    return json.loads(text_data.strip("```json").strip("```"))  # Clean JSON and load it
