#!/usr/bin/env python3
"""
Comprehensive Automated Test Suite for:
  - Multi-Agent Swarm Runtime (src/agents/swarm_runtime.py)
  - Cryptographic SHA3-512 DAG Immutability & Tampering Detection
  - Role-Based Access Control (RBAC) Clearance Enforcement
  - 4 Mathematical Skills: Spectral 2D MHD, Ising Optimizer, J2 Ephemeris, Lyapunov Verifier
  - Pantheon Agents YAML Prompt Schema & Contracts (prompts/pantheon_system_prompts.yaml)
  - 3D Navier-Stokes MHD PINN with Divergence-Free Potentials & Offline Fallback (src/pinn/navier_stokes_mhd_pinn.py)
"""

import asyncio
from pathlib import Path

import numpy as np
import pytest
import yaml

from src.agents.swarm_runtime import (
    SKILL_REGISTRY,
    PlanetaryDAGLedger,
    SpectralMHDSolver2D,
    run_planetary_swarm_cycle,
    skill_optimize_ising_grid,
    skill_orbital_ephemeris,
    skill_solve_mhd,
    skill_verify_lyapunov,
)
from src.pinn.navier_stokes_mhd_pinn import (
    DivergenceFreeMHDPINN,
)

# ============================================================================
# 1. CRYPTOGRAPHIC SHA3-512 DAG IMMUTABILITY & TAMPERING DETECTION
# ============================================================================

def test_sha3_512_dag_immutability():
    """Verify DAG genesis root, 128-char hex SHA3-512 hashes, and parent linkage."""
    ledger = PlanetaryDAGLedger()
    assert ledger.frontier_hashes == ["0" * 128], "Genesis root must be 128 zeros"

    v1 = ledger.append_vertex(sender="HELIOS-MHD", round_num=1, payload={"plasma_temp": 15.2})
    assert len(v1.vertex_hash) == 128, f"SHA3-512 hash must be 128 hex chars, got {len(v1.vertex_hash)}"
    assert all(c in "0123456789abcdef" for c in v1.vertex_hash), "Hash must be valid hex"
    assert v1.parent_hashes == ["0" * 128]
    assert v1.verify_hash() is True

    v2 = ledger.append_vertex(sender="Q-SHOR-SHIELD", round_num=1, payload={"qubit_syndrome": "OK"})
    assert len(v2.vertex_hash) == 128
    assert v2.parent_hashes == [v1.vertex_hash]
    assert v2.verify_hash() is True

    assert ledger.verify_integrity() is True


def test_dag_vertex_tampering():
    """Verify that tampering with any vertex field invalidates SHA3-512 hash and ledger integrity."""
    ledger = PlanetaryDAGLedger()
    v1 = ledger.append_vertex(sender="HELIOS-MHD", round_num=1, payload={"coil_ka": 12.0})
    assert v1.verify_hash() is True

    # Mutate payload
    v1.payload["coil_ka"] = 9999.0
    assert v1.verify_hash() is False, "Mutated payload must fail verification"
    assert ledger.verify_integrity() is False, "Ledger integrity must fail on tampered vertex"

    # Revert payload and mutate timestamp
    v1.payload["coil_ka"] = 12.0
    v1.timestamp_ns += 1
    assert v1.verify_hash() is False, "Mutated timestamp must fail verification"

    # Mutate sender
    v1.timestamp_ns -= 1
    v1.sender_agent = "MALICIOUS-IMPOSTOR"
    assert v1.verify_hash() is False, "Mutated sender must fail verification"


# ============================================================================
# 2. ROLE-BASED ACCESS CONTROL (RBAC) SECURITY ENFORCEMENT
# ============================================================================

