from app.app_main.dto.users import UsersDto
from flask_restx import Resource
from app.app_main.models.users import Users
from app.app_main.schemas.users import UserRegistrationSchema
from werkzeug.utils import secure_filename
from marshmallow import ValidationError
import os
import random
from flask import request
from app.app_main import db

def generate_unique_number():
    """Generate a 6-digit unique number."""
    return f"{random.randint(100000, 999999)}"

signup_blueprint=UsersDto.signupapi
#usersignup
@signup_blueprint.route('',methods=['POST'])
class signup(Resource):
    def post(self):
        schema = UserRegistrationSchema()
         # Extract form data
        data = request.form.to_dict()
        file = request.files.get('file')
        # Validate input data and file
        try:
            # Validate JSON data (excluding the file)
            validated_data = schema.load(data)
        except ValidationError as err:
            return {'errors': err.messages}, 400
        
        user = Users.query.filter_by(email=validated_data['email']).first()

        if user:
            return {'message': 'user already exists'},400
        
        # Handle file upload
        if file:
            upload_folder = '/home/ytp/Desktop/uploads'  # Define your upload folder
            os.makedirs(upload_folder, exist_ok=True)  # Ensure the folder exists
        
            unique_number = generate_unique_number()
            secure_name = secure_filename(file.filename)  # Generate 6-digit unique number
            file_name = f"{unique_number}_{secure_name}"  # Append the unique number to the file name
            file_path = os.path.join(upload_folder, file_name)  # Generate full file path
            file.save(file_path)  # Save the file to the server
        else:
            file_path = None  # No file uploaded
        
        new_user= Users(
            **validated_data,
            profile_picture=file_path
        )
        new_user.set_password(validated_data.get('password'))

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

        return {'message': 'User created successfully'}, 201

