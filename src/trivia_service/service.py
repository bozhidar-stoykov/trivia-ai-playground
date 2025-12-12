import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
import random
from services.ai_service import verify_answer_with_ai, get_agent_answer

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


# Define available AI agents with their specialties and skill levels
AVAILABLE_AGENTS = [
    {"name": "HistoryBot", "specialty": "history", "skill_level": "expert"},
    {"name": "GeographyPro", "specialty": "geography", "skill_level": "expert"},
    {"name": "ScienceWiz", "specialty": "science", "skill_level": "expert"},
    {"name": "LiteratureBuff", "specialty": "literature", "skill_level": "expert"},
    {"name": "SportsGuru", "specialty": "sports", "skill_level": "expert"},
    {
        "name": "PopCultureFan",
        "specialty": "pop culture",
        "skill_level": "intermediate",
    },
    {"name": "MovieManiac", "specialty": "movies", "skill_level": "intermediate"},
    {"name": "MusicMaestro", "specialty": "music", "skill_level": "intermediate"},
    {
        "name": "GeneralKnowledge",
        "specialty": "general knowledge",
        "skill_level": "intermediate",
    },
    {"name": "NoviceNed", "specialty": "general knowledge", "skill_level": "novice"},
]


def get_agent_by_category(category: str) -> dict:
    """Select the most appropriate agent based on question category"""
    category_lower = category.lower()

    # Try to match specialty to category
    for agent in AVAILABLE_AGENTS:
        if agent["specialty"] in category_lower or category_lower in agent["specialty"]:
            return agent

    # Check for keyword matches
    if any(
        word in category_lower for word in ["history", "ancient", "war", "president"]
    ):
        return next(a for a in AVAILABLE_AGENTS if a["name"] == "HistoryBot")
    elif any(
        word in category_lower
        for word in ["geography", "country", "capital", "city", "state"]
    ):
        return next(a for a in AVAILABLE_AGENTS if a["name"] == "GeographyPro")
    elif any(
        word in category_lower
        for word in ["science", "physics", "chemistry", "biology"]
    ):
        return next(a for a in AVAILABLE_AGENTS if a["name"] == "ScienceWiz")
    elif any(
        word in category_lower for word in ["literature", "book", "author", "novel"]
    ):
        return next(a for a in AVAILABLE_AGENTS if a["name"] == "LiteratureBuff")
    elif any(
        word in category_lower for word in ["sports", "olympic", "baseball", "football"]
    ):
        return next(a for a in AVAILABLE_AGENTS if a["name"] == "SportsGuru")
    elif any(
        word in category_lower for word in ["movie", "film", "actor", "hollywood"]
    ):
        return next(a for a in AVAILABLE_AGENTS if a["name"] == "MovieManiac")
    elif any(word in category_lower for word in ["music", "song", "band", "singer"]):
        return next(a for a in AVAILABLE_AGENTS if a["name"] == "MusicMaestro")

    # Default to general knowledge agents
    return random.choice(
        [a for a in AVAILABLE_AGENTS if "General" in a["name"] or "Novice" in a["name"]]
    )


def agent_play_trivia(db: Session) -> Optional[dict]:
    """
    Have an AI agent select and answer a random trivia question.

    Args:
        db: Database session

    Returns:
        Dictionary with agent play results or None if no questions available
    """

    # Get a random question
    question = get_random_question(db)

    if not question:
        return None

    # Select appropriate agent based on category
    agent = get_agent_by_category(question.category or "")

    # Get agent's answer
    agent_answer, reasoning, is_correct = get_agent_answer(
        question=question.question or "",
        category=question.category or "",
        correct_answer=question.answer or "",
        agent_specialty=agent["specialty"],
        skill_level=agent["skill_level"],
    )

    return {
        "agent_name": f"{agent['name']}-{agent['skill_level'].capitalize()}",
        "agent_specialty": agent["specialty"],
        "skill_level": agent["skill_level"],
        "question_id": question.id,
        "category": question.category or "",
        "question": question.question or "",
        "ai_answer": agent_answer,
        "correct_answer": question.answer or "",
        "is_correct": is_correct,
        "reasoning": reasoning,
    }
