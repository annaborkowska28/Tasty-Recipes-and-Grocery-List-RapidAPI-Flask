## Overview
Tasty Recipes and Grocery List is a web application that fetches and displays recipes from the Tasty API. Users can view detailed recipes, contact the app creator, and generate a grocery list that sums up quantities of ingredients from multiple recipes. The app uses Flask for the backend, Bootstrap for styling, and allows users to manage and view their aggregated grocery lists.


## Features
- Home Page: Displays a list of recipes fetched from the Tasty API.
- Recipe Details: Shows detailed ingredients for individual recipes.
- Add to Grocery List: Allows users to add ingredients from different recipes to a combined grocery list, summing up quantities of the same ingredients.
-  View Grocery List: Displays the aggregated grocery list with summed quantities of ingredients.
- Contact Page: Users can send messages to the app creator via email.

## Technologies Used:
- Flask: To create and manage web routes and handle HTTP requests.

- Jinja2: For rendering dynamic HTML templates.

- Python: For backend logic and data processing.

- HTML & Bootstrap: To create responsive and styled web pages.

- requests: To fetch data from the Tasty API.

- smtplib: For sending emails.

- python-dotenv: To manage environment variables securely.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## ## 🔐 API and Environment Configuration

### How to get an API key?
1. Sign up or log in to [RapidAPI](https://rapidapi.com/auth?referral=hub).
2. Search for **Tasty API** and subscribe to a plan.
3. Copy your **API key** and paste it into the `.env` file.


To run the application, create a `.env` file in the main directory and add your own credentials



