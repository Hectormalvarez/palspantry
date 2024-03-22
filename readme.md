# Pals Pantry Telegram Store Project Instructions

## 1. Project Setup with Docker Compose

- Clone the repository: `git clone https://github.com/Hectormalvarez/palspantry.git`
- Set up environment variables (see `.env.example`)
- Run the project with Docker Compose: `docker-compose up`

## 2. Project Overview

This project combines a Django Rest Framework API with a Python-Telegram-Bot Library to create a convenient and accessible grocery shopping experience.

### Django Rest Framework API

The Django Rest Framework API provides the storage layer via api backed by a postgresql database.

### Telegram Bot

The Telegram bot acts as an interface for users to browse products, place orders, and communicate with store owners.

## 3. Instructions for Use

### Users

1. Send a start message to the Telegram bot.
2. Follow the on-screen instructions to register and authenticate.
3. Browse products and add them to your cart.
4. Place an order and complete the payment process.
5. Communicate with store owners directly through the Telegram bot.

### Store Owner

1. Send a start message to the Telegram bot.
2. Follow the on-screen instructions to register and authenticate.

#### Manage your store's inventory, orders, and communicate with customers directly through the Telegram bot

- **Inventory Management:** Add, edit, and remove products from your inventory. Manage stock levels and track product availability.
- **Order Management:** Process orders, track their status, and update customers on the latest information.
- **Customer Communication:** Chat with customers in real-time to answer their queries, provide support, and build relationships. Send personalized messages and offers to engage customers and drive sales.

## Getting Started

1. Clone the repository.
2. Install dependencies.
3. Set up environment variables.
4. Run `docker-compose up` to start the project.
5. Connect your Telegram bot and start interacting!

## Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a branch for your changes
3. Make your changes and add tests
4. Submit a pull request

## License

Pals Pantry Telegram Store is licensed under the MIT License.

## Acknowledgements

- Thank you to the developers of Python, Django, PostgreSQL, python-telegram-bot, and Docker Compose for making this project possible!
- Special thanks to the community for their support and contributions.

### Feedback and Contact Information

- TODO
