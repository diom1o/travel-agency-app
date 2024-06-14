import axios from 'axios';

const apiBaseUrl = process.env.API_BASE_URL || 'http://localhost:3000/api';

async function fetchAvailableTours() {
  try {
    const response = await axios.get(`${apiBaseUrl}/tours`);
    return response.data;
  } catch (error) {
    const errorMessage = error.response && error.response.data ? `Error fetching tours: ${error.response.data.message}` : 'Error fetching tours';
    console.error(errorMessage, error);
    alert(errorMessage);
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
  if (!userName || !userEmail) {
    alert('You must enter both name and email to book a tour!');
    return;
  }
  processTourBooking({ tourId, userName, userEmail });
}

async function processTourBooking(bookingDetails) {
  try {
    const response = await axios.post(`${apiBaseUrl}/bookings`, bookingDetails);
    alert('Booking successful!');
    console.log('Booking confirmation:', response.data);
  } catch (error) {
    const errorMessage = error.response && error.response.data ? `Error processing booking: ${error.response.data.message}` : 'There was an issue processing your booking.';
    console.error(errorMessage, error);
    alert(errorMessage);
  }
}

async function fetchUserBookings(userId) {
  try {
    const response = await axios.get(`${apiBaseUrl}/bookings/${userId}`);
    displayBookingsForUser(response.data);
  } catch (error) {
    const errorMessage = error.response && error.response.data ? `Error fetching user bookings: ${error.response.data.message}` : 'Error fetching user bookings';
    console.error(errorMessage, error);
    alert(errorMessage);
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
    bookingsContainer.appendChild(bookingItemDetail);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  fetchAvailableTours().then(renderTours).catch(error => {
    console.error('Failed to fetch tours on document load', error);
    alert('Failed to load tours. Please try refreshing the page.');
  });
});

window.initiateTourBooking = initiateTourBooking;
window.fetchUserBookings = fetchUserBookings;