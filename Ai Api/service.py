# services/ai_service.py
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
import os
from openai import OpenAI
from PIL import Image
import pytesseract
import PyPDF2
from functools import lru_cache


class AIService:
    def _init_(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-3.5-turbo"
        self.temperature = 0.4
        self.max_tokens = 500
        # Configure tesseract path if needed
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def _read_pdf_content(self, file_path):
        """Read content from PDF file"""
        content = ""
        try:
            with open(file_path, "rb") as document:
                reader = PyPDF2.PdfReader(document)
                for page in range(len(reader.pages)):
                    content += reader.pages[page].extract_text() + " "
            return content.strip()
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")

    def _extract_image_text(self, image_path):
        """Extract text from image using OCR"""
        try:
            img = Image.open(image_path)
            return pytesseract.image_to_string(img)
        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")

    def generate_completion(self, system_message, user_message):
        """Generate completion using OpenAI API"""
        try:
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ]

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating AI completion: {str(e)}")

    def analyze_key_concepts(self, file_path):
        """Analyze key concepts from PDF"""
        try:
            content = self._read_pdf_content(file_path)
            system_message = "You are an expert educational content analyzer."
            user_message = f"Extract and explain the key concepts from this text: {content}"
            return self.generate_completion(system_message, user_message)
        except Exception as e:
            raise Exception(f"Error analyzing key concepts: {str(e)}")

    def analyze_past_paper(self, image_path):
        """Analyze past paper from image"""
        try:
            content = self._extract_image_text(image_path)
            system_message = "You are an expert exam question analyzer."
            user_message = f"Analyze this past paper question and provide detailed solution steps: {content}"
            return self.generate_completion(system_message, user_message)
        except Exception as e:
            raise Exception(f"Error analyzing past paper: {str(e)}")


# views/concepts.py

concepts_ns = Namespace(
    'concepts', description='Operations related to educational concepts')
ai_service = AIService()


@concepts_ns.route('/analyze-pdf')
class ConceptsAnalysis(Resource):
    @jwt_required(optional=True)  # Optional Jwt()
    def post(self):
        """Analyze PDF for key concepts"""
        try:
            if 'file' not in request.files:
                return {'message': 'No file provided'}, 400

            file = request.files['file']
            if file.filename == '':
                return {'message': 'No file selected'}, 400

            if not file.filename.lower().endswith('.pdf'):
                return {'message': 'Only PDF files are allowed'}, 400

            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)

            try:
                analysis = ai_service.analyze_key_concepts(file_path)
                return {'analysis': analysis}, 200
            finally:
                # Clean up the uploaded file
                if os.path.exists(file_path):
                    os.remove(file_path)

        except Exception as e:
            return {'message': f'Error processing file: {str(e)}'}, 500


@concepts_ns.route('/analyze-past-paper')
class PastPaperAnalysis(Resource):
    @jwt_required(optional=True)  # Optional Jwt()
    def post(self):
        """Analyze past paper image"""
        try:
            if 'file' not in request.files:
                return {'message': 'No file provided'}, 400

            file = request.files['file']
            if file.filename == '':
                return {'message': 'No file selected'}, 400

            if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                return {'message': 'Only image files are allowed'}, 400

            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)

            try:
                analysis = ai_service.analyze_past_paper(file_path)
                return {'analysis': analysis}, 200
            finally:
                # Clean up the uploaded file
                if os.path.exists(file_path):
                    os.remove(file_path)

        except Exception as e:
            return {'message': f'Error processing file: {str(e)}'}, 500
