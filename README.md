Sai-Ventures

Sai-Ventures is a web-based financial data platform built with Django and React, designed to help users collect, visualize, and analyze historical stock data.

Core Features:
--------------
• Scrapes financial stock data using Python (Webscraper.py)
• Downloads and processes historical pricing info (download_data.py)
• Visualizes data via charts and statistics (viz.py)
• Backend built with Django (manage.py, views.py, urls.py, settings.py)
• Frontend built using React (App.js)
• Modular structure ready for extension into full analytics platform

Installation:
-------------
1. Clone this repository:
   git clone https://github.com/saimeda1/Sai-Ventures.git

2. Set up a virtual environment:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. Start the Django backend:
   python manage.py runserver

4. Run the frontend (navigate to frontend folder if needed):
   npm install
   npm start

Usage:
------
- Access the web app via localhost after starting backend and frontend.
- Use the scraper to collect stock data into local CSVs or a backend API.
- View visualizations by triggering data display in the React interface.

Structure:
----------
• Webscraper.py       – Extracts live or historical stock data from online sources
• download_data.py    – Pulls and saves historical data (e.g., using APIs)
• viz.py              – Generates plots (line charts, indicators)
• views.py            – Django views for serving and processing requests
• App.js              – React frontend to display and interact with data
• urls.py             – Routing for Django backend
• settings.py         – Django project settings
• manage.py           – Django entrypoint for running server and commands

Next Steps:
-----------
• Integrate database for persistent storage of data
• Add user authentication for personal portfolios
• Enhance visualization dashboard with filters and strategy tools
• Build REST APIs for dynamic client-server communication
