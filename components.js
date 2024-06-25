import React from 'react';

const TourList = ({ tours }) => {
  return (
    <div className="tour-list">
      {tours.map(tour => (
        <div key={tour.id} className="tour-item">
          <h3>{tour.name}</h3>
          <p>{tour.description}</p>
          <p>Price: {tour.price}</p>
          <button>View Details</button>
        </div>
      ))}
    </div>
  );
};

const TourDetails = ({ tour }) => {
  return (
    <div className="tour-details">
      <h2>{tour.name}</h2>
      <p>{tour.description}</p>
      <p>Price: {tour.price}</p>
      <img src={tour.imageUrl} alt={tour.name} />
      <button>Book Now</button>
    </div>
  );
};

class BookingForm extends React.Component {
  state = {
    name: '',
    email: '',
    tourId: this.props.tourId,
    date: ''
  };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  }

  handleSubmit = (event) => {
    event.preventDefault();
    console.log(this.state);
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit} className="booking-form">
        <label>Name:</label>
        <input type="text" name="name" value={this.state.name} onChange={this.handleChange} />
        <label>Email:</label>
        <input type="email" name="email" value={this.state.email} onChange={this.handleChange} />
        <label>Date:</label>
        <input type="date" name="date" value={this.state.date} onChange={this.handleChange} />
        <button type="submit">Submit</button>
      </form>
    );
  }
}

const UserBookings = ({ bookings }) => {
  return (
    <div className="user-bookings">
      <h2>Your Bookings</h2>
      {bookings.length > 0 ? (
        bookings.map(booking => (
          <div key={booking.id} className="booking-item">
            <h3>{booking.tourName}</h3>
            <p>Date: {booking.date}</p>
            <button>Cancel Booking</button>
          </div>
        ))
      ) : (
        <p>No bookings found.</p>
      )}
    </div>
  );
};

export { TourList, TourDetails, BookingForm, UserBookings };