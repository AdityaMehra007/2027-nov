# 🛠️ Contributing to CASHFLOW INFINITY: OMNIVERSE

Thank you for your interest in contributing to **CASHFLOW INFINITY: OMNIVERSE**! We welcome contributions from developers, researchers, and systems architects to help advance autonomous intelligence, quantitative engines, and planetary resilience systems.

---

## 🧭 Navigation & Workflow

1. [Code of Conduct](#code-of-conduct)
2. [Development Environment Setup](#development-environment-setup)
3. [Architecture Overview](#architecture-overview)
4. [Test-Driven Development (TDD) Guidelines](#test-driven-development-tdd-guidelines)
5. [Git & Conventional Commit Standards](#git--conventional-commit-standards)
6. [Pull Request Lifecycle](#pull-request-lifecycle)
7. [Security & Capital Governance](#security--capital-governance)

---

## 📜 Code of Conduct

All contributors and maintainers are expected to uphold the standards outlined in our [Code of Conduct](CODE_OF_CONDUCT.md). Please report unacceptable behavior to [ashishiash007@gmail.com](mailto:ashishiash007@gmail.com).

---

## 💻 Development Environment Setup

### Prerequisites
* **Python**: 3.11, 3.12, or 3.13
* **Git**: Version 2.40+
* **Optional Runtimes**: Rust (`cargo` 1.80+), C++23 (`clang++` 18+ or `g++` 14+), CUDA Toolkit 12.4+ (for hardware kernels).

### 1. Clone & Set Up Virtual Environment
```bash
# Clone the repository
git clone https://github.com/AdityaMehra007/cashflow-infinity-omniverse.git
cd cashflow-infinity-omniverse

# Create and activate Python virtual environment
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies in Editable Mode
```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

---

## 🏛️ Architecture Overview

The repository is modularly structured:

* `src/omniverse/`: Core application modules, API routes, database schemas, and CLI commands.
* `packages/apex-core/`: Standalone, pip-installable distribution package containing the Apex Autograd, Order Book, VM, and Merkle tree engines.
* `src/kernel/`: Distributed kernel nodes, Raft/Bullshark BFT consensus adapters, and LSM state engines.
* `src/rtos/`, `src/cuda/`, `src/ebpf/`: Deep-tech hardware acceleration runtimes.
* `tests/`: 100% hermetic Pytest test suites.
* `deploy/`: Multi-cloud Kubernetes manifests, Docker Compose profiles, and CI workflow blueprints.

---

## 🧪 Test-Driven Development (TDD) Guidelines

OMNIVERSE strictly enforces **Hermetic Test-Driven Development**:

1. **Zero Network Dependencies**: Unit and integration tests must run 100% offline without hitting external APIs, live Stripe gateways, or external databases. Use mocks and synthetic fixtures.
2. **Speed Standard**: Individual test files must execute in under 3.0 seconds. The full primary test suite must complete in under 15 seconds.
3. **Execution Command**:
```bash
# Run core test suites
python -m pytest tests/test_apex_core_package.py \
                 tests/test_universal_engines_32.py \
                 tests/test_singularity_civilization_codex.py \
                 tests/test_offline_master_verification.py -v
```

---

## 📝 Git & Conventional Commit Standards

All commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

* `feat(<scope>)`: A new capability, engine, or API endpoint
* `fix(<scope>)`: A bug fix or timing threshold adjustment
* `docs(<scope>)`: Documentation updates, specs, or architectural diagrams
* `chore(<scope>)`: Dependency updates, formatting, or repository housekeeping
* `perf(<scope>)`: Performance optimization or latency reduction
* `test(<scope>)`: Adding or refactoring test suites

### Example Commit:
```bash
git commit -m "feat(quant): implement Black-Scholes volatility surface interpolation"
```

---

## 🔄 Pull Request Lifecycle

1. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Implement Changes & Write Tests**: Ensure full test coverage for every new codepath.
3. **Verify Locally**: Run `python -m pytest tests/` and confirm all tests pass.
4. **Push & Open PR**:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **PR Review**: Fill out the [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md). Maintainers will review and merge upon green status.

---

## 🔒 Security & Capital Governance

Any PR touching `src/omniverse/security.py`, payment settlement gateways, or air-gapped governors requires:
* Zero regression in the cryptographic signature test suite.
* Explicit sign-off verifying that autonomous live money movement remains disabled by default.

For security vulnerabilities, please refer directly to our [Security Policy](SECURITY.md).
