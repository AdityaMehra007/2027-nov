import subprocess
import sys
from pathlib import Path
import pytest

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"

@pytest.mark.parametrize("example_file", [
    "01_autonomous_agency_growth_kit.py",
    "02_monte_carlo_var_portfolio.py",
    "03_aether_crisis_logistics_simulation.py",
    "04_planetary_mesh_federated_consensus.py",
    "05_multi_currency_rtgs_clearing.py",
    "06_autonomous_academic_paper_generation.py",
    "07_mcp_agent_orchestration.py"
])
def test_example_script_runs_successfully(example_file):
    script_path = EXAMPLES_DIR / example_file
    assert script_path.exists(), f"Example script {example_file} does not exist"

    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    assert result.returncode == 0, f"Script {example_file} failed with stderr: {result.stderr}\nstdout: {result.stdout}"
    assert "================================================================" in result.stdout
