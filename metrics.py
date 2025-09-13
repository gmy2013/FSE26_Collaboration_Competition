import math
from collections import Counter
from typing import List, Dict


def compute_task_ownership_entropy(task_winners: List[str]) -> float:
    """
    Task Ownership Entropy (TOE)
    Measures the fairness of task distribution among agents.
    Higher entropy indicates more balanced contribution across agents.

    :param task_winners: List of agent names who won each task.
    :return: TOE score.
    """
    total_tasks = len(task_winners)
    if total_tasks == 0:
        return 0.0

    counts = Counter(task_winners)
    entropy = 0.0
    for count in counts.values():
        p_i = count / total_tasks
        entropy -= p_i * math.log(p_i, 2)
    return entropy


def compute_adaptation_responsiveness_rate(improvement_flags: List[bool]) -> float:
    """
    Adaptation Responsiveness Rate (ARR)
    Measures how frequently agents improve their proposals after feedback.

    :param improvement_flags: List of booleans indicating if each proposal improved post-feedback.
    :return: ARR score.
    """
    if not improvement_flags:
        return 0.0
    improved = sum(improvement_flags)
    return improved / len(improvement_flags)


def compute_feedback_utilization_score(used_insights: int, total_insights: int) -> float:
    """
    Feedback Utilization Score (FUS)
    Measures how effectively agents incorporate peer feedback into final proposals.

    :param used_insights: Number of peer suggestions explicitly used or implemented.
    :param total_insights: Total number of peer suggestions given.
    :return: FUS score.
    """
    if total_insights == 0:
        return 0.0
    return used_insights / total_insights


