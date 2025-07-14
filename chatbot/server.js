const express = require('express');
const path = require('path');
const mongoose = require('mongoose'); 
const bodyParser = require('body-parser');
const axios = require("axios");
const app = express();
//const PORT = 3000;
const cors = require("cors");

// Middleware to parse JSON and URL-encoded data
app.use(express.json());
app.use(cors());
app.use(express.urlencoded({ extended: true }));

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/talkbots', {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
    .then(() => console.log('Connected to MongoDB'))
    .catch(err => console.error('Could not connect to MongoDB:', err));

// Define the user schema and model
const userSchema = new mongoose.Schema({
    username: String,
    email: String,
    password: String
});

const User = mongoose.model('User', userSchema); // Create a model for users

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));

// Route for index page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public/index.html'));
});

// Route for signup page
app.get('/signup', (req, res) => {
    res.sendFile(path.join(__dirname, 'public/signup.html'));
});


// Handle signup form submission
app.post('/signup_process', async (req, res) => {
    const { username, email, password } = req.body;

    try {
        // Check if a user with the exact username, email, and password exists
        const existingUser = await User.findOne({ username, email, password });
        if (existingUser) {
            // If the user already exists with the same details, redirect to chat.html
            return res.send(`
                <script>
                    alert('User already exists! Redirecting to chat.');
                    window.location.href = '/chat';
                </script>
            `);
        }

        // Save new user to the database if any field does not match
        const newUser = new User({ username, email, password });
        await newUser.save();

        console.log('New user signed up:', newUser);
        // Redirect to chat.html after successful signup
        res.send(`
            <script>
                alert('Signup successful! Redirecting to chat.');
                window.location.href = '/chat';
            </script>
        `);
    } catch (error) {
        console.error('Error during signup:', error);
        res.status(500).send('Internal Server Error');
    }
});


app.post("/chat", async (req, res) => {
    const { msg } = req.body;
  
    try {
      // Send message to Flask API and get response
      const response = await axios.post("http://localhost:5000/chat", { msg });
      const botResponse = response.data.response;
      res.json({ response: botResponse });
    } catch (error) {
      console.error("Error connecting to chatbot API:", error);
      res.status(500).json({ error: "Chatbot service unavailable." });
    }

    try {
        const flaskResponse = await axios.post("http://localhost:5000/chat", {
          msg: req.body.msg,
        });
        res.json({ response: flaskResponse.data.response });
      } catch (error) {
        console.error("Error connecting to Flask:", error);
        res.status(500).send("Error forwarding request to Flask.");
      }
  });

// Placeholder for chatbots page
app.get('/chat', (req, res) => {
    res.sendFile(path.join(__dirname, 'public/chat.html'));
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
