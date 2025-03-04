document.addEventListener('DOMContentLoaded', function() {
  const buttons = document.querySelectorAll('.toggle-btn');
  const selectedValueDisplay = document.getElementById('selected-value');
  let selectedValue = null;

  buttons.forEach(button => {
      button.addEventListener('click', function() {
          // Remove active class from all buttons
          buttons.forEach(btn => btn.classList.remove('active'));
          
          // Add active class to clicked button
          this.classList.add('active');
          
          // Store the selected value
          selectedValue = this.getAttribute('data-value');
          
          // Display the selected value (optional)
          setStatus(this.getAttribute('data-value'));
          
          // You can also trigger other actions based on the selection
          console.log(`Option selected: ${selectedValue}`);
      });
  });
});

function setStatus(ID) {
  const url = '/status';
  const data = {
      "SelectedState": ID // Literally just send the back -end the ID
  };

  const options = {
      method: 'PUT', // Specify the HTTP method as PUT
      headers: {
          'Content-Type': 'application/json' // Specify content type as JSON
      },
      body: JSON.stringify(data) // Convert data to JSON string
  };

  fetch(url, options)
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          return response.json(); // Parse response JSON
      })
      .then(data => {
          console.log(data);
      })
      .catch(error => {
          console.error('There was a problem with the PUT request:', error);
      });

}