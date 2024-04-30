# Imports
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from info import * 

# Create the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

# Create the User model
class User(db.Model):
    # Store alias, username, password, gmail, OpenAI API key & Age
    alias = db.Column(db.String(aliasLengthMax), nullable=False, unique=False)
    username = db.Column(db.String(usernameLengthMax), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.String(passwordLengthMax), nullable=False)
    gmail = db.Column(db.String(gmailLengthMax), nullable=False, unique=True)
    openai_api_key = db.Column(db.String(openaiApiKeyLengthMax), nullable=False, unique=False)
    age = db.Column(db.Integer, nullable=False, unique=False)

    # Methods to save data and check password
    def __init__(self, alias, username, password, gmail, openai_api_key, age):
        self.alias = alias
        self.username = username
        self.set_password(password)
        self.gmail = gmail
        self.openai_api_key = openai_api_key
        self.age = age

    # Methods to set and check password
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def serialize(self):
        return {
            'alias': self.alias,
            'age': self.age,
            'openai_api_key': self.openai_api_key
        }  

# Routes

# Sign up route 
@app.route('/signup', methods=['POST'])
def signup():
    with app.app_context():
        # Get data
        data = request.get_json()
        alias = data['alias']
        username = data['username']
        password = data['password']
        gmail = data['gmail']
        openai_api_key = data['openai_api_key']
        age = data['age']

        # check if data is empty
        if not alias or not username or not password or not gmail or not openai_api_key or not age:
            return jsonify({'error': 'Please fill all the missing Feilds.'}), 400
    
        # check if user or gmail already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'User already exists.'}), 400
        elif User.query.filter_by(gmail=gmail).first():
            return jsonify({'error': 'Gmail already exists.'}), 400

        # Create a new user
        user = User(alias, username, password, gmail, openai_api_key, age)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User created successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    with app.app_context():
        # Get data
        data = request.get_json()
        username = data['username']
        password = data['password']

        # check if data is empty
        if not username or not password:
            return jsonify({'error': 'Please fill all the missing Feilds.'}), 400

        # check if user exists
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid username or password.'}), 400

        # Return sucess message, name, age and openai api key
        return jsonify({'message': 'Login successful!', 'alias': user.alias, 'age': user.age, 'openai_api_key': user.openai_api_key}), 200

# Run the server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(app.run(host='0.0.0.0',port=6969,debug=True))