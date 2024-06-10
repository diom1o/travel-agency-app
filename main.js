import axios from 'axios';
const apiBaseUrl = process.env.API_BASE_URL || 'http://localhost:3000/api';
async function fetchTours() {
  try {
    const response = await axios.get(`${apiBaseUrl}/tours`);
    return response.data;
  } catch (error) {
    console.error('Error fetching tours', error);
    throw error;
  }
}
function displayTours(tours) {
  const toursContainer = document.getElementById('toursContainer');
  toursContainer.innerHTML = '';
  tours.forEach(tour => {
    const tourElement = document.createElement('div');
    tourElement.innerHTML = `
      <h3>${tour.name}</h3>
      <p>${tour.description}</p>
      <button onclick="bookTour('${tour.id}')">Book Now</button>
    `;
    toursContainer.appendChild(tourElement);
  });
}
function bookTour(tourId) {
  const userName = prompt('Enter your name:');
  const userEmail = prompt('Enter your email:');
  submitBooking({ tourId, userName, userEmail });
}
async function submitBooking(bookingDetails) {
  try {
    const response = await axios.post(`${apiBaseUrl}/bookings`, bookingDetails);
    alert('Booking successful!');
    console.log('Booking response:', response.data);
  } catch (error) {
    console.error('Error submitting booking', error);
    alert('There was an error with your booking.');
  }
}
async function manageBookings(userId) {
  try {
    const response = await axios.get(`${apiBaseUrl}/bookings/${userId}`);
    displayUserBookings(response.data);
  } catch (error) {
    console.error('Error fetching user bookings', error);
  }
}
function displayUserBookings(bookings) {
  const bookingsContainer = document.getElementById('bookingsContainer');
  bookingsContainer.innerHTML = '';
  bookings.forEach(booking => {
    const bookingElement = document.createElement('div');
    bookingOngoing.innerHTML = `
      <h4>${booking.tourName}</h4>
      <p>Date: ${booking.date}</p>
    `;
    bookingsContainer.appendChild(bookingElement);
  });
}
document.addEventListener('DOMContentLoaded', () => {
  fetchTours().then(displayTours).catch(console.error);
});
window.bookTour = bookTour;
window.manageBookings = manageBookings;