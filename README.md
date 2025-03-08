# Infographic Generator

The Infographic Generator is a web service designed to create professional infographics based on input Hebrew text. The system processes the text using natural language processing (NLP), translates the structured output into multiple languages, and generates graphic outputs tailored to the design style of the Home Front Command and optimized for Instagram formats.

---

## Table of Contents

- [Project Features](#project-features)
- [System Requirements](#system-requirements)
- [Installation and Setup](#installation-and-setup)
- [Prompting Instructions](#prompting-instructions)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Future Improvements](#future-improvements)

---

## Project Features

- **Advanced Text Processing:**  
  Analyzes Hebrew text using an NLP model to extract structured information following a predefined template.

- **Multi-Language Translation:**  
  Translates the structured output into Arabic, Russian, and English while maintaining the original structure and highlighted keywords.

- **Infographic Creation:**  
  Generates infographics in Instagram-friendly formats (1:1 or 4:5) using dynamic image generation techniques with the Python Pillow library.

- **Modular and Clean Architecture:**  
  The project is organized into separate modules (e.g., `main.py`, `chat_manager.py`, text processing, translation, infographic creation) that simplify maintenance and future extensions.

- **REST API:**  
  Provides endpoints for sending text, checking job status, and retrieving the final infographic outputs.

- **User Interface:**  
  A simple web interface (HTML) allows users to input text and view or download the generated infographics.

---

## System Requirements

- **Python 3.8+**
- **Inkscape:**  
  Inkscape must be installed on your system. The application uses Inkscape for converting generated images to SVG format.
- Dependencies are listed in the [requirements.txt](./requirements.txt) file:
  ```plaintext
  fastapi
  uvicorn
  Pillow
  langdetect
  arabic_reshaper
  python-bidi
  protobuf
  pydantic
  google-auth
  google-generativeai
  ```

---

## Installation and Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/poptarts12/infographic-generator/
   cd infographic-generator
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Inkscape:**
   Download and install Inkscape from [Inkscape's official website](https://inkscape.org/).  
   **Note:** Ensure Inkscape is installed on your system. By default, the path is set to:
   ```plaintext
   C:\Program Files\Inkscape\bin\inkscape.exe
   ```
   If your Inkscape installation is located in a different path, update the `inkscape_path` variable in `chat_manager.py` accordingly.

4. **Run the Application:**  
   Run the main script to start processing text and generating infographics:
   ```bash
   python main.py
   ```

---

## Prompting Instructions

To ensure optimal results when generating infographics, follow these guidelines when entering prompts:

- **Use clear and concise Hebrew text** for better structuring and translation accuracy.
- **Avoid special characters or excessive punctuation**, as they may interfere with processing.
- **If highlighting specific words**, make sure they are properly spaced and not merged with other text.
- **Use full sentences instead of fragmented words**, as the NLP model works best with contextual data.
- **Ensure important keywords are included** to make them stand out in the infographic design.

Example prompt:
```plaintext
הנחיות למקרה חירום: כאשר נשמעת אזעקה, יש להיכנס למרחב המוגן ולהישאר שם 10 דקות לפחות.
```

---

## API Documentation

The full API documentation is available in the [API_Documentation.docx](./API_Documentation.docx) file. Below is a brief summary of the main endpoints:

### **1. POST /api/generate**
- **Description:** Accepts Hebrew text and initiates the infographic generation process.  
- **Response:** Returns a `job_id` and an initial status message (e.g., "working on it").

### **2. GET /api/status/{job_id}**
- **Description:** Checks the processing status of a job by its `job_id`.  
- **Response:** Returns the current status, such as "working on it", "completed", or an error message.

### **3. GET /api/result/{job_id}**
- **Description:** Once the job is completed, this endpoint returns the file paths for the generated infographic images in multiple languages.  
- **Response:** Provides file paths (e.g., `"generated/infographic_hebrew.svg"`) that can be used to display or download the images.

---

## Project Structure

```plaintext
infographic-generator/
│── core/
│   ├── infographic_maker.py
│   ├── word_checker.py
│── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│── models/
│   ├── instruction_prompts.py
│   ├── model_maker.py
│   ├── text_processing.py
│   ├── translation.py
│── routes/
│   ├── generate.py
│   ├── test_results/
│── tests/
│   ├── test_word_checker.py
│   ├── test_infographic_maker.py
│   ├── test_nlp_model.py
│   ├── test_translator_model.py
│   ├── test_chat_manager.py
│   ├── test_api.py
│── main.py
│── chat_manager.py
│── API_Documentation.docx
│── README.md
│── requirements.txt
```

---

## Testing

### **Run All Tests**
To run all unit and integration tests, use:
```bash
pytest tests/
```

### **Run Specific Test Files**
To test a specific module:
```bash
pytest tests/test_word_checker.py
```

### **Ensure Pytest is Installed**
If `pytest` is not installed, install it with:
```bash
pip install pytest
```

---

## Future Improvements

- **User Interface Enhancements:**  
  More official and creative format of the posts, using models like trained Stable Diffusion to provide more options for creativity and to make the infographics more accurate to the original ones (with icons and different styles).

