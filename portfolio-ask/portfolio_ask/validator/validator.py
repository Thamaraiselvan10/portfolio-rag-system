import re

def extract_numbers(text):
    """
    Extract all numbers from text
    """
    return re.findall(r'\d+', text)


def validate_answer(answer, context_chunks):
    """
    Validate if numbers in answer exist in context
    """

    # Extract numbers from answer
    answer_numbers = extract_numbers(answer)

    # Combine all context text
    context_text = " ".join([chunk["text"] for chunk in context_chunks])

    # Extract numbers from context
    context_numbers = extract_numbers(context_text)

    missing_numbers = []

    for num in answer_numbers:
        if num not in context_numbers:
            missing_numbers.append(num)

    # Decision
    if len(missing_numbers) == 0:
        return {
            "status": "VERIFIED",
            "reason": "All numbers found in context"
        }
    else:
        return {
            "status": "UNVERIFIED",
            "reason": f"Numbers {missing_numbers} not found in context"
        }