"""
SOP (Standard Operating Procedure) templates for proposal formatting.
Each agent will follow its role-specific SOP to structure the proposal clearly.
"""

SOP_TEMPLATES = {
    "Architect": (
        "System Design Proposal:\n"
        "- Provide a high-level architectural design using UML-like textual representations.\n"
        "- Describe main components/modules, their responsibilities, and how they interact.\n"
        "- Use bullet points or text diagrams to show relationships between modules.\n"
        "- Include technologies/libraries/frameworks if applicable."
    ),

    "Engineer": (
        "Implementation Plan:\n"
        "- Outline the main algorithm or implementation logic in structured pseudocode.\n"
        "- Use indentation, control flow (if/else, loops), and function-like definitions.\n"
        "- Explain data structures, helper functions, and error handling as needed.\n"
        "- Keep it readable and suitable for implementation handoff."
    ),

    "QA Engineer": (
        "Test Plan and Validation Strategy:\n"
        "- List key functional and edge-case scenarios to validate.\n"
        "- Include unit test cases, integration points, and any stress/load tests.\n"
        "- Specify input-output expectations for each case.\n"
        "- Mention frameworks (e.g., pytest) or coverage tools if relevant."
    ),

    "Product Manager": (
        "PRD (Product Requirement Document) Clarification:\n"
        "- Summarize the end-user need and business goal.\n"
        "- Break down the requirements into functional and non-functional goals.\n"
        "- Identify constraints (e.g., response time, UI constraints).\n"
        "- Highlight edge requirements or ambiguities to be discussed.\n"
        "- Output in a numbered list or tabular format for clarity."
    )
}
