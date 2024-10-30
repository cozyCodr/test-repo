from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from models import Course, File, Concept, Query, Student
from datetime import datetime
from sqlalchemy import func

dashboard_blueprint = Namespace(
    'dashboard',
    description='Operations related to user quesries'
)

query_model = dashboard_blueprint.model('File', {
    'id': fields.Integer(readonly=True),
    'query': fields.String(required=True),
    'answer': fields.String(required=True),
    'student_id': fields.Integer(required=True),
    'created_at': fields.DateTime(readonly=True),
    'course_id': fields.Integer(required=True)
})


@dashboard_blueprint.route('/ask-eduquery')
class AskQuery(Resource):
    @jwt_required(optional=True)  # Optional Jwt()
    def get(self):
        """Get user's recent queries"""
        user_id = get_jwt_identity()
        queries = Query.query.filter_by(student_id=user_id)\
            .order_by(Query.created_at.desc())\
            .limit(10)\
            .all()

        return {
            'queries': [{
                'id': q.id,
                'query': q.query,
                'answer': q.answer,
                'created_at': q.created_at.isoformat()
            } for q in queries]
        }

    @jwt_required(optional=True)  # Optional Jwt()
    @dashboard_blueprint.expect(query_model)
    def post(self):
        """Save a new query"""
        user_id = get_jwt_identity()
        data = request.get_json()

        new_query = Query(
            student_id=user_id,
            query=data['query'],
            answer='',  # This would be filled by your answer generation logic
            created_at=datetime.utcnow()
        )
        new_query.save()

        return {
            'message': 'Query saved successfully',
            'query_id': new_query.id
        }, 201


@dashboard_blueprint.route('/test')
class TestEndpoint(Resource):
    def get(self):
        """Test endpoint to verify API functionality"""
        return {
            'message': 'API is running',
            'status': 'success',
            'timestamp': datetime.utcnow().isoformat()
        }
