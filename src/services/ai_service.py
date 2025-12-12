import os
from openai import OpenAI
from typing import Tuple
import random

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


def get_agent_answer(
    question: str,
    category: str,
    correct_answer: str,
    agent_specialty: str,
    skill_level: str,
) -> Tuple[str, str, bool]:
    """
    Get an AI agent's answer to a trivia question.

    Args:
        question: The trivia question
        category: Question category
        correct_answer: The correct answer (for verification)
        agent_specialty: Agent's area of expertise (history, geography, science, etc.)
        skill_level: Agent's skill level (expert, intermediate, novice)

    Returns:
        Tuple of (agent_answer, reasoning, is_correct)
    """

    # Define skill level prompts
    skill_prompts = {
        "expert": "You are a trivia expert with deep knowledge. Answer confidently and accurately.",
        "intermediate": "You are moderately knowledgeable. Sometimes you might make small mistakes or be slightly uncertain.",
        "novice": "You are a beginner at trivia. You often make mistakes, misremember facts, or confuse similar concepts.",
    }

    # Adjust confidence and error rate based on skill
    skill_configs = {
        "expert": {"error_chance": 0.05, "confidence": "very confident"},
        "intermediate": {"error_chance": 0.25, "confidence": "somewhat confident"},
        "novice": {"error_chance": 0.50, "confidence": "uncertain"},
    }

    skill_config = skill_configs.get(skill_level, skill_configs["intermediate"])
    skill_prompt = skill_prompts.get(skill_level, skill_prompts["intermediate"])

    # Check if category matches specialty
    category_match = (
        agent_specialty.upper() in category.upper()
        or category.upper() in agent_specialty.upper()
    )

    # Adjust error chance based on specialty match
    if category_match and skill_level == "expert":
        error_chance = 0.02
    elif category_match:
        error_chance = skill_config["error_chance"] * 0.5
    else:
        error_chance = skill_config["error_chance"] * 1.5

    # Randomly decide if agent will make a mistake
    make_mistake = random.random() < error_chance

    prompt = f"""You are playing Jeopardy! as an AI agent specialized in {agent_specialty}.

    {skill_prompt}

    Category: {category}
    Question: {question}

    {'IMPORTANT: Make a plausible but INCORRECT answer for this question. Make a mistake that a ' + skill_level + ' player might make - confuse similar concepts, get dates wrong, mix up names, etc.' if make_mistake else 'Answer this question correctly and confidently.'}

    Provide your answer in this format:
    ANSWER: [Your answer]
    REASONING: [One sentence explaining your answer]

    Be concise. Answer as if you're a contestant."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a Jeopardy! contestant AI agent. Specialty: {agent_specialty}. Skill: {skill_level}.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.7 if make_mistake else 0.3,
        )

        ai_response = response.choices[0].message.content.strip()

        # Parse the response
        lines = ai_response.split("\n")
        agent_answer = ""
        reasoning = ""

        for line in lines:
            if line.startswith("ANSWER:"):
                agent_answer = line.replace("ANSWER:", "").strip()
            elif line.startswith("REASONING:"):
                reasoning = line.replace("REASONING:", "").strip()

        # Fallback if parsing fails
        if not agent_answer:
            agent_answer = ai_response.split("\n")[0]
        if not reasoning:
            reasoning = "No reasoning provided."

        # Verify if the answer is correct
        is_correct, _ = verify_answer_with_ai(question, correct_answer, agent_answer)

        return agent_answer, reasoning, is_correct

    except Exception as e:
        print(f"OpenAI API error in get_agent_answer: {e}")
        return "Unable to answer", f"API error occurred: {str(e)}", False
