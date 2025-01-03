# connecto

# Social Media Clone

## Project Overview

Connecto is a social media platform designed to replicate key features of modern social media applications. This project focuses on backend architecture, interactions, and applying essential concepts such as database schema design, Hashing Passwd, routing, authentication(JWT), authorization, and more.

---

## Features

### Core Features

- **User Profiles**:
  - Create, view, edit, and delete user profiles.
- **Post Feeds**:
  - Create, view, update, delete, and interact with posts.
- **Pagination**:
  - Efficiently load feed data with limited items per request.

---

## Tech Stack

### Backend

- **Framework**: Flask
- **Database**: SQLite
- **ORM**: SQLAlchemy

### Tools and Libraries

- **Environment Management**: virtualenv

---

## Installation and Setup

### Prerequisites

Ensure the following are installed on your system:

- Python 3.8+
- SQLite
- Flask

### Steps to Run

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/connecto.git
   cd connecto
   ```

2. **Set Up Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file with the following:

   ```env
   SECRET_KEY=your_secret_key
   ```

5. **Run Database Migrations**:

   ```bash
   flask db upgrade
   ```

6. **Start the Application**:

   ```bash
   python mars/run.py
   ```

---

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── user_models.py  # User-related APIs
│   │   ├── post_models.py  # Post-related
│   ├── routes/
│   │   ├── user_routes.py  # User-related APIs
│   │   ├── post_routes.py  # Post-related
|
utility functions
├── migrations/  # Database migrations
├── .env         # Environment variables
├── requirements.txt  # Python dependencies
├── README.md    # Project documentation
└── run.py       # Entry point for the application
```

---

## API Endpoints

### Authentication

- **POST** `/users/register`: Register a new user.
- **POST** `/users/login`: Login a user.

### User Profiles

- **GET** `/users/<id>`: Retrieve a Specific user profile.
- **PUT** `/users/<id>`: Update a user profile.
- **DELETE** `/users/<id>`: Delete a user profile.
- **GET** `/users/`: Retrieve all Users

### Posts

- **GET** `/posts`: Retrieve all posts (paginated).
- **POST** `/posts`: Create a new post.
- **GET** `/posts/<id>`: Retrieve a specific post.
- **PUT** `/posts/<id>`: Update a post.
- **DELETE** `/posts/<id>`: Delete a post.

### Interactions

- **POST** `/posts/<id>/like`: Like a post.
- **POST** `/posts/<id>/comment`: Comment on a post.

--

## Future Enhancements

- Implement real-time updates for feeds and notifications using WebSockets.
- Add support for multimedia posts (videos).
- Async Email notification on Sucessfull registration .
- Enhance security features (OAuth, 2FA).
- Follow / unfollow users Feature (m:m Relationship)
- Rate limiters
- API versioning
- Optimize database performance with indexing.

## Contribution

Feel free to fork this repository and submit pull requests. For major changes, open an issue first to discuss what you would like to change.

---

## Contact

For any questions or feedback, please reach out at [prawinrahul1411@gmail.com].
'
