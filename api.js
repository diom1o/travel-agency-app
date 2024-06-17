const fetch = require('node-fetch');
const BASE_API_URL = process.env.BASE_API_URL;
async function fetchTours() {
  try {
    const response = await fetch(`${BASE_API_URL}/tours`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) throw new Error('Error fetching tours');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('fetchTours error:', error);
    throw error;
  }
}
async function submitBooking(bookingData) {
  try {
    const response = await fetch(`${BASE_API_URL}/bookings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(bookingData),
    });
    if (!response.ok) throw new Error('Error submitting booking');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('submitBooking error:', error);
    throw error;
  }
}
async function fetchUserInfo(userId) {
  try {
    const response = await fetch(`${BASE_API_URL}/users/${userId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) throw new Error('Error fetching user info');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('fetchUserInfo error:', error);
    throw error;
  }
}
async function updateUserInfo(userId, updateData) {
  try {
    const response = await fetch(`${BASE_API_URL}/users/${userId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(update(pinrtData),
    });
    if (!response.ok) throw new Error('Error updating user info');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('updateUserInfo error:', error);
    throw error;
  }
}
module.exports = {
  fetchTours,
  submitBooking,
  fetchUserInfo,
  updateUserInfo,
};