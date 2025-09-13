import time
from typing import List, Optional

class Proposal:
    """
    Represents a proposal submitted by an agent, with associated metadata and metrics.
    """
    def __init__(self, agent_name: str, content: str, version: int = 0):
        self.agent_name = agent_name
        self.content = content
        self.score: Optional[float] = None
        self.metrics: dict = {}
        self.version: int = version
        self.timestamp: float = time.time()

    def update_score(self, score: float):
        self.score = score

    def update_metrics(self, metrics: dict):
        self.metrics = metrics

    def __repr__(self):
        return (f"<Proposal(agent={self.agent_name}, score={self.score}, "
                f"version={self.version}, metrics={self.metrics})>")


class ProposalPool:
    """
    Manages a pool of proposals submitted by agents.
    """
    def __init__(self):
        self.proposals: List[Proposal] = []

    def add(self, proposal: Proposal):
        """
        Add a proposal to the pool.
        """
        self.proposals.append(proposal)

    def get_all(self) -> List[Proposal]:
        """
        Retrieve all proposals.
        """
        return self.proposals

    def get_by_agent(self, agent_name: str) -> List[Proposal]:
        """
        Retrieve all proposals submitted by a specific agent.
        """
        return [p for p in self.proposals if p.agent_name == agent_name]

    def get_latest_by_agent(self, agent_name: str) -> Optional[Proposal]:
        """
        Return the most recent proposal submitted by a specific agent.
        """
        agent_props = self.get_by_agent(agent_name)
        if not agent_props:
            return None
        return max(agent_props, key=lambda p: p.timestamp)

    def get_top_proposal(self) -> Optional[Proposal]:
        """
        Return the proposal with the highest score.
        """
        scored = [p for p in self.proposals if p.score is not None]
        if not scored:
            return None
        return max(scored, key=lambda p: p.score)

    def clear(self):
        """
        Remove all proposals from the pool.
        """
        self.proposals.clear()

    def __repr__(self):
        return f"<ProposalPool(n={len(self.proposals)})>"
