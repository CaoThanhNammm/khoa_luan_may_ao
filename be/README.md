# Chatbot FastAPI Backend

This is the FastAPI backend for the chatbot application, migrated from Spring Boot.

## Setup and Installation

### Prerequisites

- Python 3.8+
- MySQL Server
- Virtual environment (recommended)

### Installation Steps

1. Clone the repository
2. Navigate to the backend directory:
   ```
   cd chat-backend/be
   ```
3. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Configure environment variables:
   - Copy `.env.example` to `.env` (if not already done)
   - Update the values in `.env` with your configuration

### Database Setup

The application will automatically create the database and tables when it starts. Make sure your MySQL server is running and the credentials in the `.env` file are correct.

## Running the Application

Start the FastAPI server:
```
python main.py
```

The API will be available at http://localhost:8000

API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login and get access token
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password with token

### Chat
- `GET /api/chat/conversations` - Get all conversations
- `GET /api/chat/conversations/{id}` - Get a specific conversation
- `POST /api/chat/conversations` - Start a new conversation
- `POST /api/chat/conversations/with-document` - Start a conversation with document
- `POST /api/chat/conversations/empty-with-document` - Create empty conversation with document
- `POST /api/chat/conversations/{id}/messages` - Send a message
- `DELETE /api/chat/conversations/{id}` - Delete a conversation

### Documents
- `POST /api/upload-file` - Upload a file (PDF)
- `GET /api/documents` - Get all documents

### Users
- `GET /api/users/me` - Get current user info
- `GET /api/users/stats` - Get user statistics

### Contact
- `POST /api/contact` - Send a contact message

## Architecture

The application follows the MVC (Model-View-Controller) pattern:

- **Models**: Database models using SQLAlchemy ORM
- **Views**: Pydantic schemas for request/response validation
- **Controllers**: FastAPI routers handling HTTP requests
- **Services**: Business logic layer

## External Services Integration

The backend integrates with:

1. Local LLM API (http://localhost:8000) for chat functionality
2. AWS S3 for document storage
3. Email service for password reset