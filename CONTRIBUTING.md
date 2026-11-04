# Contributing to CASHFLOW INFINITY: OMNIVERSE

Thank you for your interest in contributing to the world's most ambitious autonomous intelligence and resilience operating system.

## 🌟 Code of Conduct
We are committed to providing an open, welcoming, and harassment-free environment for all contributors. Please review our [Code of Conduct](CODE_OF_CONDUCT.md).

## 🛠️ Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/omniverse.git
   cd omniverse
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies in editable mode:**
   ```bash
   pip install -e .
   pip install pytest pytest-cov ruff
   ```

4. **Verify tests pass:**
   ```bash
   pytest -v
   ```

## 📐 Engineering Principles & Architectural Guidelines

1. **Evidence Before Assertions**: Every bug fix or feature must include automated test coverage with `pytest`.
2. **Security & Human Gating**: Never bypass the `SecurityGovernor`. Live money movement and external communications must remain behind explicit human-in-the-loop approvals.
3. **Clean Decoupling**: Keep domain boundaries intact (`core`, `agents`, `modules/revenue`, `modules/intelligence`, `modules/aether`, `modules/commerce`).
4. **Fast & Deterministic**: Tests should run quickly without external network dependencies by using appropriate fixtures and mocks.
