/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      await loginUser(email, password);
    });
  }
});

async function loginUser(email, password) {
  const response = await fetch('https://your-api-url/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
  });
  // Handle the response
  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } else {
    alert('Login failed: ' + response.statusText);
  }
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
      loginLink.style.display = 'block';
  } else {
      loginLink.style.display = 'none';
      // Fetch places data if the user is authenticated
      fetchPlaces(token);
  }
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}


async function fetchPlaces(token) {
  // Make a GET request to fetch places data
    const response = await fetch('https://your-api-url/login', {
        headers: {
            'Content-Type': 'application/json'
        },
    });
    if (response.ok) {
      const places = await response.json();
      displayPlaces(places);
    } else {
      console.error('Error :', response.statusText);
  }
}


  // Include the token in the Authorization header
  // Handle the response and pass the data to displayPlaces function


function displayPlaces(places) {
  // Clear the current content of the places list
  const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';
  // Iterate over the places data
  // For each place, create a div element and set its content
  places.forEach(place => {
    const placeCard = document.createElement('div');
    placeCard.classList.add('place-card');
    placesList.appendChild(placeCard);
  });
  // Append the created element to the places list
}

document.getElementById('price-filter').addEventListener('change', function(event) {
  const selectedPrice = event.target.value;
  const places = document.querySelectorAll('.place-card');

  places.forEach(function(place) {
      const price = parseInt(place.querySelector('.place-price').textContent);
      place.style.display = (selectedPrice === 'All' || price <= selectedPrice) ? 'block' : 'none';
  });
});

function getPlaceIdFromURL() {
  // Extract the place ID from window.location.search
  // Your code here
}

function checkAuthentication() {
  const token = getCookie('token');
  const addReviewSection = document.getElementById('add-review');

  if (!token) {
      addReviewSection.style.display = 'none';
  } else {
      addReviewSection.style.display = 'block';
      // Store the token for later use
      const placeId = getPlaceIdFromURL();
      fetchPlaceDetails(token, placeId);
  }
}

function getCookie(name) {
  // Function to get a cookie value by its name
  // Your code here
  const output = document.getElementById("cookies");
  output.textContent = `> ${document.cookie}`;
}

async function fetchPlaceDetails(token, placeId) {
  // Make a GET request to fetch place details
    const response = await fetch(`https://your-api-url/places/${placeId}`, {
      headers: {
          'Content-Type': 'application/json',
      }
    });
    if (response.ok) {
      const place = await response.json();
      displayPlaceDetails(place);
    } else {
      console.error('Error API :', response.statusText);
      alert('Error');
}

  // Include the token in the Authorization header
  // Handle the response and pass the data to displayPlaceDetails function
}

function displayPlaceDetails(place) {
  // Clear the current content of the place details section
  // Create elements to display the place details (name, description, price, amenities and reviews)
  // Append the created elements to the place details section
}