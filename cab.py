import os
from datetime import datetime
from openai import OpenAI
from agent import (
    ArchitectAgent,
    EngineerAgent,
    QAEngineerAgent,
    ProductManagerAgent,
)
from sop_templates import SOP_TEMPLATES
from proposal_pool import Proposal, ProposalPool
from auction import AuctionCoordinator

# === Setup ===
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_path = f"logs/cab_log_{timestamp}.txt"
os.makedirs("logs", exist_ok=True)

client = OpenAI(
    base_url="XXXXXX",  # replace with your actual endpoint
    api_key="your api key",
)

def log_and_print(message, f):
    print(message)
    f.write(message + "\n")

def run_cab_stage(agents, task_input, role_name, auction_coordinator, f, max_iter=5):
    """
    Run a full CAB stage for one role group (e.g., Engineers), including proposal refinement and feedback loop.
    Returns the final winning proposal content to pass to next role.
    """
    proposal_dict = {}     # agent_name -> latest proposal string
    last_losers = []       # agent names that lost previous round
    last_feedback = {}     # agent_name -> feedback string

    for iteration in range(1, max_iter + 1):
        log_and_print(f"\n=== {role_name} Stage - Iteration {iteration} ===", f)

        pool = ProposalPool()

        for agent in agents:
            if agent.name in last_losers:
                previous = proposal_dict.get(agent.name, "")
                feedback = last_feedback.get(agent.name, "")
                proposal_text = agent.refine_proposal(feedback, previous)
            else:
                proposal_text = agent.generate_proposal(task_input)

            proposal_dict[agent.name] = proposal_text
            pool.add(Proposal(agent.name, proposal_text))

            log_and_print(f"[{agent.name}] Proposal:\n{proposal_text}\n", f)

        # === Scoring ===
        auction_coordinator.score_proposals(pool.get_all(), task_input)

        for p in pool.get_all():
            m = p.metrics
            log_and_print(f"{p.agent_name} scores -> Novelty: {m.get('novelty')}, Executability: {m.get('executability')}, Diversity: {m.get('diversity')}, Total: {p.score:.2f}", f)

        # === Winner Selection ===
        winner = auction_coordinator.select_winner(pool.get_all())
        if winner:
            log_and_print(f"\n🏆 Winner: {winner.agent_name} (Score: {winner.score:.2f})", f)
            log_and_print(f"Winning Proposal Content:\n{winner.content}\n", f)
        else:
            log_and_print("⚠️ No valid winner selected.", f)
            break

        # === Generate Feedback ===
        new_losers = []
        new_feedback = {}
        for p in pool.get_all():
            if p.agent_name != winner.agent_name:
                feedback = auction_coordinator.generate_feedback(p, winner, task_input)
                new_feedback[p.agent_name] = feedback
                new_losers.append(p.agent_name)
                log_and_print(f"📝 Feedback for {p.agent_name}: {feedback}", f)
            else:
                new_feedback[p.agent_name] = ""  # Winner gets no feedback

        last_losers = new_losers
        last_feedback = new_feedback

    return winner.content if winner else task_input
