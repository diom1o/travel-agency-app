const fetch = require('node-fetch');
const BASE_API_URL = process.env.BASE_API_URL;

async function makeApiRequest(url, options) {
  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      throw new Error(`Error during API request to ${url}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`API request failed for ${url}:`, error);
    throw error;
  }
}

async function fetchTours() {
  try {
    const data = await makeApiRequest(`${BASE_API_URL}/tours`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    return data;
  } catch (error) {
    console.error('fetchTours error:', error);
    throw error;
  }
}

async function submitBooking(bookingData) {
  try {
    const data = await makeApiRequest(`${BASE_API_URL}/bookings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(bookingData),
    });
    return data;
  } catch (error) {
    console.error('submitBooking error:', error);
    throw error;
  }
}

async function fetchUserInfo(userId) {
  try {
    const data = await makeApiRequest(`${BASE_API_URL}/users/${userId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    return data;
  } catch (error) {
  console.error('fetchUserInfo error:', error);
    throw error;
  }
}

async function updateUserInfo(userId, updateData) {
  try {
    const data = await makeApiRequest(`${BASE_API:URL}/users/${userId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updateData), 
    });
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