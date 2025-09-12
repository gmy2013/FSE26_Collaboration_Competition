This repository implements the C3 framework, which integrates centralized auction-based collaboration and decentralized communication-aware competition to overcome the collaboration degeneration problem in multi-agent LLM systems, particularly in complex software development tasks.

In C3 folder:

auction.py contains the  AuctionCoordinator class used to evaluate and score agent proposals based on novelty, executability, and diversity. Also responsible for generating peer feedback.

agent.py defines the base Agent class and specialized roles (e.g., Architect, Engineer). Each agent can generate and refine proposals using OpenAI's Chat API. Includes utility computation based on LLM-assessed quality.

proposal_pool.py provides Proposal and ProposalPool classes to manage agent submissions and evaluation metadata. Used in scoring and refinement cycles.

sop_templates.py contains standardized SOP (Standard Operating Procedure) templates that define role-specific proposal formats and evaluation criteria.

metrics.py implements offline quantitative metrics such as Task Ownership Entropy (TOE), Adaptation Responsiveness Rate (ARR), and Feedback Utilization Score (FUS) for evaluating inter-agent dynamics.

dcc.py implements the Decentralized Communication-aware Competition (DCC) mechanism. Agents iteratively observe and refine proposals until convergence. 

cab.py implements a multi-stage pipeline across Product Manager, Architect, Engineer, and QA Engineer agents. Proposals are generated, refined, and passed between roles in a structured pipeline. 

naive_isolated.py implements naive competition, where all agents generate proposals independently, followed by a centralized auction-style winner selection. No refinement or communication is involved and solated competition, where agents generate proposals in complete isolation without visibility, feedback, or scoring. Serves as a baseline for collaboration-free behavior.

dataset: 70 tasks extended from SoftwareDev since it is not fully open-source.