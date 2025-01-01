# Social Media Clone

## Project Overview
A Social Media Clone designed to replicate key features of a modern social media platform, focusing on scalability, interactions, and backend architecture. This project serves as a learning experience to apply advanced backend concepts like database relationships, caching, asynchronous processing, and more.

---

## Features

### Core Features
- **User Profiles**:
  - Create, view, and edit user profiles.
- **Follow/Unfollow**:
  - Follow or unfollow other users.
- **Post Feeds**:
  - Create, view, and interact with posts.

### Interactions
- **Like and Comment**:
  - Like and comment on posts to engage with content.

### Advanced Features
- **Pagination**:
  - Efficiently load feed data with limited items per request.
- **Caching**:
  - Use Redis to optimize data delivery for feeds and frequent queries.
- **Email Notifications**:
  - Send async email notifications (e.g., on user registration) using Celery.
- **Rate Limiting**:
  - Prevent abuse with API rate limiting mechanisms.

---

## Tech Stack

### Backend
- **Framework**: Flask / Flask-RESTful
- **Database**: MySQL or PostgreSQL
- **ORM**: SQLAlchemy
- **Caching**: Redis
- **Asynchronous Processing**: Celery + Redis
- **Rate Limiting**: Flask-Limiter

### Tools and Libraries
- **Testing**: pytest
- **Environment Management**: Docker / virtualenv

---

## Installation and Setup

### Prerequisites
Ensure the following are installed on your system:
- Python 3.8+
- MySQL or PostgreSQL
- Redis
- Docker (optional, for containerization)

### Steps to Run

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/social-media-clone.git
   cd social-media-clone
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
   DATABASE_URL=mysql+pymysql://username:password@localhost/social_media_db
   SECRET_KEY=your_secret_key
   REDIS_URL=redis://localhost:6379/0
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/0
   ```

5. **Run Database Migrations**:
   ```bash
   flask db upgrade
   ```

6. **Start the Application**:
   ```bash
   flask run
   ```

7. **Start Celery Worker (Async Tasks)**:
   ```bash
   celery -A mars.celery worker --loglevel=info
   ```

---

## Project Structure
```
.
├── mars/  # Backend directory
│   ├── __init__.py
│   ├── models.py  # Database models
│   ├── routes/
│   │   ├── auth_routes.py  # Authentication APIs
│   │   ├── user_routes.py  # User-related APIs
│   │   ├── post_routes.py  # Post-related APIs
│   └── services/  # Business logic and utility functions
├── migrations/  # Database migrations
├── tests/       # Unit tests
├── .env         # Environment variables
├── requirements.txt  # Python dependencies
├── README.md    # Project documentation
└── run.py       # Entry point for the application
```

---

## API Endpoints

### Authentication
- **POST** `/register`: Register a new user.
- **POST** `/login`: Login a user.

### User Profiles
- **GET** `/users/<id>`: Retrieve a user profile.
- **PUT** `/users/<id>`: Update a user profile.

### Follow/Unfollow
- **POST** `/users/<id>/follow`: Follow a user.
- **POST** `/users/<id>/unfollow`: Unfollow a user.

### Posts
- **GET** `/posts`: Retrieve all posts (paginated).
- **POST** `/posts`: Create a new post.
- **GET** `/posts/<id>`: Retrieve a specific post.
- **PUT** `/posts/<id>`: Update a post.
- **DELETE** `/posts/<id>`: Delete a post.

### Interactions
- **POST** `/posts/<id>/like`: Like a post.
- **POST** `/posts/<id>/comment`: Comment on a post.

---

## Testing
Run tests using pytest:
```bash
pytest
```

---

## Future Enhancements
- Implement real-time updates for feeds and notifications using WebSockets.
- Add support for multimedia posts (images/videos).
- Introduce admin roles for managing content.
- Enhance security features (OAuth, 2FA).

---

## Contribution
Feel free to fork this repository and submit pull requests. For major changes, open an issue first to discuss what you would like to change.

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

## Contact
For any questions or feedback, please reach out at [your-email@example.com].
