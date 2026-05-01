# AI Study Companion — Backend

A RESTful API backend for an AI-powered study companion application. Built with FastAPI and MongoDB, it enables students to upload learning materials, generate AI-powered summaries and flashcards, chat with an AI assistant, manage custom flashcard decks, and schedule academic assessments.

---

## Tech stack

- **FastAPI** — web framework
- **MongoDB Atlas** — cloud database (via Motor async driver)
- **Google Gemini API** — AI content generation (`gemini-2.5-flash-lite`)
- **Python 3.11**
- **Pydantic v2** — data validation and serialisation
- **JWT** — authentication (via `python-jose`)
- **bcrypt** — password hashing
- **pymupdf** — PDF text extraction
- **python-pptx** — PowerPoint text extraction
- **APScheduler** — background task scheduling
- **Uvicorn** — ASGI server

---

## Project structure

```
app/
├── core/
│   ├── gemini.py           # Gemini client setup and retry logic
│   └── jwt.py              # JWT token creation and verification
├── db/
│   ├── connection.py       # MongoDB connection
│   ├── models.py           # Pydantic data models
│   └── queries/
│       ├── user_queries.py
│       ├── chat_queries.py
│       ├── material_queries.py
│       ├── flashcard_queries.py
│       └── assessment_queries.py
├── routers/
│   ├── users_routes.py
│   ├── ai_routes.py
│   ├── material_routes.py
│   ├── flashcard_routes.py
│   └── assessment_routes.py
├── schemas/
│   ├── user_schemas.py
│   ├── chat_schemas.py
│   └── assessment_schemas.py
├── services/
│   ├── user_services.py
│   ├── ai_services.py
│   ├── material_services.py
│   ├── flashcard_services.py
│   ├── assessment_services.py
│   └── file_services.py
└── main.py
```

---

## Getting started

### Prerequisites

- Python 3.11+
- A [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) cluster
- A [Google AI Studio](https://aistudio.google.com) API key

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd AI_powered_study_companion_backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the project root:

```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net
DB_NAME=study_companion
GOOGLE_API_KEY=your_gemini_api_key
SECRET_KEY=your_jwt_secret_key
```

### Running the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.  
Interactive docs are available at `http://127.0.0.1:8000/docs`.

---

## API endpoints

All protected routes require a `Bearer` token in the `Authorization` header.

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Register a new user | No |
| POST | `/api/v1/auth/login` | Login and receive JWT token | No |

### Materials

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/materials/upload` | Upload a PDF or PPTX file | Yes |
| GET | `/api/v1/materials/{material_id}` | Get a single material | Yes |
| GET | `/api/v1/materials/user/all` | Get all materials for the user | Yes |

### AI

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/ai/chat` | Start a new chat | Yes |
| POST | `/api/v1/ai/chat/{chat_id}` | Continue an existing chat | Yes |
| GET | `/api/v1/ai/chat/{chat_id}` | Get a chat with full history | Yes |
| GET | `/api/v1/ai/chats` | Get all user chats (paginated) | Yes |
| GET | `/api/v1/ai/summary/{chat_id}` | Get AI summary for a material | Yes |
| GET | `/api/v1/ai/flashcards/{chat_id}` | Get AI flashcards for a material | Yes |
| POST | `/api/v1/ai/ask/{chat_id}` | Ask a question about a material | Yes |


### Assessments

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/assessments/` | Create a new assessment | Yes |
| GET | `/api/v1/assessments/` | Get all assessments (paginated) | Yes |
| GET | `/api/v1/assessments/upcoming` | Get upcoming assessments | Yes |
| GET | `/api/v1/assessments/{id}` | Get a single assessment | Yes |
| PATCH | `/api/v1/assessments/{id}` | Update an assessment | Yes |
| PATCH | `/api/v1/assessments/{id}/complete` | Mark as completed | Yes |
| DELETE | `/api/v1/assessments/{id}` | Delete an assessment | Yes |

---

## Key design decisions

**Separation of schemas** — three distinct schemas are used for each entity: an input schema (what the client sends), a database model (what is stored), and a response schema (what is returned). This ensures sensitive fields such as `hashed_password` are never exposed in API responses.

**Background task processing** — when a file is uploaded, the material record and its associated chat are created immediately and returned to the client. Summary and flashcard generation runs as a background task so the upload endpoint responds instantly regardless of Gemini's response time.

**AI result caching** — summaries and flashcards are generated once and stored in MongoDB. Subsequent requests return the cached result without calling the Gemini API again, reducing latency and API usage.

**Gemini retry logic** — all Gemini API calls are wrapped in a retry function that automatically reattempts on 503 service unavailable errors with progressive delays (5s, 10s, 15s), and fails immediately on 429 quota errors.

**Material–chat linkage** — every uploaded material is tied to a dedicated chat via a shared `chat_id`, allowing users to ask questions about the material within the same conversational context.

---

## Database collections

| Collection | Description |
|------------|-------------|
| `users` | User accounts and profile data |
| `chats` | Conversation sessions with embedded messages |
| `materials` | Uploaded files with extracted text, summaries, and flashcards |
| `flashcards` | Custom user-created flashcard decks |
| `assessments` | Scheduled academic assessments |

---

## Dependencies

Install all dependencies with:

```bash
pip install -r requirements.txt
```

Key packages:

```
fastapi
uvicorn
motor
pydantic[email]
python-jose[cryptography]
bcrypt
pymupdf
python-pptx
google-genai
python-dotenv
apscheduler
python-multipart
```
