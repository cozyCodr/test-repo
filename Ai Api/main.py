import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import prompts
import PyPDF2
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

_ = load_dotenv(find_dotenv())
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)


model = "gpt-3.5-turbo"
temperature = 0.4
max_tokens = 500


def read_file_content(file_name):
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
    img = Image.open(filename)

    # Use Tesseract to do OCR on the image
    extracted_text = pytesseract.image_to_string(img)
    return extracted_text


print("What do you want to do: ")
print("1. Generate keyconcepts.")
print("2. Go through past papers.")
print("3. Assess yourself with a quiz")
Task = input("Your option is: ")

if Task == "1":
    filename = "Capacitance.pdf"
    file_content = read_file_content(filename)

    def key_concepts(model, max_tokens, temperature):
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
            temperature=temperature
        )
        return completion.choices[0].message.content
    response = key_concepts(model, max_tokens, temperature)
    print(response)

    # def key_concepts(model, max_tokens, temperature):
    #     system_message = prompts.system_message1
    #     prompt = prompts.book_reference(file_content)

    #     messages = [
    #         {"role": "system", "content": system_message},
    #         {"role": "user", "content": prompt},
    #     ]

    #     completion = client.chat.completions.create(
    #     model=model,
    #     messages=messages,
    #     max_tokens=max_tokens,
    #     temperature=temperature
    #     )
    #     return completion.choices[0].message.content
    # response = key_concepts(model, max_tokens, temperature)
    # print(response)

elif Task == "2":
    filename = "PP1.jpg"
    file_content = extract_text(filename)

    def past_papers(model, max_tokens, temperature):
        system_message = prompts.system_message4
        prompt = prompts.generate_from_pastpaper(file_content)

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return completion.choices[0].message.content
    response = past_papers(model, max_tokens, temperature)
    print(response)

# elif Task == "3":

else:
    print("You have entered an invalid option.")
