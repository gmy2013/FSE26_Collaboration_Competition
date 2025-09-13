from typing import List
from agent import Agent
import os
import re
from openai import OpenAI

def dcc_simulation(task_description, sop_template, roles, max_rounds=5):
    agents = [Agent(f"Agent-{i+1}", role, sop_template[role]) for i, role in enumerate(roles)]
    message_pool = {}

    for agent in agents:
        proposal = agent.generate_initial_proposal(task_description)
        message_pool[agent.name] = proposal
        print(f"{agent.name} ({agent.role}) initial proposal:\n{proposal}\n")

    for round_num in range(max_rounds):
        print(f"\n===== Round {round_num + 1} =====")
        converged = True
        for agent in agents:
            peer_proposals = [p for name, p in message_pool.items() if name != agent.name]
            prev_utility = agent.utility
            refined = agent.refine_proposal(peer_proposals)
            message_pool[agent.name] = refined
            if agent.utility > prev_utility:
                print(f"{agent.name} improved utility: {prev_utility:.4f} -> {agent.utility:.4f}")
                converged = False
            else:
                print(f"{agent.name} no change in utility ({agent.utility:.4f})")

        if converged:
            print("\n[Converged] All agents reached local optima.")
            break

    final_outputs = sorted(agents, key=lambda a: a.utility, reverse=True)
    print("\n===== Final Optimized Outputs =====")
    for agent in final_outputs:
        print(f"\n{agent.name} ({agent.role})\nUtility: {agent.utility:.4f}\nProposal:\n{agent.proposal}\n")


# Role-specific SOP templates
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



def run_stage(agents, task_input, stage_name, max_rounds=5):
    message_pool = {}
    for agent in agents:
        proposal = agent.generate_initial_proposal(task_input)
        message_pool[agent.name] = proposal
        print(f"\n[{stage_name}] {agent.name} initial proposal:\n{proposal}\n")
        print('*****************')

    for round_num in range(max_rounds):
        print(f"--- {stage_name} Round {round_num + 1} ---")
        converged = True
        for agent in agents:
            peers = [p for name, p in message_pool.items() if name != agent.name]
            prev_util = agent.utility
            refined = agent.refine_proposal(peers)
            message_pool[agent.name] = refined
            if agent.utility > prev_util:
                print(f"{agent.name} improved utility: {prev_util:.2f} -> {agent.utility:.2f}")
                converged = False
        if converged:
            print(f"[{stage_name}] Converged.")
            break

    # Select the best agent proposal
    best_agent = max(agents, key=lambda a: a.utility)
    print(f"\n[{stage_name}] Best Proposal by {best_agent.name}:\n{best_agent.proposal}\n")

    # Save proposal to file
    os.makedirs("output", exist_ok=True)
    proposal_file = f"output/{stage_name.replace(' ', '_')}_proposal.txt"
    with open(proposal_file, "w", encoding="utf-8") as f:
        f.write(best_agent.proposal)
    print(f"[{stage_name}] Proposal saved to: {proposal_file}")


    return best_agent.proposal





