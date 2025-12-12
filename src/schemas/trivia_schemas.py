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
