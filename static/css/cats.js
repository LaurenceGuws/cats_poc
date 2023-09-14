document.addEventListener("DOMContentLoaded", function() {
  console.log('Document loaded, initializing cat cards.');
  const catCards = document.querySelectorAll('.cat-card');

  catCards.forEach((card) => {
    let originalInnerHTML = card.innerHTML; // Save the original content of the card

    card.addEventListener('click', function(event) {
      console.log('Cat card clicked.');
      
      // Prevent the form from disappearing when we are interacting with its elements
      if (event.target.tagName === 'INPUT' || event.target.tagName === 'LABEL' || event.target.tagName === 'BUTTON') {
        console.log('Form interaction detected, stopping propagation.');
        event.stopPropagation();
        return;
      }

      const catData = {};
      for (let attribute of card.attributes) {
        if (attribute.name.startsWith('data-cat-')) {
          const key = attribute.name.replace('data-cat-', '');
          catData[key] = attribute.value;
        }
      }
      console.log('Cat data extracted:', catData);

      const form = document.createElement('form');
      form.id = 'updateForm';
      console.log('Form created.');
      
      Object.keys(catData).forEach(key => {
        const input = document.createElement('input');
        input.name = key;
        input.value = catData[key];
        form.appendChild(input);
      });
      console.log('Form fields added.');

      const submitButton = document.createElement('button');
      submitButton.id = 'submit-button';
      submitButton.innerText = 'Submit';
      form.appendChild(submitButton);

      // Add a Cancel button
      const cancelButton = document.createElement('button');
      cancelButton.id = 'cancel-button';
      cancelButton.innerText = 'Cancel';
      form.appendChild(cancelButton);

      card.innerHTML = ''; // Clear the card content
      card.appendChild(form); // Add the form
      console.log('Form appended to card.');

      // Handle Submit button click
      submitButton.addEventListener('click', function(event) {
        console.log('Submit button clicked.');
        event.preventDefault();

        const formData = new FormData(form);

        const updatedData = {};
        formData.forEach((value, key) => {
          if (catData[key] !== value) {
            updatedData[key] = value;
          }
        });
        console.log('Updated data:', updatedData);

        if (Object.keys(updatedData).length > 0) {
          console.log('Sending update request.');
          fetch('/update_cat', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({cat_name: catData['Name'], ...updatedData})
          })
          .then(response => response.json())
          .then(data => {
            if (data.message === 'Cat updated successfully') {
              console.log('Cat updated successfully. Reloading page.');
              window.location.reload();
            } else {
              console.log('Failed to update cat');
            }
          })
          .catch(error => {
            console.log('Error:', error);
          });
        }

        card.innerHTML = originalInnerHTML; // Revert back to the original content
      });

      // Handle Cancel button click
      cancelButton.addEventListener('click', function(event) {
        console.log('Cancel button clicked.');
        event.preventDefault();
        card.innerHTML = originalInnerHTML; // Revert back to the original content
      });
    });
  });
});
