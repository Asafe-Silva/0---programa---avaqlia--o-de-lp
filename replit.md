# Registo de Cliques

## Overview
A simple Flask application for tracking button clicks. Users can click one of four buttons and the application records each click with:
- Button name
- Sequential click number for the day
- Date and time

## Project Structure
- `app.py` - Main Flask application with routes and SQLite database logic
- `templates/index.html` - Frontend HTML template
- `static/style.css` - Styling for the application
- `static/script.js` - Frontend JavaScript for button click handling and dark/light mode toggle
- `database.db` - SQLite database file storing click records

## Running the Application
The app runs on port 5000 using the configured workflow:
```
python app.py
```

## Database Schema
The application uses SQLite with a single table:
- **cliques**: id, botao (button name), sequencial (daily sequence number), data (date), hora (time)

## Features
- Track button clicks with timestamps
- Daily sequential numbering
- Dark/Light mode toggle
