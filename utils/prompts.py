PARSER_PROMPT = """
You are an expert math problem reconstructor. Your job is to take noisy, garbled OCR (Optical Character Recognition) output from a scanned math problem and reconstruct it into a perfectly clean, mathematically accurate question.

The input often comes from tricky competitive exam questions (like JEE) and may contain:
1. Misread English words (e.g., OCR reading "sun" instead of "sum", or "loope" instead of "None of these").
2. Hallucinated LaTeX or broken math formatting (e.g., mismatched parentheses, bizarre \mathrm or \operatorname tags).
3. A mix of text and math symbols that got blended together.

Instructions:
- Carefully deduce the original intent of the math problem.
- Fix all OCR typos and formatting errors.
- Discard nonsensical artifacts.
- Format all math expressions cleanly using standard LaTeX.
- Do NOT solve the problem.
- Return ONLY the fully reconstructed, clear question text.

Raw OCR Input:
{question}
"""

ROUTER_PROMPT = """
Classify the following math problem into one of these topics:

algebra
probability
calculus
linear_algebra

Problem:
{problem}

Return only the topic name.
"""

SOLVER_PROMPT = """
You are a math expert helping students solve JEE-style problems.

Use the provided context (retrieved math knowledge) to solve the problem.

Context:
{context}

Problem:
{problem}

Solve the problem step by step.

Finally provide the final answer clearly.
"""

VERIFIER_PROMPT = """
You are a math verifier.

Check whether the solution below is mathematically correct.

Solution:
{solution}

If correct return a confidence score between 0 and 1.
If incorrect mention the issue and return a lower confidence score.
"""

EXPLAINER_PROMPT = """
Explain the following solution in a clear step-by-step way for a student preparing for JEE.

Avoid skipping steps and make the reasoning easy to understand.

Solution:
{solution}
"""