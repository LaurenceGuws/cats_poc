// Initialize cat cards when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
  console.log('Document fully loaded. Initializing cat cards.');
  initializeCatCards();
});

// Function to attach event listeners to each cat card
function initializeCatCards() {
  console.log('Entering initializeCatCards function.');
  const catCards = document.querySelectorAll('.cat-card');
  
  catCards.forEach((card) => {
    card.addEventListener('click', function(event) {
      console.log('Cat card clicked. Handling click event.');
      handleCatCardClick(card, event);
    });
  });

  console.log('Exiting initializeCatCards function.');
}

// Function to handle clicks on individual cat cards
function handleCatCardClick(card, event) {
  console.log('Entering handleCatCardClick function.');

  // Stop propagation if form elements are interacted with
  if (['INPUT', 'LABEL', 'BUTTON'].includes(event.target.tagName)) {
    console.log('Form element interaction detected. Stopping propagation.');
    event.stopPropagation();
    return;
  }

  const originalInnerHTML = card.innerHTML;
  const catData = extractCatData(card);

  console.log('Extracted cat data:', catData);

  const form = createForm(catData);
  card.innerHTML = '';
  card.appendChild(form);

  console.log('Form added to card. Handling form buttons.');
  
  handleFormButtons(form, card, originalInnerHTML, catData);
  console.log('Exiting handleCatCardClick function.');
}

// Function to handle Submit and Cancel buttons on the form
function handleFormButtons(form, card, originalInnerHTML, catData) {
  console.log('Entering handleFormButtons function.');

  const submitButton = form.querySelector('#submit-button');
  const cancelButton = form.querySelector('#cancel-button');

  submitButton.addEventListener('click', function(event) {
    console.log('Submit button clicked.');
    event.preventDefault();

    const updatedData = extractUpdatedData(form, catData);
    console.log('Extracted updated data:', updatedData);

    if (Object.keys(updatedData).length > 0) {
      console.log('Sending update request.');
      sendUpdateRequest(catData, updatedData);
    }

    console.log('Restoring original card content.');
    card.innerHTML = originalInnerHTML;
    initializeCatCards();
  });

  cancelButton.addEventListener('click', function(event) {
    console.log('Cancel button clicked. Restoring original card content.');
    event.preventDefault();
    card.innerHTML = originalInnerHTML;
    initializeCatCards();
  });

  console.log('Exiting handleFormButtons function.');
}

// Function to extract data attributes from the cat card
function extractCatData(card) {
  console.log('Entering extractCatData function.');
  
  const catData = {};
  for (let attribute of card.attributes) {
    if (attribute.name.startsWith('data-cat-')) {
      const key = attribute.name.replace('data-cat-', '');
      catData[key] = attribute.value;
    }
  }

  console.log('Exiting extractCatData function.');
  return catData;
}

// Function to create a form based on the cat data
function createForm(catData) {
  console.log('Entering createForm function.');
  
  const form = document.createElement('form');
  form.id = 'updateForm';

  for (const key in catData) {
    const input = document.createElement('input');
    input.name = key;
    input.value = catData[key];
    form.appendChild(input);
  }

  const submitButton = document.createElement('button');
  submitButton.id = 'submit-button';
  submitButton.innerText = 'Submit';
  form.appendChild(submitButton);

  const cancelButton = document.createElement('button');
  cancelButton.id = 'cancel-button';
  cancelButton.innerText = 'Cancel';
  form.appendChild(cancelButton);

  console.log('Exiting createForm function.');
  return form;
}

// Function to extract any updated data from the form
function extractUpdatedData(form, originalData) {
  console.log('Entering extractUpdatedData function.');
  
  const formData = new FormData(form);
  const updatedData = {};

  formData.forEach((value, key) => {
    if (originalData[key] !== value) {
      updatedData[key] = value;
    }
  });

  console.log('Exiting extractUpdatedData function.');
  return updatedData;
}

// Function to send the update request to the server
function sendUpdateRequest(originalData, updatedData) {
  console.log('Entering sendUpdateRequest function.');

    // Make sure to capture the original cat name correctly
    const originalCatName = originalData['name'];  // Assuming the key for the cat name in originalData is 'name'
  
    const payload = JSON.stringify({cat_name: originalCatName, ...updatedData});
    console.log('Prepared payload:', payload);

  fetch('/update_cat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: payload
  })
  .then(response => {
    console.log('Received server response:', response);
    return response.json();
  })
  .then(data => {
    if (data.message === 'Cat updated successfully') {
      console.log('Cat update was successful. Page reloading');
      window.location.reload();
    } else {
      console.log('Failed to update cat.');
    }
  })
  .catch(error => {
    console.log('An error occurred:', error);
  });

  console.log('Exiting sendUpdateRequest function.');
}
