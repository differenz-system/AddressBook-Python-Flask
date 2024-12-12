# AddressBook Flask API

## Overview
This repository contains the **Address Book** application built using **Flask**. It demonstrates design and coding practices for developing secure, efficient, and modular APIs followed by **[Differenz System](http://www.differenzsystem.com/)**. The application allows users to manage their address book, including authentication, viewing, creating, updating, and deleting contacts.

## Features
1. **User Authentication:**
   - User registration with email and password.
   - Secure login system using hashed passwords and JWT-based authentication.

2. **Contact Management:**
   - Retrieve all contacts for the logged-in user.
   - Add a new contact with details like name, email, phone number, and address.
   - Update existing contact information.
   - Delete contacts.

## Key Technologies and Tools
- **Framework:** Flask
- **Database:** MySQL
- **Authentication:** JWT
- **Password Hashing:** Bcrypt
- **Object Relational Mapper (ORM):** SQLAlchemy
- **Data Serialization:** Marshmallow
- **IDE:** Visual Studio Code

## Pre-requisites
1. [Python](https://www.python.org/) (3.8 or higher recommended).
2. [MySQL](https://www.mysql.com/) (Ensure a running instance of MySQL).
3. [Visual Studio Code](https://code.visualstudio.com/).
4. [Postman](https://www.postman.com/) or any REST client for testing API endpoints.

## Getting Started
### 1. Clone the Repository
```bash
git clone https://github.com/differenz-system/AddressBook-Python-Flask
cd AddressBook-Python-Flask
```

### 2. Set Up the Environment
1. Create a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add the following configuration:
   ```env
   # Database configuration
   DATABASE_URI=mysql+pymysql://<user>:<password>@<host>/<database>

   # Flask configuration
   FLASK_ENV=development
   SECRET_KEY=<your_secret_key>

   # JWT configuration
   JWT_SECRET_KEY=<your_jwt_secret_key>
   ```

4. Initialize the database:
   ```bash
   flask db upgrade
   ```

### 3. Start the Server
Run the Flask application:
```bash
flask run
```

The server will start at `http://127.0.0.1:5000` by default.

## API Endpoints
### User Authentication
#### Register
**POST** `/auth/register`

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com"
}
```

#### Login
**POST** `/auth/login`

**Request:**
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "token": "<JWT Token>"
}
```

### Contact Management
#### Get All Contacts
**GET** `/contacts`

**Headers:**
```http
Authorization: Bearer <JWT Token>
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "1234567890",
    "address": "123 Main St",
    "user_id": 1
  }
]
```

#### Add Contact
**POST** `/contacts`

**Headers:**
```http
Authorization: Bearer <JWT Token>
```

**Request:**
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "1234567890",
  "address": "123 Main St"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "1234567890",
  "address": "123 Main St",
  "user_id": 1
}
```

#### Update Contact
**PUT** `/contacts/<contact_id>`

**Headers:**
```http
Authorization: Bearer <JWT Token>
```

**Request:**
```json
{
  "name": "Jane Smith",
  "email": "jane.smith@example.com",
  "phone": "0987654321",
  "address": "456 Elm St"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Jane Smith",
  "email": "jane.smith@example.com",
  "phone": "0987654321",
  "address": "456 Elm St",
  "user_id": 1
}
```

#### Delete Contact
**DELETE** `/contacts/<contact_id>`

**Headers:**
```http
Authorization: Bearer <JWT Token>
```

**Response:**
```json
{
  "message": "Contact deleted"
}
```

## Troubleshooting
### Common Issues
1. **Missing Dependencies:** Ensure all dependencies in `requirements.txt` are installed.
2. **Database Connection Issues:** Verify your `.env` configuration and database credentials.
3. **JWT Token Issues:** Ensure the token is included in the request header for protected endpoints.

### Useful Commands
- **Run the server:** `flask run`
- **Initialize the database:** `flask db upgrade`
- **Activate virtual environment:** `source venv/bin/activate`

## Support
If you encounter any issues, feel free to [report an issue](https://github.com/differenz-system/AddressBook-Python-Flask/issues).
---

Happy coding!

