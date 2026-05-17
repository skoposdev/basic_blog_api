# Basic Blog API

A RESTful blog API built with FastAPI, featuring JWT authentication via HTTP-only cookies, and a clean layered architecture.

## Stack

- **Python** 3.14
- **FastAPI** — web framework
- **SQLite** — database
- **PyJWT** — JWT authentication
- **Pydantic** — data validation
- **pwdlib** — password hashing

## Prerequisites

- Python 3.14
- pip

## Installation

```bash
# Clone the repository
git clone https://github.com/skoposdev/basic_blog_api.git
cd basic_blog_api

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Initialize the databases
python database/db.py

# Start the server
uvicorn main:app --reload
```

## Environment Variables

Create a `.env` file at the root of the project with the following variables:

```env
SECRET_KEY=your_secret_key_minimum_32_characters
```

## API Routes

### Auth

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and receive JWT cookie | No |
| POST | `/auth/logout` | Logout and clear JWT cookie | Yes |

### Articles

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/articles` | Retrieve all articles | No |
| GET | `/article/author/{article_author}` | Retrieve articles by author | No |
| GET | `/article/id/{article_id}` | Retrieve an article by ID | No |
| POST | `/article` | Create a new article | Yes |
| PATCH | `/article/{article_id}` | Update an article | Yes |
| DELETE | `/article/{article_id}` | Delete an article | Yes |

## Architecture

```
basic_blog_api/
├── main.py                  # Entry point
├── database/
│   ├── article_db.py        # Article database logic
│   └── user_db.py           # User database logic
├── routes/
│   ├── articles.py          # Article routes
│   └── auth.py              # Auth routes
├── services/                # Business logic
├── dependencies/
│   └── dependencies.py      # FastAPI dependencies (auth guard)
├── utils/
│   ├── models.py            # Pydantic models
│   ├── exceptions.py        # Custom exceptions
│   └── jwt_utils.py         # JWT encode/decode
└── README.md
```

## Authentication

Authentication is handled via **JWT tokens** stored in **HTTP-only cookies**, providing protection against XSS attacks. Protected routes require a valid token cookie issued at login.
