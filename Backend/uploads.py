from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
# Optional Jwt, get_jwt_identity
from flask_jwt_extended import jwt_required
from models import Course, File, Concept, Query, Student
from datetime import datetime
from sqlalchemy import func

uploads_blueprint = Namespace(
    'uploads',
    description='Operations related to upload materials materials'
)

file_model = uploads_blueprint.model('File', {
    'id': fields.Integer(readonly=True),
    'code': fields.String(required=True),
    'name': fields.String(required=True),
    'data': fields.String(required=True),
    'course_id': fields.String(required=True),
    'uploaded_at': fields.DateTime(readonly=True)
})


@uploads_blueprint.route('/files')
class FileResource(Resource):
    @jwt_required(optional=True)  # Optional Jwt()
    @uploads_blueprint.expect(file_model)
    @uploads_blueprint.marshal_with(file_model)
    def post(self):
        """Upload a new file"""
        data = request.get_json()
        code = data['coursecode']
        cid = Course.query.filter_by(code=code)
        new_file = File(
            code=data['coursecode'],
            name=data['title'],
            data=data['data'],
            course_id=cid.id,
            uploaded_at=datetime.utcnow()
        )
        new_file.save()
        return new_file, 201


@uploads_blueprint.route('/files/<int:file_id>')
class FileDetail(Resource):
    @jwt_required(optional=True)  # Optional Jwt()
    @uploads_blueprint.marshal_with(file_model)
    def get(self, file_id):
        """Get specific file details"""
        file = File.query.get_or_404(file_id)
        return file

    @jwt_required(optional=True)  # Optional Jwt()
    def delete(self, file_id):
        """Delete a file"""
        file = File.query.get_or_404(file_id)
        file.delete()
        return {'message': 'File deleted successfully'}, 200
