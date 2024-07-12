from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Float)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'))
    date = db.Column(db.Date)

class User(db.Model):
    id = db.Column(db.Integer, primaryKey=True)  
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)

@app.route('/tours', methods=['POST', 'GET'])
def handle_tours():
    if request.method == 'POST':
        tour_info = request.json
        new_tour = Tour(name=tour_info['name'], description=tour_info['description'], price=tour_info['price'])
        db.session.add(new_tour)
        db.session.commit()
        return jsonify({'message': 'Tour added successfully'}), 201
    elif request.method == 'GET':
        all_tours = Tour.query.all()
        tours_data = [{'id': tour.id, 'name': tour.name, 'description': tour.description, 'price': tour.price} for tour in all_tours]
        return jsonify(tours_data)

@app.route('/bookings', methods=['POST', 'GET'])
def handle_bookings():
    if request.method == 'POST':
        booking_info = request.json
        new_booking = Booking(user_id=booking_info['user_id'], tour_id=booking_info['tour_id'], date=booking_info['date'])
        db.session.add(new_booking)
        db.session.commit()
        return jsonify({'message': 'Booking added successfully'}), 201
    elif request.method == 'GET':
        all_bookings = Booking.query.all()
        bookings_data = [{'id': booking.id, 'user_id': booking.user_id, 'tour_id': booking.tour_id, 'date': booking.date} for booking in all_bookings]
        return jsonify(bookings_data)

@app.route('/users', methods=['POST', 'GET'])
def handle_users():
    if request.method == 'POST':
        user_info = request.json
        new_user = User(username=user_info['username'], email=user_info['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User added successfully'}), 201
    elif request.method == 'GET':
        all_users = User.query.all()
        users_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in all_users]
        return jsonify(users_data)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)