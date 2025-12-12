import os
from openai import OpenAI
from typing import Tuple

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def verify_answer_with_ai(
    question: str, correct_answer: str, user_answer: str
) -> Tuple[bool, str]:
    """
    Verify if user's answer matches the correct answer using OpenAI.

    Args:
        question: The trivia question
        correct_answer: The correct answer from the database
        user_answer: The user's submitted answer

    Returns:
        Tuple of (is_correct, ai_explanation)
    """

    prompt = f"""You are a Jeopardy! game judge. Your task is to determine if a user's answer is correct, even if it has spelling errors or is phrased differently.

    Question: {question}
    Correct Answer: {correct_answer}
    User's Answer: {user_answer}

    Analyze if the user's answer is essentially correct despite any spelling errors or different phrasing. Consider:
    1. Spelling mistakes (e.g., "Copernics" vs "Copernicus")
    2. Alternative names or titles
    3. Partial answers that capture the key concept
    4. Contextual understanding

    Respond in this exact format:
    VERDICT: [CORRECT or INCORRECT]
    EXPLANATION: [One sentence explaining why, providing context about the correct answer]

    Be generous with spelling errors but strict about factual accuracy."""

    try:
        response = client.chat.completions.create(
            model="gpt-4.5",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful and fair Jeopardy! game judge.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
        )

        ai_response = response.choices[0].message.content.strip()

        # Parse the response
        lines = ai_response.split("\n")
        verdict_line = ""
        explanation_line = ""

        for line in lines:
            if line.startswith("VERDICT:"):
                verdict_line = line.replace("VERDICT:", "").strip()
            elif line.startswith("EXPLANATION:"):
                explanation_line = line.replace("EXPLANATION:", "").strip()

        # Determine if correct
        is_correct = (
            "CORRECT" in verdict_line.upper()
            and "INCORRECT" not in verdict_line.upper()
        )

        # Use explanation or fallback
        explanation = explanation_line if explanation_line else ai_response

        return is_correct, explanation

    except Exception as e:
        print(f"OpenAI API error: {e}")
        is_correct = (
            user_answer.lower().strip() in correct_answer.lower()
            or correct_answer.lower() in user_answer.lower().strip()
        )
        explanation = f"API error. Simple match: {'Yes' if is_correct else 'No'}, correct answer is {correct_answer}."
        return is_correct, explanation
