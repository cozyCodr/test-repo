from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from models import Concept
from datetime import datetime
import fitz  # PyMuPDF
from openai import OpenAI
from config import Config  # Update import to get the configuration class
import json

concepts_blueprint = Namespace(
    'concepts',
    description='Operations related to course concepts and materials'
)

# Models for request/response
concept_model = concepts_blueprint.model('Concept', {
    'content': fields.String(required=True),
    'explanation': fields.String(required=True),
    'file_id': fields.Integer(required=True),
    'created_at': fields.DateTime(readonly=True)
})

# Initialize OpenAI client with API key from config
client = OpenAI(api_key=Config.OPENAI_API_KEY)


@concepts_blueprint.route('/generate')
class ConceptGeneration(Resource):
    @jwt_required(optional=True)  # Optional Jwt()
    @concepts_blueprint.expect(concept_model)
    def post(self):
        """Handle PDF upload and generate key concepts."""
        if 'file' not in request.files:
            return jsonify({'message': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        # Read PDF content
        pdf_content = self.extract_pdf_content(file)

        # Send content to OpenAI for key concept extraction
        concepts_data = self.extract_key_concepts(pdf_content)

        # Validate that concepts_data is a list of dictionaries
        if not isinstance(concepts_data, list):
            return jsonify({'message': 'Invalid response format from OpenAI'}), 500

        # Save each concept to the database
        for concept in concepts_data:
            if isinstance(concept, dict) and 'content' in concept:
                new_concept = Concept(
                    content=concept['content'],  # The extracted content
                    explanation=concept.get(
                        'explanation', 'No explanation provided'),
                    created_at=datetime.utcnow()
                )
                # Add the new concept to the session
                # db.session.add(new_concept)

        # db.session.commit()  # Commit the session to save all changes
        print("concepts data")
        print(concepts_data)
        return concepts_data
        # return jsonify({'message': 'PDF processed successfully', 'concepts': concepts_data}), 200

    def extract_pdf_content(self, file):
        """Use PyMuPDF to extract text from PDF."""
        print("here- extracting pdf content")
        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in pdf_document:
            text += page.get_text()
        pdf_document.close()
        return text

    def extract_key_concepts(self, content):
        """Send the content to OpenAI to extract key concepts."""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Extract key concepts from the following text:\n\n{content}\n\nReturn the result in JSON format as a list of objects with 'content' and 'explanation'."}
            ]
        )

        # Get the response string and attempt to parse it
        # Extract the string
        key_concepts_str = response.choices[0].message.content.strip()
        print(key_concepts_str)

        # Convert the string to a list of dictionaries (if the response is JSON)
        try:
            # Parse the JSON string
            key_concepts = json.loads(key_concepts_str)
            print(key_concepts)
        except json.JSONDecodeError:
            # Handle error in parsing JSON
            key_concepts = []  # Return an empty list if JSON parsing fails

        return key_concepts  # Return the list of concepts
