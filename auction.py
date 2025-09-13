import ast
import difflib
import json
from itertools import combinations
import numpy as np
import openai
from openai import OpenAI

# ============ OPENAI SETUP ============
client = OpenAI(
    base_url="XXXXXX",
    api_key="your api key",
)

# ============ STATIC SCORING TOOLS ============

def compute_ast_similarity(code1: str, code2: str) -> float:
    try:
        tree1 = ast.dump(ast.parse(code1))
        tree2 = ast.dump(ast.parse(code2))
        seq = difflib.SequenceMatcher(None, tree1, tree2)
        return seq.ratio()
    except Exception:
        return 0.0

def compute_novelty(generated_code: str, reference_code: str) -> float:
    return 1.0 - compute_ast_similarity(generated_code, reference_code)

def compute_diversity(code_samples: list) -> float:
    if len(code_samples) < 2:
        return 0.0
    distances = [1.0 - compute_ast_similarity(a, b) for a, b in combinations(code_samples, 2)]
    return float(np.mean(distances))

def compute_executability(code: str) -> float:
    try:
        exec_globals = {}
        exec(code, exec_globals)
        return 1.0
    except Exception:
        return 0.0

# ============ AUCTION COORDINATOR ============

class AuctionCoordinator:
    """
    Central evaluator and feedback generator in CAB or peer evaluation in DCC.
    """
    def __init__(self, weights):
        """
        weights: dict mapping metric name -> weight for final score.
        """
        self.weights = weights

    def _safe_call_gpt_metrics(self, proposal, task_description):
        system_message = "You are an expert software reviewer evaluating proposals based on standard metrics."
        user_message = (
            f"Task: {task_description}\n"
            f"Proposal:\n{proposal}\n\n"
            "Evaluate this proposal on a scale from 1 to 10 for the following:\n"
            "- novelty: originality or creativity\n"
            "- executability: likelihood code runs without error\n"
            "- diversity: variance from common/peer solutions\n\n"
            "Respond ONLY with JSON like:\n"
            "{\"novelty\": 8, \"executability\": 7, \"diversity\": 6}"
        )
        try:
            response = client.chat.completions.create(
                model="gpt-4o-2024-05-13",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
            )
            return json.loads(response.choices[0].message.content.strip())
        except Exception as e:
            print(f"[Fallback] GPT evaluation failed: {e}")
            return {k: 5 for k in self.weights}  # Neutral fallback

    def evaluate_proposal(self, proposal_content, task_description, fallback_metrics=None):
        """
        Evaluate one proposal and return full metric dict.
        Optionally fallback to static scoring if GPT fails.
        """
        metrics = self._safe_call_gpt_metrics(proposal_content, task_description)
        if not metrics and fallback_metrics:
            return fallback_metrics
        return metrics

    def score_proposals(self, proposals, task_description):
        """
        Annotate proposal.score and proposal.metrics using weighted metric aggregation.
        """
        for proposal in proposals:
            metrics = self.evaluate_proposal(proposal.content, task_description)
            proposal.metrics = metrics
            proposal.score = sum(self.weights.get(k, 0) * metrics.get(k, 0) for k in self.weights)

    def evaluate_multiple(self, proposal_dict: dict, task_description: str):
        """
        For DCC peer-eval. Input: dict {agent_name: proposal_text}
        Returns: dict {agent_name: metrics dict}
        """
        result = {}
        for name, content in proposal_dict.items():
            metrics = self.evaluate_proposal(content, task_description)
            result[name] = metrics
        return result

    def select_winner(self, proposals):
        """
        Return proposal with highest .score.
        """
        return max(proposals, key=lambda p: p.score if p.score is not None else -1)

    def generate_feedback(self, losing_proposal, winning_proposal, task_description):
        """
        Structured GPT feedback from losing to winning proposal.
        """
        system_message = "You are a reviewer providing feedback to improve a weaker proposal."
        user_message = (
            f"Task: {task_description}\n\n"
            f"Winning Proposal:\n{winning_proposal.content}\n\n"
            f"Losing Proposal:\n{losing_proposal.content}\n\n"
            "Give constructive, actionable feedback to the losing proposal to help it improve. "
            "Highlight how it differs from the winner and what can be better."
        )
        try:
            response = client.chat.completions.create(
                model="gpt-4o-2024-05-13",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[Fallback] Feedback generation failed: {e}")
            return "Improve clarity, feasibility, and innovation in your proposal based on peer comparison."
