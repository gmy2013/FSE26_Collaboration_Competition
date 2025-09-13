import openai
from openai import OpenAI
import random

client = OpenAI(
    base_url="XXXXXXX",
    api_key="your api key",
)

EVALUATION_PROMPTS = {
    "Product Manager": [
        ("Novelty", "How unique and innovative is the proposed approach compared to other Product Manager proposals?"),
        ("Feasibility", "How realistic and achievable is the proposed solution given the system constraints (e.g., time, resources, scalability)? Can it be implemented within the specified requirements?"),
        ("Alignment with Vision", "Does the proposal align well with the broader goals and vision of the project? Does it cover all major aspects of the product requirements?")
    ],
    "Architect": [
        ("Novelty", "How innovative is the design? Does it introduce new architectural patterns or solutions compared to other proposals?"),
        ("SOP Compliance", "How well does the design adhere to standard architectural patterns, best practices, and coding standards (e.g., design patterns, modularity)? Is it easy to understand and integrate?"),
        ("Feasibility", "How practical and realistic is the design? Does it fit within the overall system constraints (e.g., performance, scalability, and maintenance)? Are there any potential implementation challenges?")
    ],
    "Engineer": [
        ("Code Novelty", "How innovative and different is the implementation compared to others? Does the code use novel algorithms, libraries, or structures?"),
        ("Performance", "How well does the implementation perform? Are there any significant bottlenecks or inefficiencies?"),
        ("Code Diversity", "How diverse are the solutions proposed by different engineers? Does the code explore a range of potential approaches (e.g., different data structures, algorithms)?")
    ],
    "QA Engineer": [
        ("Test Coverage", "How comprehensive is the test coverage? Does it cover all key features, edge cases, and potential failure scenarios?"),
        ("Bug Detection Rate", "How effective are the QA agents at identifying bugs or issues? Do they identify critical problems that were missed in earlier stages?"),
        ("Robustness", "How resilient is the solution under various conditions? Does it handle unexpected inputs and edge cases gracefully?")
    ]
}


class Agent:
    def __init__(self, name, role, sop_template):
        self.name = name
        self.role = role
        self.sop_template = sop_template
        self.current_proposal = ""

    def generate_proposal(self, task_description):
        """
        CAB round 1 proposal generation.
        """
        system_message = f"You are a {self.role} agent named {self.name}. Follow SOP to generate a proposal."
        user_message = (
            f"Task: {task_description}\n"
            f"SOP Guidelines: {self.sop_template}\n"
            f"Please provide a structured and thoughtful proposal for your role."
        )
        try:
            response = client.chat.completions.create(
                model="gpt-4o-2024-05-13",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
            )
            self.current_proposal = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[Error] Proposal generation failed for {self.name}: {e}")
            self.current_proposal = f"[Fallback] Initial proposal by {self.name}"
        return self.current_proposal

    def refine_proposal(self, feedback):
        """
        CAB refinement after feedback from coordinator.
        """
        system_message = f"You are a {self.role} agent named {self.name}. Refine your proposal based on feedback."
        user_message = (
            f"Previous Proposal:\n{self.current_proposal}\n\n"
            f"Feedback:\n{feedback}\n\n"
            "Revise your proposal accordingly."
        )
        try:
            response = client.chat.completions.create(
                model="gpt-4o-2024-05-13",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
            )
            self.current_proposal = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[Error] Refinement failed for {self.name}: {e}")
            self.current_proposal = f"[Fallback] Refined draft by {self.name}"
        return self.current_proposal

    def evaluate_peers(self, peer_proposals):
        """
        DCC peer evaluation: score others using role-based criteria.
        Returns: {peer_name: {criterion: comment}}
        """
        evaluations = {}
        prompts = EVALUATION_PROMPTS.get(self.role, [])
        for peer_name, proposal in peer_proposals.items():
            if peer_name == self.name:
                continue
            evaluations[peer_name] = {}
            for criterion, question in prompts:
                message = (
                    f"Evaluate the following proposal:\n{proposal}\n\n"
                    f"Criterion: {criterion}\nQuestion: {question}\n"
                    "Please provide a concise and critical evaluation."
                )
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-2024-05-13",
                        messages=[
                            {"role": "system", "content": f"You are a {self.role} evaluating peer proposals."},
                            {"role": "user", "content": message}
                        ],
                    )
                    evaluations[peer_name][criterion] = response.choices[0].message.content.strip()
                except Exception as e:
                    evaluations[peer_name][criterion] = f"[Evaluation failed: {e}]"
        return evaluations

    def evolve_from_peers(self, peer_proposals, peer_scores):
        """
        DCC-style evolution: analyze peer proposals and revise current_proposal accordingly.
        """
        # Select two inspirations based on score (or random fallback)
        inspirations = sorted(peer_scores.items(), key=lambda x: -x[1])[:2]
        inspiration_summary = "\n".join(
            [f"{name}: {peer_proposals[name][:500]}" for name, _ in inspirations]
        )
        system_message = "You are a competitive LLM agent improving your solution by observing stronger peers."
        user_message = (
            f"Your Previous Proposal:\n{self.current_proposal}\n\n"
            f"Top Peer Proposals:\n{inspiration_summary}\n\n"
            "Identify two useful strategies or techniques, incorporate them into your solution, and justify the changes."
        )
        try:
            response = client.chat.completions.create(
                model="gpt-4o-2024-05-13",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
            )
            self.current_proposal = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[Error] Evolution failed for {self.name}: {e}")
            self.current_proposal = f"[Fallback] Evolved version by {self.name}"
        return self.current_proposal


# Specialized roles

class ProductManagerAgent(Agent):
    def __init__(self, name, sop_template):
        super().__init__(name, "Product Manager", sop_template)


class ArchitectAgent(Agent):
    def __init__(self, name, sop_template):
        super().__init__(name, "Architect", sop_template)


class EngineerAgent(Agent):
    def __init__(self, name, sop_template):
        super().__init__(name, "Engineer", sop_template)


class QAEngineerAgent(Agent):
    def __init__(self, name, sop_template):
        super().__init__(name, "QA Engineer", sop_template)
