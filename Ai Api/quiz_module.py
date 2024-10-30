import os
from openai import OpenAI
import PyPDF2  # Add this import at the top

class QuizGenerator:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        
    def read_file_content(self, filename):
        """Read content from a PDF file."""
        try:
            if filename.lower().endswith('.pdf'):
                with open(filename, 'rb') as file:  # Note the 'rb' mode for binary reading
                    # Create a PDF reader object
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    # Extract text from all pages
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                    return text
            else:
                # For non-PDF files, try different encodings
                encodings = ['utf-8', 'latin-1', 'ascii', 'iso-8859-1']
                for encoding in encodings:
                    try:
                        with open(filename, 'r', encoding=encoding) as file:
                            return file.read()
                    except UnicodeDecodeError:
                        continue
                raise Exception(f"Could not read file with any of the attempted encodings: {encodings}")
        except FileNotFoundError:
            raise Exception(f"File {filename} not found.")
        except Exception as e:
            raise Exception(f"Error reading file: {str(e)}")
            
    def generate_quiz(self, file_content, num_questions=5):
        """Generate quiz questions using GPT-3.5-turbo."""
        system_message = """You are a helpful assistant that creates multiple-choice quiz questions. 
        For each question, provide:
        1. The question
        2. Four options (A, B, C, D)
        3. The correct answer
        Format each question as:
        Question: [question text]
        A) [option A]
        B) [option B]
        C) [option C]
        D) [option D]
        Answer: [correct letter]"""
        
        prompt = f"""Generate {num_questions} multiple-choice questions based on this content:
        {file_content}
        
        Make sure each question:
        - Tests understanding of key concepts
        - Has one clearly correct answer
        - Has plausible but incorrect alternatives"""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        return completion.choices[0].message.content
        
    def parse_quiz_response(self, response):
        """Parse the GPT response into structured quiz data."""
        questions = response.strip().split("\n\n")
        quiz_data = []
        
        for q in questions:
            try:
                lines = q.strip().split("\n")
                question = lines[0].replace("Question: ", "").strip()
                options = [line.strip() for line in lines[1:5]]
                correct_answer = lines[5].replace("Answer: ", "").strip()
                
                quiz_data.append({
                    "question": question,
                    "options": options,
                    "correct_answer": correct_answer
                })
            except IndexError:
                continue  # Skip malformed questions
                
        return quiz_data
        
    def run_quiz(self, quiz_data):
        """Run the interactive quiz and grade responses."""
        student_answers = {}
        score = 0
        total_questions = len(quiz_data)
        
        print("\n=== Quiz Started ===\n")
        
        for i, quiz_item in enumerate(quiz_data, 1):
            print(f"\nQuestion {i}: {quiz_item['question']}")
            for option in quiz_item['options']:
                print(option)
                
            while True:
                answer = input("\nYour answer (A/B/C/D): ").strip().upper()
                if answer in ['A', 'B', 'C', 'D']:
                    break
                print("Invalid input. Please enter A, B, C, or D.")
            
            student_answers[i] = answer
            correct = answer == quiz_item['correct_answer']
            
            print("Correct! ✓" if correct else f"Incorrect. The correct answer was {quiz_item['correct_answer']} ✗")
            if correct:
                score += 1
        
        self.show_report(student_answers, quiz_data, score, total_questions)
        
    def show_report(self, student_answers, quiz_data, score, total_questions):
        """Display a detailed quiz report."""
        print("\n=== Quiz Report ===")
        print(f"\nFinal Score: {score}/{total_questions} ({(score/total_questions*100):.1f}%)\n")
        
        for i, quiz_item in enumerate(quiz_data, 1):
            student_answer = student_answers.get(i, "No Answer")
            status = "✓" if student_answer == quiz_item['correct_answer'] else "✗"
            
            print(f"Q{i}: {quiz_item['question']}")
            print(f"Your Answer: {student_answer} | Correct Answer: {quiz_item['correct_answer']} | {status}\n")

def main():
    # Initialize the quiz generator
    quiz_gen = QuizGenerator()
    
    # Read the file content
    filename = "Capacitance.pdf"
    file_content = quiz_gen.read_file_content(filename)
    
    # Generate and parse the quiz
    response = quiz_gen.generate_quiz(file_content)
    quiz_data = quiz_gen.parse_quiz_response(response)
    
    # Run the quiz
    quiz_gen.run_quiz(quiz_data)

if __name__ == "__main__":
    main()