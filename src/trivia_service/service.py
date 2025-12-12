import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from services.ai_service import verify_answer_with_ai

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.trivia_question import TriviaQuestion


def parse_value(value_str: str) -> Optional[int]:
    if not value_str:
        return None
    try:
        return int(value_str.replace("$", "").replace(",", "").strip())
    except (ValueError, AttributeError):
        return None


def format_value(value_int: Optional[int]) -> str:
    if value_int is None:
        return ""
    return f"${value_int:,}" if value_int >= 1000 else f"${value_int}"


def get_random_question(
    db: Session, round: Optional[str] = None, value: Optional[str] = None
) -> Optional[TriviaQuestion]:
    """Get a random trivia question with optional filters"""
    query = db.query(TriviaQuestion)

    if round:
        query = query.filter(TriviaQuestion.round == round)

    if value:
        value_int = parse_value(value)
        if value_int:
            query = query.filter(TriviaQuestion.value == value_int)

    return query.order_by(func.random()).first()


def get_question_by_id(db: Session, question_id: int) -> Optional[TriviaQuestion]:
    """Get a specific question by ID"""
    return db.query(TriviaQuestion).filter(TriviaQuestion.id == question_id).first()


def verify_user_answer(
    db: Session, question_id: int, user_answer: str
) -> Optional[dict]:
    """
    Verify user's answer against the correct answer using AI.

    Args:
        db: Database session
        question_id: ID of the question
        user_answer: User's submitted answer

    Returns:
        Dictionary with verification results or None if question not found
    """

    question = get_question_by_id(db, question_id)

    if not question:
        return None

    # Verify using AI
    is_correct, ai_explanation = verify_answer_with_ai(
        question=question.question or "",
        correct_answer=question.answer or "",
        user_answer=user_answer,
    )

    return {
        "is_correct": is_correct,
        "ai_response": ai_explanation,
        "correct_answer": question.answer,
        "question": question.question,
    }