def test_rbac_clearance_enforcement():
    """Verify that agents with insufficient clearance cannot invoke protected skills."""
    registry = SKILL_REGISTRY

    # GAIA-NAVIER has clearance 8; verify_lyapunov_stability requires clearance 9
    with pytest.raises(PermissionError) as exc_info:
        registry.invoke(
            skill_name="verify_lyapunov_stability",
            agent_id="GAIA-NAVIER",
            agent_clearance=8,
            jacobian_flat=[-1.0, 0.0, 0.0, -1.0],
            dim=2,
        )
    assert "[RBAC VIOLATION]" in str(exc_info.value)
    assert "GAIA-NAVIER" in str(exc_info.value)
    assert "Requires 9" in str(exc_info.value)

    # AEGIS-FORMAL has clearance 10; invocation must succeed
    res = registry.invoke(
        skill_name="verify_lyapunov_stability",
        agent_id="AEGIS-FORMAL",
        agent_clearance=10,
        jacobian_flat=[-1.0, 0.0, 0.0, -1.0],
        dim=2,
    )
    assert res["executed_by"] == "AEGIS-FORMAL"
    assert "execution_time_us" in res
    assert res["payload"]["lyapunov_certified_stable"] is True


def test_rbac_unknown_skill():
    """Verify invoking an unregistered skill raises KeyError with security message."""
    registry = SKILL_REGISTRY
    with pytest.raises(KeyError) as exc_info:
        registry.invoke(
            skill_name="quantum_teleport",
            agent_id="Q-SHOR-SHIELD",
            agent_clearance=10,
        )
    assert "[SECURITY FAULT]" in str(exc_info.value)


def test_tool_manifest_export():
    """Verify tool manifest exports all 4 skills with schemas and clearance levels."""
    manifest = SKILL_REGISTRY.export_tool_manifest()
    names = {s["name"] for s in manifest}
    expected_skills = {
        "solve_mhd_plasma_step",
        "optimize_ising_power_grid",
        "compute_orbital_laser_ephemeris",
        "verify_lyapunov_stability",
    }
    assert expected_skills.issubset(names), f"Missing skills: {expected_skills - names}"

    for skill in manifest:
        assert "domain" in skill
        assert "description" in skill
        assert "parameters" in skill
        assert 1 <= skill["required_clearance"] <= 10


# ============================================================================
# 3. MATHEMATICAL SKILLS: SPECTRAL 2D MHD, ISING, J2, LYAPUNOV
# ============================================================================

def test_spectral_mhd_solver_direct():
    """Verify direct Fourier pseudo-spectral 2D MHD integration with Orszag-Tang vortex."""
    solver = SpectralMHDSolver2D(N=32, nu=0.01, eta=0.01)
    omega0 = -2.0 * np.sin(solver.X) - 2.0 * np.sin(solver.Y)
    psi0 = np.cos(solver.X) + 0.5 * np.cos(2.0 * solver.Y)

    omega, psi = omega0.copy(), psi0.copy()
    for _ in range(5):
        omega, psi = solver.step_rk4(omega, psi, dt=0.005)

    assert omega.shape == (32, 32)
    assert psi.shape == (32, 32)
    assert np.all(np.isfinite(omega))
    assert np.all(np.isfinite(psi))


def test_spectral_mhd_skill_invocation():
    """Verify solve_mhd_plasma_step skill returns regime and telemetry."""
    res = skill_solve_mhd(grid_size=32, steps=10, dt=0.005, nu=0.01, eta=0.01)
    assert "plasma_regime" in res
    assert res["plasma_regime"] in ["H-MODE_CONFINED", "TEARING_MODE_WARNING"]
    assert res["max_vorticity_rad_s"] > 0.0
    assert res["rms_magnetic_flux_weber"] > 0.0
    assert isinstance(res["recommended_poloidal_coil_delta_ka"], float)

    # Edge cases
    with pytest.raises(ValueError):
        skill_solve_mhd(grid_size=-4)


