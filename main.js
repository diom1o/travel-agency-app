import axios from 'axios';

const apiBaseUrl = process.env.API_BASE_URL || 'http://localhost:3000/api';

async function fetchAvailableTours() {
  try {
    const response = await axios.get(`${apiBaseUrl}/tours`);
    return response.data;
  } catch (error) {
    console.error('Error fetching tours', error);
    throw error;
  }
}

function renderTours(toursList) {
  const toursContainerElement = document.getElementById('toursContainer');
  toursContainerElement.innerHTML = '';
  toursList.forEach(tour => {
    const tourItemElement = document.createElement('div');
    tourItemElement.innerHTML = `
      <h3>${tour.name}</h3>
      <p>${tour.description}</p>
      <button onclick="initiateTourBooking('${tour.id}')">Book Now</button>
    `;
    toursContainerElement.appendChild(tourItemElement);
  });
}

function initiateTourBooking(tourId) {
  const userName = prompt('Enter your name:');
  const userEmail = prompt('Enter your email:');
  processTourBooking({ tourId, userName, userEmail });
}

async function processTourBooking(bookingDetails) {
  try {
    const response = await axios.post(`${apiBaseUrl}/bookings`, bookingDetails);
    alert('Booking successful!');
    console.log('Booking confirmation:', response.data);
  } catch (error) {
    console.error('Error processing booking', error);
    alert('There was an issue processing your booking.');
  }
}

async function fetchUserBookings(userId) {
  try {
    const response = await axios.get(`${apiBaseUrl}/bookings/${userId}`);
    displayBookingsForUser(response.data);
  } catch (error) {
    console.error('Error fetching user bookings', error);
  }
}

function displayBookingsForUser(bookingsList) {
  const bookingsContainer = document.getElementById('bookingsContainer');
  bookingsContainer.innerHTML = '';
  bookingsList.forEach(booking => {
    const bookingItemElement = document.createElement('div');
    bookingItemElement.innerHTML = `
      <h4>${booking.tourName}</h4>
      <p>Date: ${booking.date}</p>
    `;
    bookingsContainer.appendChild(bookingItemElement);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  fetchAvailableTours().then(renderTours).catch(console.error);
});

window.initiateTourBooking = initiateTourBooking;
window.fetchUserBookings = fetchUserBookings;