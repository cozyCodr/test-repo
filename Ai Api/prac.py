import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import prompts  # Ensure prompts.py contains necessary prompt functions
import PyPDF2
import pytesseract
from quiz_module import QuizGenerator  # Import the QuizGenerator class
from PIL import Image

# Configure Tesseract for OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load API key from environment variables
_ = load_dotenv(find_dotenv())
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# GPT-3.5-turbo parameters
model = "gpt-3.5-turbo"
temperature = 0.4
max_tokens = 500

def read_file_content(file_name):
    """Read the content from a PDF file."""
    content = ""
    try:
        with open(file_name, "rb") as document:
            reader = PyPDF2.PdfReader(document)
            for page in range(len(reader.pages)):
                content += reader.pages[page].extract_text() + " "
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    return content.strip()

def extract_text(filename):
    """Extract text from an image using Tesseract OCR."""
    img = Image.open(filename)
    extracted_text = pytesseract.image_to_string(img)
    return extracted_text

# Display options to the user
print("What do you want to do:")
print("1. Generate key concepts.")
print("2. Go through past papers.")
print("3. Assess yourself with a quiz")
Task = input("Your option is: ").strip()

if Task == "1":
    filename = "Capacitance.pdf"
    file_content = read_file_content(filename)

    if file_content:
        def key_concepts():
            system_message = prompts.system_message1
            prompt1 = prompts.generate_key_concepts(file_content)

            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt1},
            ]

            completion = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return completion.choices[0].message.content

        print(key_concepts())

elif Task == "2":
    filename = "PP1.jpg"
    file_content = extract_text(filename)

    def past_papers():
        system_message = prompts.system_message4
        prompt = prompts.generate_from_pastpaper(file_content)

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ]

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return completion.choices[0].message.content

    print(past_papers())

elif Task == "3":
    def main():
        """Initialize and run the quiz generator."""
        quiz_gen = QuizGenerator()
        filename = "Capacitance.pdf"

        try:
            file_content = quiz_gen.read_file_content(filename)

            # Generate and run the quiz
            response = quiz_gen.generate_quiz(file_content)
            quiz_data = quiz_gen.parse_quiz_response(response)
            quiz_gen.run_quiz(quiz_data)

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    main()

else:
    print("You have entered an invalid option.")
