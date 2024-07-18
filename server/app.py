from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///:memory:')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)  # Fixed Typo: Ndb.Column -> db.Column

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Utility functions for bulk operations
def create_tours(tours_data):
    tours = [Tour(name=t['name'], description=t.get('description', ''), price=t['price']) for t in tours_data]
    db.session.bulk_save_objects(tours)
    db.session.commit()

def create_bookings(bookings_data):
    bookings = [Booking(user_id=b['user_id'], tour_id=b['tour_id'], date=b['date']) for b in bookings_data]
    db.session.bulk_save_objects(bookings)
    db.session.commit()

def create_users(users_data):
    users = [User(username=u['username'], email=u['email']) for u in users_data]
    db.session.bulk_save_objects(users)
    db.session.commit()

@app.route('/tours', methods=['POST', 'GET'])
def handle_tours():
    if request.method == 'POST':
        tour_data = request.json  # Expecting a list of tours
        create_tours(tour_data)
        return jsonify({'message': f'{len(tour_data)} tours added successfully'}), 201
    
    all_tours = Tour.query.all()
    tours_data = [{'id': tour.id, 'name': tour.name, 'description': tour.description, 'price': tour.price} for tour in all_tours]
    return jsonify(tours_data)

@app.route('/bookings', methods=['POST', 'GET'])
def handle_bookings():
    if request.method == 'POST':
        booking_data = request.json  # Expecting a list of bookings
        create_bookings(booking_data)
        return jsonify({'message': f'{len(booking_data)} bookings added successfully'}), 201
    
    all_bookings = Booking.query.all()
    bookings_data = [{'id': booking.id, 'user_id': booking.user_id, 'tour_id': booking.tour_id, 'date': booking.date} for booking in all_bookings]
    return jsonify(bookings_data)

@app.route('/users', methods=['POST', 'GET'])
def handle_users():
    if request.method == 'POST':
        user_data = request.json  # Expecting a list of users
        create_users(user_command_data)
        return jsonify({'message': f'{len(user_data)} users added successfully'}), 201
    
    all_users = User.query.all()
    users_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in all_users]
    return jsonify(users_data)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)