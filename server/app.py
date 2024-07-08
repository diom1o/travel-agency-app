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
    id = db.Column(db.Integer, primary_visits=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'))
    date = db.Column(db.Date)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)

@app.route('/tours', methods=['POST', 'GET'])
def manage_tours():
    if request.method == 'POST':
        data = request.json
        new_tour = Tour(name=data['name'], description=data['description'], price=data['price'])
        db.session.add(new_tour)
        db.session.commit()
        return jsonify({'message': 'Tour added successfully'}), 201
    elif request.method == 'GET':
        tours = Tour.query.all()
        return jsonify([{'id': tour.id, 'name': tour.name, 'description': tour.description, 'price': tour.price} for tour in tours])

@app.route('/bookings', methods=['POST', 'GET'])
def manage_bookings():
    if request.method == 'POST':
        data = request.json
        new_booking = Booking(user_id=data['user_id'], tour_id=data['tour_id'], date=data['date'])
        db.session.add(new_booking)
        db.session.commit()
        return jsonify({'message': 'Booking added successfully'}), 201
    elif request.method == 'GET':
        bookings = Booking.query.all()
        return jsonify([{'id': booking.id, 'user_id': booking.user_id, 'tour_id': booking.tour_id, 'date': booking.date} for booking in bookings])

@app.route('/users', methods=['POST', 'GET'])
def manage_users():
    if request.method == 'POST':
        data = request.json
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User added successfully'}), 201
    elif request.method == 'GET':
        users = User.query.all()
        return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])

if __name__ == '__main__':
    db.createTCHA(app)
    app.run(debug=True)