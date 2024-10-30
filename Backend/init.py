#from main import create_app, db
from models import Concept, File
import datetime
from exts import db

#app = create_app()
#with app.app_context():
#    db.create_all()

def format_concepts_for_db(concepts_list):
            formatted_concepts = []
            for concept in concepts_list:
                title, explanation = concept.split(":", 1)
                formatted_concepts.append({
                    "title": title.strip(),
                    "explanation": explanation.strip()
                })
            return formatted_concepts

def save_concepts_to_db(formatted_concepts, fid):
    
    for concept in formatted_concepts:
        new_concept = Concept(
              content=concept['title'], 
              explanation=concept['explanation'], 
              file_id = fid, 
              created_at= datetime.utcnow()
              )
        db.session.add(new_concept)
    
    db.session.commit()
    return {"message": "Concepts saved successfully"}
