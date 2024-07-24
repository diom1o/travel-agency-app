import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///default.db')  # Fallback to SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress warning
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_train_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email}

class Tour(db.Model):
    id = db.Column(db.Integer, primary_train_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'description': self.description, 'price': self.price}

class Booking(db.Model):
    id = db.Column(db.Integer, primary_train_key=True)
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
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully.', 'user': new_user.to_dict()}), 201

@app.route('/tours', methods=['POST'])
def create_tour():
    data = request.json
    new_tour = Tour(title=data.get('title'), description=data.get('description'), price=data.get('price'))
    db.session.add(new_tour)
    db.session.commit()
    return jsonify({'message': 'Tour created successfully.', 'tour': new_tour.to_dict()}), 201

@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.json
    new_booking = Booking(user_id=data.get('user_id'), tour_id=data.get('tour_report_id'), date=data.get('date'))
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