def test_ising_ground_state_exact():
    """Verify Ising Hamiltonian ground state search and spectral gap."""
    res = skill_optimize_ising_grid(num_nodes=8, seed=2027)
    assert isinstance(res["ground_state_energy_eigenvalue"], float)
    assert res["spectral_gap_delta_e"] >= 0.0
    assert len(res["optimal_hvdc_bus_spin_bitstring"]) == 8
    assert all(c in "01" for c in res["optimal_hvdc_bus_spin_bitstring"])
    assert isinstance(res["adiabatic_protection_verified"], bool)

    # Reproducibility check with fixed seed
    res2 = skill_optimize_ising_grid(num_nodes=8, seed=2027)
    assert res["ground_state_energy_eigenvalue"] == res2["ground_state_energy_eigenvalue"]
    assert res["optimal_hvdc_bus_spin_bitstring"] == res2["optimal_hvdc_bus_spin_bitstring"]

    # Edge cases
    with pytest.raises(ValueError):
        skill_optimize_ising_grid(num_nodes=0)
    with pytest.raises(ValueError):
        skill_optimize_ising_grid(num_nodes=30)


def test_j2_orbital_laser_ephemeris():
    """Verify J2 RAAN precession, Bradley aberration lead angle, and GR/SR clock drift."""
    res = skill_orbital_ephemeris(altitude_km=1150.0, inclination_deg=53.2)
    assert 7.0 <= res["orbital_velocity_km_s"] <= 7.5, f"Unexpected orbital velocity: {res['orbital_velocity_km_s']}"
    assert res["j2_raan_precession_deg_per_day"] < 0.0, "Prograde orbit must exhibit nodal regression"
    assert 40.0 <= res["laser_point_ahead_lead_angle_urad"] <= 60.0, "Point-ahead angle must be ~48 urad"
    assert isinstance(res["gr_sr_atomic_clock_offset_ppb"], float)

    # Edge cases
    with pytest.raises(ValueError):
        skill_orbital_ephemeris(altitude_km=-100.0)


def test_lyapunov_stable_jacobian():
    """Verify Continuous-Time Algebraic Lyapunov equation certifies stable Hurwitz Jacobian."""
    # Closed loop Hurwitz matrix with strictly negative real eigenvalues
    jacobian_flat = [
        -3.2,  0.8,  0.0,
        -0.8, -2.5,  0.4,
         0.0, -0.4, -4.1,
    ]
    res = skill_verify_lyapunov(jacobian_flat=jacobian_flat, dim=3)
    assert res["lyapunov_certified_stable"] is True
    assert res["safety_interlock_action"] == "COMMIT_APPROVED"
    assert res["min_eigenvalue_P"] > 0.0
    assert res["max_real_eigenvalue_A"] < 0.0


def test_lyapunov_unstable_jacobian():
    """Verify Continuous-Time Algebraic Lyapunov equation VETOES unstable Jacobian."""
    # Matrix with positive eigenvalue +1.0
    jacobian_flat = [
        1.0, 0.0, 0.0,
        0.0, -2.0, 0.0,
        0.0, 0.0, -3.0,
    ]
    res = skill_verify_lyapunov(jacobian_flat=jacobian_flat, dim=3)
    assert res["lyapunov_certified_stable"] is False
    assert res["safety_interlock_action"] == "EMERGENCY_SCRAM_VETO"
    assert res["max_real_eigenvalue_A"] > 0.0

    # Dimension mismatch
    with pytest.raises(ValueError):
        skill_verify_lyapunov(jacobian_flat=[1.0, 2.0], dim=3)


# ============================================================================
# 4. PANTHEON AGENTS YAML PROMPTS SCHEMA & CONTRACTS
# ============================================================================

