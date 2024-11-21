from marshmallow import Schema, fields, validate
from datetime import datetime

class UserRegistrationSchema(Schema):
    # First Name Validation (Required, Length between 2-80)
    firstName = fields.String(
        required=True,
        validate=validate.Length(min=2, max=80),
        error_messages={
            "required": "First name is required.",
            "null": "First name cannot be null.",
            "validator_failed": "First name must be between 2 and 80 characters."
        }
    )

    # Last Name Validation (Required, Length between 2-80)
    lastName = fields.String(
        required=True,
        validate=validate.Length(min=2, max=80),
        error_messages={
            "required": "Last name is required.",
            "null": "Last name cannot be null.",
            "validator_failed": "Last name must be between 2 and 80 characters."
        }
    )

    # Email Validation (Required, Valid Email Format)
    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email is required.",
            "invalid": "Enter a valid email address."
        }
    )

    # Mobile Number Validation (Required, Must be 10-15 digits long)
    phoneNumber = fields.String(
        required=True,
        validate=validate.Regexp(r'^\d{10,15}$', error="Phone number must be numeric and 10-15 digits long."),
        error_messages={"required": "Mobile number is required"}
    )

    # Gender Validation (Required, Only 'male', 'female', or 'other' are valid options)
    gender = fields.String(
        required=True,
        validate=validate.OneOf(["male", "female", "other"], error="Gender must be 'male', 'female', or 'other'."),
        error_messages={"required": "Gender is required"}
    )

    # Date of Birth Validation (Required, Valid Date)
    dob = fields.Date(
        required=True,
        error_messages={"required": "Date of birth is required"},
        validate=lambda val: val <= datetime.today().date() and val >= datetime.today().date().replace(year=datetime.today().year - 100),
    )

    # Address Validation (Required, Maximum Length 255 characters)
    address = fields.String(
        required=True,
        validate=validate.Length(max=255),
        error_messages={"required": "Address is required", "max": "Address cannot exceed 255 characters."}
    )

    # Password Validation (Required, Complex Password)
    password = fields.String(
        required=True,
        validate=validate.Regexp(
            r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$',
            error="Password must have at least 8 characters, one uppercase letter, one digit, and one special character."
        ),
        error_messages={"required": "Password is required"}
    )

    # Profile Picture Validation (Optional, Valid File Name)
    profilePicture = fields.String(
        required=False,  # Optional, as some users may not upload an image initially
        validate=validate.Regexp(
            r'^[^\\/:*?"<>|]+$',  # Regex to prevent illegal characters in the filename
            error="Invalid file name for profile picture. It cannot contain special characters like \\ / : * ? \" < > |"
        ),
        error_messages={"invalid": "Profile picture file name is invalid"}
    )

    # Optional: Custom function to check that the user is at least 18 years old (for DOB validation)
    def validate_dob(self, dob):
        age = (datetime.today().date() - dob).days // 365
        if age < 18:
            raise validate.ValidationError("You must be at least 18 years old to register.")
        return dob
