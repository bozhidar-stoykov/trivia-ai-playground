from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class QuestionResponse(BaseModel):
    """Response model for a single trivia question"""

    question_id: int = Field(..., description="Unique identifier for the question")
    round: str = Field(
        ..., description="Game round (Jeopardy!, Double Jeopardy!, Final Jeopardy!)"
    )
    category: str = Field(..., description="Question category")
    value: str = Field(..., description="Monetary value (e.g., $200)")
    question: str = Field(..., description="The trivia question text")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "question_id": 3,
                "round": "Jeopardy!",
                "category": "HISTORY",
                "value": "$200",
                "question": "For the last 8 years of his life, Galileo was under house arrest for espousing this man's theory",
            }
        }


class QuestionDetailResponse(QuestionResponse):
    """Detailed response including the answer"""

    answer: str = Field(..., description="The correct answer")
    show_number: Optional[int] = Field(None, description="Show number")
    air_date: Optional[date] = Field(None, description="Air date of the episode")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "question_id": 3,
                "round": "Jeopardy!",
                "category": "HISTORY",
                "value": "$200",
                "question": "For the last 8 years of his life, Galileo was under house arrest for espousing this man's theory",
                "answer": "Copernicus",
                "show_number": 4680,
                "air_date": "2004-12-31",
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""

    detail: str = Field(..., description="Error message")

    class Config:
        json_schema_extra = {
            "example": {"detail": "No questions found matching the criteria"}
        }


class VerifyAnswerRequest(BaseModel):
    """Request model for answer verification"""

    question_id: int = Field(..., description="The question ID to verify against")
    user_answer: str = Field(..., description="The user's answer in free text")

    class Config:
        json_schema_extra = {
            "example": {"question_id": 7, "user_answer": "The answer is Copernics"}
        }


class VerifyAnswerResponse(BaseModel):
    """Response model for answer verification"""

    is_correct: bool = Field(..., description="Whether the answer is correct")
    ai_response: str = Field(..., description="AI explanation of the verification")

    class Config:
        json_schema_extra = {
            "example": {
                "is_correct": True,
                "ai_response": "Yes, Copernicus proposed the heliocentric theory.",
            }
        }


class AgentPlayResponse(BaseModel):
    """Response model for AI agent playing trivia"""

    agent_name: str = Field(..., description="Name of the AI agent")
    agent_specialty: str = Field(..., description="Agent's specialty area")
    skill_level: str = Field(
        ..., description="Agent's skill level (expert, intermediate, novice)"
    )
    question_id: int = Field(..., description="The question ID")
    category: str = Field(..., description="Question category")
    question: str = Field(..., description="The trivia question")
    ai_answer: str = Field(..., description="The AI agent's answer")
    correct_answer: str = Field(..., description="The correct answer")
    is_correct: bool = Field(..., description="Whether the AI agent answered correctly")
    reasoning: str = Field(..., description="AI agent's reasoning or explanation")

    class Config:
        json_schema_extra = {
            "example": {
                "agent_name": "HistoryBot-Expert",
                "agent_specialty": "history",
                "skill_level": "expert",
                "question_id": 42,
                "category": "ANCIENT ROME",
                "question": "Built in 312 B.C. to link Rome & the South of Italy, it's still in use today",
                "ai_answer": "The Appian Way",
                "correct_answer": "Appian Way",
                "is_correct": True,
                "reasoning": "The Appian Way (Via Appia) was one of the earliest and most important Roman roads.",
            }
        }
