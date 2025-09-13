import os
from openai import OpenAI
from agents.agent import Agent
from sop_templates import SOP_TEMPLATES
from auction import AuctionCoordinator
from proposal_pool import Proposal, ProposalPool
from utils import log_and_print

client = OpenAI(
    base_url="https://api.yesapikey.com/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)


def naive_competition(task_description, role, num_agents=4):
    """
    Run naive competition among agents of the same role.
    Each agent independently generates a single-shot proposal without observing or adapting.
    """
    print(f"\n==== Naive Competition: {role} Agents ====")

    # Create agents
    agents = [Agent(f"{role}-{i + 1}", role, SOP_TEMPLATES[role]) for i in range(num_agents)]

    # Evaluation setup
    weights = {"novelty": 0.4, "executability": 0.4, "diversity": 0.2}
    auction = AuctionCoordinator(weights)

    pool = ProposalPool()
    for agent in agents:
        proposal_text = agent.generate_initial_proposal(task_description)
        proposal = Proposal(agent.name, proposal_text)
        pool.add(proposal)
        print(f"\n{agent.name}'s proposal:\n{proposal_text}")

    # Score all proposals
    auction.score_proposals(pool.get_all(), task_description)

    for prop in pool.get_all():
        metrics = prop.metrics
        print(f"{prop.agent_name} scores -> Executability: {metrics['executability']:.2f}, "
              f"Novelty: {metrics['novelty']:.2f}, Diversity: {metrics['diversity']:.2f}, "
              f"Total: {prop.score:.2f}")

    # Select best proposal
    winner = auction.select_winner(pool.get_all())
    print(f"\nWinner: {winner.agent_name} (Score: {winner.score:.2f})\n")
    print(f"Winning Proposal:\n{winner.content}\n")
    return winner.content

def isolated_competition(task_description, role, num_agents=4):
    """
    Simulates isolated competition: Each agent independently completes the task
    with no access to others' ideas, no ranking, and no refinement.
    Useful as a baseline for non-collaborative performance.
    """
    print(f"\n==== Isolated Competition: Role = {role} ====\n")
    agents = [Agent(f"{role}-{i+1}", role, SOP_TEMPLATES[role]) for i in range(num_agents)]

    proposals = []

    for agent in agents:
        proposal_text = agent.generate_initial_proposal(task_description)
        proposals.append(Proposal(agent.name, proposal_text))
        print(f"{agent.name}'s isolated proposal:\n{proposal_text}\n")

    return proposals