def test_pantheon_yaml_schema():
    """Verify prompts/pantheon_system_prompts.yaml defines all 5 agents with valid contracts."""
    yaml_path = Path("prompts/pantheon_system_prompts.yaml")
    assert yaml_path.exists(), "prompts/pantheon_system_prompts.yaml does not exist"

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data["version"] == "2027.1.0-OMEGA"
    assert data["classification"] == "TIER-0-PLANETARY-CORE"

    agents = {a["id"]: a for a in data["agents"]}
    expected_agents = {
        "CHRONOS-PRIME": 10,
        "HELIOS-MHD": 9,
        "GAIA-NAVIER": 8,
        "Q-SHOR-SHIELD": 9,
        "AEGIS-FORMAL": 10,
    }

    assert len(agents) == 5, f"Expected 5 agents, found {len(agents)}"
    for agent_id, exp_clearance in expected_agents.items():
        assert agent_id in agents, f"Agent {agent_id} missing from YAML"
        agent = agents[agent_id]
        assert agent["clearance_level"] == exp_clearance, f"Clearance mismatch for {agent_id}"
        assert len(agent["role"]) > 5
        prompt = agent["system_prompt"]
        assert len(prompt) > 50

    # Contract specific checks
    assert "AEGIS-FORMAL" in agents["CHRONOS-PRIME"]["system_prompt"]
    assert "Lyapunov" in agents["CHRONOS-PRIME"]["system_prompt"]
    assert "Lawson" in agents["HELIOS-MHD"]["system_prompt"]
    assert "MHD" in agents["HELIOS-MHD"]["system_prompt"]
    assert "divergence-free" in agents["GAIA-NAVIER"]["system_prompt"]
    assert "Surface Code" in agents["Q-SHOR-SHIELD"]["system_prompt"]
    assert "VETO" in agents["AEGIS-FORMAL"]["system_prompt"]
    assert "Lyapunov" in agents["AEGIS-FORMAL"]["system_prompt"]


# ============================================================================
# 5. 3D NAVIER-STOKES MHD PINN DIVERGENCE-FREE POTENTIALS & LOSS
# ============================================================================

def test_pinn_vector_potentials_divergence_free():
    """Verify divergence-free property: div(u) == 0 and div(B) == 0."""
    pinn = DivergenceFreeMHDPINN()
    x = [0.1, 0.2, 0.3]
    y = [0.4, 0.5, 0.6]
    z = [0.7, 0.8, 0.9]
    t = [0.0, 0.05, 0.1]

    div_check = pinn.verify_divergence_free(x, y, z, t)
    assert div_check["is_divergence_free"] is True
    assert div_check["max_abs_div_u"] < 1e-4, f"Divergence of u too high: {div_check['max_abs_div_u']}"
    assert div_check["max_abs_div_B"] < 1e-4, f"Divergence of B too high: {div_check['max_abs_div_B']}"


def test_pinn_pde_residuals_computation():
    """Verify computation of Navier-Stokes and Maxwell induction PDE residuals."""
    pinn = DivergenceFreeMHDPINN()
    x = [0.2, 0.5]
    y = [0.3, 0.6]
    z = [0.4, 0.7]
    t = [0.0, 0.1]

    loss_dict = pinn.pde_residual_loss(x, y, z, t, nu=1e-3, eta=1e-3, rho=1.0)
    assert "total_physics_loss" in loss_dict
    assert "navier_stokes_momentum_loss" in loss_dict
    assert "maxwell_induction_loss" in loss_dict

    tot = float(loss_dict["total_physics_loss"])
    mom = float(loss_dict["navier_stokes_momentum_loss"])
    ind = float(loss_dict["maxwell_induction_loss"])

    assert np.isfinite(tot) and tot >= 0.0
    assert np.isfinite(mom) and mom >= 0.0
    assert np.isfinite(ind) and ind >= 0.0
    assert abs(tot - (mom + ind)) < 1e-4


# ============================================================================
# 6. FULL MULTI-ROUND PLANETARY SWARM CYCLE E2E
# ============================================================================

def test_planetary_swarm_cycle_e2e():
    """Verify end-to-end execution of full multi-round swarm cycle with DAG commitment."""
    result = asyncio.run(run_planetary_swarm_cycle())
    assert result["status"] == "SUCCESS"
    assert result["consensus_decision"] == "COMMIT_APPROVED"
    assert result["total_vertices"] >= 5
    assert len(result["final_commit_hash"]) == 128
    assert result["is_chain_valid"] is True
