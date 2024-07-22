import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Tour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

@app.route('/tours', methods=['POST'])
def create_tour():
    data = request.json
    new_tour = Tour(title=data['title'], description=data['description'], price=data['price'])
    db.session.add(new_tour)
    db.session.commit()
    return jsonify({'message': 'Tour created successfully.'}), 201

@app.route('/tours', methods=['GET'])
def get_tours():
    tours = Tour.query.all()
    return jsonify([{'title': tour.title, 'description': tour.description, 'price': tour.price} for tour in tours])

@app.route('/tours/<int:id>', methods=['PUT'])
def update_tour(id):
    tour = Tour.query.get_or_404(id)
    data = request.json
    tour.title = data['title']
    tour.description = data['description']
    tour.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Tour updated successfully.'})

@app.route('/tours/<int:id>', methods=['DELETE'])
def delete_tour(id):
    tour = Tour.query.get_or_404(id)
    db.session.delete(tour)
    db.session.commit()
    return jsonify({'message': 'Tour deleted successfully.'})

@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.json
    new_booking = Booking(user_id=data['user_id'], tour_id=data['tour_id'], date=data['date'])
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'message': 'Booking created successfully.'}), 201

@app.route('/bookings/<int:id>', methods=['DELETE'])
def delete_booking(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking deleted successfully.'})

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully.'}), 201

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    user.name = data['name']
    user.email = data['email']
    db.session.commit()
    return jsonify({'message': 'User updated successfully.'})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully.'})

if __name__ == '__main__':
    db.createAll()
    app.run(debug=True)