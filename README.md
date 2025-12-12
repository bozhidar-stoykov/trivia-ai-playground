# Trivia AI Playground

AI-powered Jeopardy! trivia API with PostgreSQL, FastAPI, and OpenAI integration.

## Features

- 🎯 Random trivia questions with filtering (round, value)
- 🤖 AI-powered answer verification (tolerant to spelling errors)
- 🎮 AI agents that play trivia (10 agents with different specialties and skill levels)
- 📊 216,930+ Jeopardy! questions from CSV dataset
- 🐳 Dockerized deployment

## Quick Start

### Using Docker (Recommended)

```bash
# 1. Clone and navigate to the project
cd trivia-ai-playground

# 2. Set your OpenAI API key
$env:OPENAI_API_KEY="sk-your-key-here"  # Windows PowerShell
# export OPENAI_API_KEY="sk-your-key-here"  # Linux/Mac

# 3. Start all services
docker-compose up

# 4. API is ready at http://localhost:8000
# 5. View docs at http://localhost:8000/docs
```

### Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start PostgreSQL (or use Docker)
docker-compose up postgres

# 3. Set environment variables
$env:OPENAI_API_KEY="sk-your-key-here"
$env:DATABASE_URL="postgresql://postgres:postgres@localhost:5432/trivia_db"

# 4. Run data ingestion
python src/data_ingestion/ingestion_script.py

# 5. Start the API
cd src
uvicorn main:app --reload

# API runs at http://localhost:8000
```

## API Endpoints

### GET /api/v1/question/
Get a random trivia question (without the answer).

**Query Parameters:**
- `round` (optional): Filter by round (e.g., "Jeopardy!", "Double Jeopardy!")
- `value` (optional): Filter by value (e.g., "$200", "$400")

**Example:**
```bash
curl "http://localhost:8000/api/v1/question/?round=Jeopardy!&value=$200"
```

**Response:**
```json
{
  "question_id": 123,
  "round": "Jeopardy!",
  "category": "HISTORY",
  "value": "$200",
  "question": "For the last 8 years of his life, Galileo was under house arrest for espousing this man's theory"
}
```

### GET /api/v1/question/{question_id}
Get detailed question info including the answer.

**Example:**
```bash
curl http://localhost:8000/api/v1/question/123
```

**Response:**
```json
{
  "question_id": 123,
  "round": "Jeopardy!",
  "category": "HISTORY",
  "value": "$200",
  "question": "For the last 8 years of his life, Galileo was under house arrest for espousing this man's theory",
  "answer": "Copernicus",
  "show_number": 4680,
  "air_date": "2004-12-31"
}
```

### POST /api/v1/verify-answer/
Verify a user's answer using AI (tolerant to spelling errors).

**Request Body:**
```json
{
  "question_id": 123,
  "user_answer": "Copernics"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/verify-answer/ \
  -H "Content-Type: application/json" \
  -d '{"question_id": 123, "user_answer": "Copernics"}'
```

**Response:**
```json
{
  "is_correct": true,
  "ai_response": "Yes, that's correct! Despite the spelling error, you meant Copernicus."
}
```

### POST /api/v1/agent-play/
Watch an AI agent select and answer a random question.

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/agent-play/
```

**Response:**
```json
{
  "agent_name": "HistoryBot-Expert",
  "agent_specialty": "history",
  "skill_level": "expert",
  "question_id": 42,
  "category": "ANCIENT ROME",
  "question": "Built in 312 B.C. to link Rome & the South of Italy, it's still in use today",
  "ai_answer": "The Appian Way",
  "correct_answer": "Appian Way",
  "is_correct": true,
  "reasoning": "The Appian Way was one of the earliest Roman roads."
}
```

## AI Agents

10 specialized agents with varying expertise:

| Agent | Specialty | Skill Level |
|-------|-----------|-------------|
| HistoryBot | History | Expert |
| GeographyPro | Geography | Expert |
| ScienceWiz | Science | Expert |
| LiteratureBuff | Literature | Expert |
| SportsGuru | Sports | Expert |
| PopCultureFan | Pop Culture | Intermediate |
| MovieManiac | Movies | Intermediate |
| MusicMaestro | Music | Intermediate |
| GeneralKnowledge | General | Intermediate |
| NoviceNed | General | Novice |

Agents are automatically matched to questions based on category.

## Testing

I didn't have time to write any tests.

## Tech Stack

- **FastAPI** - Web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **OpenAI GPT-4** - Answer verification & AI agents
- **Docker** - Containerization
- **Pydantic** - Data validation

## Environment Variables

Create a `.env` file or export these variables:

```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/trivia_db
OPENAI_API_KEY=sk-your-openai-api-key-here
```

## Project Structure

```
trivia-ai-playground/
├── src/
│   ├── main.py                 # FastAPI application
│   ├── database.py             # Database configuration
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # AI service (OpenAI)
│   ├── trivia_service/         # Business logic & routes
│   └── data_ingestion/         # CSV import scripts
├── docker-compose.yml          # Docker orchestration
├── Dockerfile.api              # API container
├── Dockerfile.ingestion        # Data ingestion container
├── requirements.txt            # Python dependencies
├── test_api.py                 # API tests
├── test_agent_play.py          # Agent play tests
└── demo_agent_play.py          # Quick demo

```

## Interactive Documentation

Visit **http://localhost:8000/docs** for Swagger UI to try all endpoints interactively.

## Notes

- Requires valid OpenAI API key for AI features
- Expert agents: ~95% accuracy in their specialty
- Intermediate agents: ~75% accuracy
- Novice agents: ~50% accuracy
- Questions are randomly selected from 216,930+ Jeopardy! questions