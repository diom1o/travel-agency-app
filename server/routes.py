import os
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

# Load environment variables
load_dotenv()

# Initialize Flask and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///default.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'a_secret_key') # Required for session management
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email}

class Tour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'description': self.description, 'price': self.price}

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'user_id': self.user_id, 'tour_id': self.tour_id, 'date': self.date}

# Routes
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(name=data.get('name'), email=data.get('email'))
    new_user.set_password(data.get('password')) # Assuming you're sending a password
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully.', 'user': new_user.to_dict()}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()
    if user and user.check_password(data.get('password')):
        session['user_id'] = user.id
        return jsonify({'message': 'Logged in successfully.'}), 200
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully.'}), 200

@app.route('/tours/search', methods=['GET'])
def search_tours():
    query = request.args.get('query')
    if query:
        results = Tour.query.filter((Tour.title.contains(query)) | (Tour.description.contains(query))).all()
        return jsonify([tour.to_dict() for tour in results])
    return jsonify({'message': 'No query provided.'}), 400

@app.route('/tours', methods=['POST'])
def create_tour():
    data = request.json
    new_tour = Tour(title=data.get('title'), description=data.get('description'), price=data.get('price'))
    db.session.add(new_tour)
    db.session.commit()
    return jsonify({'message': 'Tour created successfully.', 'tour': new_tour.to_dict()}), 201

@app.route('/bookings', methods=['POST'])
def create_booking():
    # Assuming user_id comes from the logged-in user's session
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    user_id = session['user_id']
    data = request.json
    new_booking = Booking(user_id=user_id, tour_id=data.get('tour_id'), date=data.get('date'))
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'message': 'Booking created successfully.', 'booking': new_booking.to_dict()}), 201

# Error handling
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify({'error': 'Resource not found.'}), 404

# Start the Flask app
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)