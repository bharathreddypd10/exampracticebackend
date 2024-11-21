from app.app_main import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash,check_password_hash

class Users(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firstName = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(10), nullable=False)  # Add gender field here
    dob = db.Column(db.Date, nullable=False)
    phoneNumber = db.Column(db.String(15), unique=True, nullable=False)  # Assuming phone numbers are unique
    address = db.Column(db.String(255), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True) 

    def __repr__(self):
        return f'<User {self.firstName} {self.lastName}>'

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'user_id': self.user_id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'phoneNumber': self.phoneNumber,
            'gender':self.gender,
            'dob':self.dob,
            'address': self.address,
            'profile_picture': self.profile_picture
        }
    

    def set_password(self, password):
        self.password = generate_password_hash(password,salt_length=10)

    def check_password(self, password):
        return check_password_hash(self.password, password)