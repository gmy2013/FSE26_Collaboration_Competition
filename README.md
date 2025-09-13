# C3: Centralized Auction + Decentralized Competition Framework for Multi-Agent LLM Collaboration

This repository implements the **C3 framework**, designed to overcome *collaboration degeneration* in multi-agent LLM systems, especially in complex software development tasks.

C3 synergistically integrates:
- **Centralized Auction-based Collaboration** (CAB)
- **Decentralized Communication-aware Competition** (DCC)

Together, they enable both *structured coordination* and *adaptive refinement* in multi-agent environments.

---

## 🔧 Key Features

- **Agent Roles**: Architect, Engineer, QA, etc., each powered by OpenAI Chat API.
- **Auction Coordinator**: Scores proposals for novelty, feasibility, and diversity.
- **Proposal Pool**: Manages multi-round proposal tracking and metadata.
- **SOP Templates**: Role-specific formats and evaluation criteria.
- **Offline Metrics**: Quantify agent dynamics with TOE, ARR, FUS.
- **Baselines**: Naive competition and fully isolated agents for ablation studies.

---

## 📁 Folder Overview

### `C3/`

| File | Description |
|------|-------------|
| `agent.py` | Defines base `Agent` class and specialized roles. Agents generate and refine proposals with LLMs, compute utilities based on assessed quality. |
| `auction.py` | Implements `AuctionCoordinator` for evaluating proposals (novelty, executability, diversity) and generating peer feedback. |
| `proposal_pool.py` | Contains `Proposal` and `ProposalPool` classes for tracking agent submissions, history, and scoring metadata. |
| `dcc.py` | Implements **Decentralized Communication-aware Competition (DCC)** — agents iteratively observe and refine proposals until convergence. |
| `cab.py` | Implements **Centralized Auction-based Collaboration (CAB)** — proposals pass through structured roles (Product Manager → Architect → Engineer → QA). |
| `naive_isolated.py` | Implements naive competition and isolated agents baseline. No communication or refinement is involved. Useful for studying collaboration absence. |
| `sop_templates.py` | Defines **Standard Operating Procedure (SOP)** templates, guiding role-specific proposal formats and scoring rubrics. |
| `metrics.py` | Offline evaluation metrics for inter-agent dynamics: <br> - `Task Ownership Entropy (TOE)` <br> - `Adaptation Responsiveness Rate (ARR)` <br> - `Feedback Utilization Score (FUS)` |

---

## 🧪 Dataset

- **70 extended tasks** from [SoftwareDev benchmark](https://github.com/OpenAGI/SoftwareDev), adapted for internal use due to partial open-source limitations.

Tasks include:
- API design and implementation
- Refactoring and debugging
- Test generation
- System architecture tasks

---

## 🧠 Motivation

Large Language Models show promise in software engineering but face **collaboration degeneration** when scaled across roles. C3 addresses this by:
- Coordinating via **auctions** that reward diverse and feasible ideas.
- Encouraging communication-aware **competition** and refinement cycles.

This allows agents to balance **alignment** and **autonomy** during development workflows.

---

## 📊 Evaluation Metrics

| Metric | Description |
|--------|-------------|
| **TOE** | Measures distribution of contributions across agents. |
| **ARR** | Tracks how quickly agents adapt to peer feedback. |
| **FUS** | Quantifies how much feedback is effectively utilized in refinements. |

---

