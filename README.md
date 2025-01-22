# Mini Price Tracker

## Project Description
Mini Price Tracker is a Telegram bot that allows users to track prices of various products in different online stores. Users can add items to their tracking list, and the bot automatically checks their prices. If the price changes, the bot instantly sends a notification to the user 📈🌟🔔

The bot offers a wide range of features, including adding and removing items from the tracking list, viewing current prices, and automatic price monitoring using specialized parsers for different stores. This tool is convenient for users who want to save time and always be up to date with price changes 🔢🚀🔐

The project is built with the following technologies. The main logic is written in Python. The Telegram bot is created using the **aiogram** library. Asynchronous data parsing is implemented with **aiohttp**. **SQLAlchemy** is used for working with the database, while **asyncpg** is the driver for **PostgreSQL**. The project is based on an asynchronous architecture to ensure high performance and fast response to requests 📊🛠️🔧

---

## How to Deploy the Project
### 1. Clone the Repository
```bash
git clone <https://github.com/AndrewEndy/mini-price-tracker.git>
cd mini_price_tracker
```

### 2. Set Up the Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # For Linux/MacOS
venv\Scripts\activate   # For Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up the Database
- Create a PostgreSQL database.
- Configure the `.env` file by specifying the database access credentials and the Telegram bot token.

### 5. Run the Bot
```bash
python aiogram_run.py
```

---

## Future Plans
- Expand support for new online stores 🛒
- Implement advanced price analytics 📊
- Provide more interaction with products 🔄
- Offer more detailed product information 📋

---

## Author
This project was created to track prices and make it easier for users. If you have any questions or suggestions, feel free to contact me! 📚🌐

GitHub: [https://github.com/AndrewEndy](https://github.com/AndrewEndy)  
Email: andrijpastuh@gmail.com

---
