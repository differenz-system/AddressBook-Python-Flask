from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field  # Import from marshmallow_sqlalchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv
import os


app = Flask(__name__)

load_dotenv()


# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Schemas
class ContactSchema(SQLAlchemySchema):  # Use SQLAlchemySchema instead of SQLAlchemyAutoSchema
    class Meta:
        model = Contact
        load_instance = True  # Allows you to load and dump model instances

    id = auto_field()
    name = auto_field()
    email = auto_field()
    phone = auto_field()
    address = auto_field()
    user_id = auto_field()

class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = auto_field()
    username = auto_field()
    email = auto_field()
    password = auto_field()

# Initialize schemas
contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)
user_schema = UserSchema()

# Routes
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    result = user_schema.dump(new_user)  # Serialize the new_user object
    return jsonify(result)  # Return the serialized object as JSON

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity={'id': user.id, 'username': user.username})
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/contacts', methods=['GET'])
@jwt_required()
def get_contacts():
    user_id = get_jwt_identity()['id']
    contacts = Contact.query.filter_by(user_id=user_id).all()
    return contacts_schema.jsonify(contacts)

@app.route('/contacts', methods=['POST'])
@jwt_required()
def add_contact():
    user_id = get_jwt_identity()['id']
    data = request.get_json()
    new_contact = Contact(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        address=data['address'],
        user_id=user_id
    )
    db.session.add(new_contact)
    db.session.commit()
    return contact_schema.jsonify(new_contact)

@app.route('/contacts/<int:id>', methods=['PUT'])
@jwt_required()
def update_contact(id):
    user_id = get_jwt_identity()['id']
    contact = Contact.query.filter_by(id=id, user_id=user_id).first()
    if not contact:
        return jsonify({'error': 'Contact not found'}), 404

    data = request.get_json()
    contact.name = data['name']
    contact.email = data['email']
    contact.phone = data['phone']
    contact.address = data['address']
    db.session.commit()
    return contact_schema.jsonify(contact)

@app.route('/contacts/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_contact(id):
    user_id = get_jwt_identity()['id']
    contact = Contact.query.filter_by(id=id, user_id=user_id).first()
    if not contact:
        return jsonify({'error': 'Contact not found'}), 404

    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'Contact deleted'})

# Initialize database
# @app.before_first_request
# def create_tables():
#     db.create_all()

if __name__ == '__main__':
    # Initialize database tables manually
    with app.app_context():
        db.create_all()  # Create all tables here
    app.run(debug=True)

