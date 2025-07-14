document.addEventListener("DOMContentLoaded", () => {
    const signupForm = document.getElementById("signupForm");
    const emailInput = document.getElementById("email");
    const errorMessage = document.getElementById("error-message");
  
    signupForm.addEventListener("submit", (e) => {
      const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      if (!emailPattern.test(emailInput.value)) {
        e.preventDefault();
        errorMessage.style.display = "block";
      } else {
        errorMessage.style.display = "none";
      }
    });
  });
  
  // Assuming we store the login status in localStorage or sessionStorage
// Set login status as 'true' or 'false' (this can be updated on login/logout actions)

// Check if the user is logged in
function checkLogin(chatbot) {
    const isLoggedIn = localStorage.getItem('isLoggedIn'); // Check if the user is logged in (stored as 'true' or 'false')
  
    if (isLoggedIn === 'true') {
      // Redirect to the chatbot website if the user is logged in
      let chatbotURL = '';
  
      if (chatbot === 'learningBot') {
        chatbotURL = 'http://127.0.0.1:5001/';
      } else if (chatbot === 'translatorBot') {
        chatbotURL = 'http://127.0.0.1:5002/';
      } else if (chatbot === 'generalBot') {
        chatbotURL = 'http://127.0.0.1:5000/';
      }
  
      window.location.href = chatbotURL; // Redirect to the selected chatbot URL
    } else {
      // Redirect to login page if not logged in
      alert("You need to log in first!");
      window.location.href = "login.html"; // Redirect to login page
    }
  }
  