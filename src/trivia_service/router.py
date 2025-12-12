"""Simplified FastAPI router for trivia endpoints"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from schemas.trivia_schemas import (
    QuestionResponse,
    QuestionDetailResponse,
    VerifyAnswerRequest,
    VerifyAnswerResponse,
)
from trivia_service.service import (
    get_random_question,
    get_question_by_id,
    verify_user_answer,
    format_value,
)

router = APIRouter(prefix="/api/v1", tags=["trivia"])


@router.get("/question/", response_model=QuestionResponse)
async def get_question(
    round: Optional[str] = Query(None, example="Jeopardy!"),
    value: Optional[str] = Query(None, example="$200"),
    db: Session = Depends(get_db),
):
    """
    Get a random trivia question.

    - **round**: Filter by game round (e.g., "Jeopardy!")
    - **value**: Filter by monetary value (e.g., "$200")
    """
    question = get_random_question(db, round=round, value=value)

    if not question:
        raise HTTPException(status_code=404, detail="No questions found")

    return QuestionResponse(
        question_id=question.id,
        round=question.round or "",
        category=question.category or "",
        value=format_value(question.value),
        question=question.question or "",
    )


@router.get("/question/{question_id}", response_model=QuestionDetailResponse)
async def get_question_detail(question_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific question including the answer"""
    question = get_question_by_id(db, question_id)

    if not question:
        raise HTTPException(status_code=404, detail=f"Question {question_id} not found")

    return QuestionDetailResponse(
        question_id=question.id,
        round=question.round or "",
        category=question.category or "",
        value=format_value(question.value),
        question=question.question or "",
        answer=question.answer or "",
        show_number=question.show_number,
        air_date=question.air_date,
    )


@router.post("/verify-answer/", response_model=VerifyAnswerResponse)
async def verify_answer(request: VerifyAnswerRequest, db: Session = Depends(get_db)):
    """
    Verify a user's answer using AI.

    This endpoint uses OpenAI to intelligently verify if the user's answer is correct,
    accounting for spelling errors, alternative phrasings, and contextual understanding.

    - **question_id**: The ID of the question to verify
    - **user_answer**: The user's answer in free text (spelling errors are OK)

    Example: Even if the user writes "Copernics" instead of "Copernicus",
    the AI will recognize it as correct.
    """
    result = verify_user_answer(
        db=db, question_id=request.question_id, user_answer=request.user_answer
    )

    if not result:
        raise HTTPException(
            status_code=404, detail=f"Question {request.question_id} not found"
        )

    return VerifyAnswerResponse(
        is_correct=result["is_correct"], ai_response=result["ai_response"]
    )
