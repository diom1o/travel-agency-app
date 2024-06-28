import React, { useState, useEffect, useCallback } from 'react';

const logEvent = (message) => {
  console.log(message);
};

const TourList = ({ tours }) => {
  const handleItemClick = useCallback((tourName) => logEvent(`Showing details for ${tourName}`), []);

  if (!tours || tours.length === 0) {
    return <p>Error: No tours data available.</p>;
  }

  return (
    <div className="tour-list">
      {tours.map((tour) => (
        <div key={tour.id} className="tour-item" onClick={() => handleItemClick(tour.name)}>
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
  useEffect(() => {
    if (!tour) {
      console.error("Error: Tour details are missing.");
      return;
    }
    logEvent(`Viewing details of ${tour.name}`);
  }, [tour]);

  if (!tour) {
    return <p>Error: No tour details found.</p>;
  }

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

const BookingForm = ({ tourId }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    tourId: tourId,
    date: '',
  });

  const handleChange = useCallback((event) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
  }, [formData]);

  const handleSubmit = useCallback((event) => {
    event.preventDefault();
    if (formData.name === '' || formData.email === '' || formData.date === '') {
      console.error("Error: All fields are required to submit the booking.");
      return;
    }
    logEvent(`Booking submitted: ${JSON.stringify(formData)}`);
  }, [formData]);

  return (
    <form onSubmit={handleSubmit} className="booking-form">
      <label>Name:</label>
      <input type="text" name="name" value={formData.name} onChange={handleChange} />
      <label>Email:</label>
      <input type="email" name="email" value={formData.email} onChange={handleChange} />
      <label>Date:</label>
      <input type="date" name="date" value={formData.date} onChange={handleChange} />
      <button type="submit">Submit</button>
    </form>
  );
};

const UserBookings = ({ bookings }) => {
  const handleCancel = useCallback((bookingName) => {
    logEvent(`Canceling booking: ${bookingName}`);
  }, []);

  if (!bookings || bookings.length === 0) {
    return <p>No bookings found.</p>;
  }

  return (
    <div className="user-bookings">
      <h2>Your Bookings</h2>
      {bookings.map((booking) => (
        <div key={booking.id} className="booking-item">
          <h3>{booking.tourName}</h3>
          <p>Date: {booking.date}</p>
          <button onClick={() => handleCancel(booking.tourName)}>Cancel Booking</button>
        </div>
      ))}
    </div>
  );
};

export { TourList, TourDetails, BookingForm, UserBookings };