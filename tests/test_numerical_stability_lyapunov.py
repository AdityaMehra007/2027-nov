#!/usr/bin/env python3
"""
Comprehensive Formal Verification Suite for:
1. Continuous-Time Algebraic Lyapunov Equation: A^T P + P A = -Q
   - Unique solution P is symmetric positive definite (min lambda(P) > 0) for Hurwitz A
   - Positive or zero real eigenvalues in A fail Hurwitz stability and trigger EMERGENCY_SCRAM_VETO
   - Dimensions dim = 2, 3, 4, 6:
     * dim = 2: Damped planar oscillator & magnetic drift
     * dim = 3: ITER scrape-off layer 3-state transport model
     * dim = 4: Tokamak plasma perturbation matrix (delta_psi, delta_j_phi, delta_v_r, delta_T_e)
     * dim = 6: Orbital laser attitude Jacobian (3-DOF Euler angles + 3-DOF body rates)
   - General symmetric positive definite weighting matrices Q
   - Lyapunov candidate function dissipation rate dV/dt = -x^T Q x < 0 along trajectories
2. Numerical Convergence and Conservation Laws:
   a) Quantum wavepacket norm unitarity (||psi||_2 == 1.0) via Crank-Nicolson TDSE
   b) Double-entry ledger zero-sum conservation (sum(B_i) == 0) across multi-party transactions
   c) Divergence-free vector potential fields (div(u) == 0, div(B) == 0)
   d) Thermodynamic energy bounds in DAG state transitions (|Delta E| <= 1 TW)
"""

import math
from typing import Any, Dict, List, Tuple

import numpy as np
import pytest
import scipy.linalg as la

import prometheus_universal_genesis as pug
from src.agents.swarm_runtime import (
    SKILL_REGISTRY,
    skill_verify_lyapunov,
)
from src.kernel.standalone_runner import (
    PlanetaryState,
    PlanetaryStateTransition,
)
from src.omni_corp_engine import ImmutableDoubleEntryLedger
from src.pinn.navier_stokes_mhd_pinn import (
    DivergenceFreeMHDPINN,
    NumpyDivergenceFreeMHDPINN,
)


# ============================================================================
# HELPER: DIRECT LYAPUNOV SOLVER & RESIDUAL COMPUTATION
# ============================================================================

def solve_lyapunov_direct(
    A: np.ndarray, Q: np.ndarray | None = None
) -> Tuple[np.ndarray, float, float, float]:
    """
    Solves A^T P + P A = -Q directly using Bartels-Stewart Schur decomposition.
    Returns:
      P: symmetric solution matrix
      min_eig_P: smallest eigenvalue of P
      max_real_eig_A: largest real part of eigenvalues of A
      residual_norm: Frobenius norm ||A^T P + P A + Q||_F
    """
    dim = A.shape[0]
    if Q is None:
        Q = np.eye(dim, dtype=np.float64)

    eig_A = np.linalg.eigvals(A)
    max_real_A = float(np.max(np.real(eig_A)))

    # scipy.linalg.solve_continuous_lyapunov(a, q) solves a X + X a^H = q
    # With a = A^T and q = -Q, this gives A^T P + P A = -Q
    P = la.solve_continuous_lyapunov(A.T, -Q)
    # Symmetrize to eliminate numerical asymmetry
    P = 0.5 * (P + P.T)
    eig_P = np.linalg.eigvalsh(P)
    min_eig_P = float(np.min(eig_P))

    residual = A.T @ P + P @ A + Q
    residual_norm = float(la.norm(residual, "fro"))

    return P, min_eig_P, max_real_A, residual_norm


# ============================================================================
# 1. CONTINUOUS-TIME ALGEBRAIC LYAPUNOV EQUATION (A^T P + P A = -Q)
# ============================================================================

class TestLyapunovEquationFormalVerification:
    """Formal mathematical validation of Continuous-Time Algebraic Lyapunov Equation."""

    def test_lyapunov_residual_zero_for_hurwitz_matrix(self):
        """Verify ||A^T P + P A + Q||_F < 1e-10 for Hurwitz stable Jacobian."""
        # 3x3 Hurwitz matrix
        A = np.array([
            [-3.5,  0.9,  0.0],
            [-0.9, -2.8,  0.3],
            [ 0.0, -0.3, -4.2],
        ], dtype=np.float64)
        Q = np.eye(3, dtype=np.float64)

        P, min_eig_P, max_real_A, residual_norm = solve_lyapunov_direct(A, Q)

        assert max_real_A < 0.0, "Hurwitz matrix must have strictly negative real poles"
        assert min_eig_P > 0.0, "Solution P must be strictly positive definite"
        assert residual_norm < 1e-10, f"Lyapunov residual must be near zero, got {residual_norm}"

        # Verify symmetry of P
        assert la.norm(P - P.T, "fro") < 1e-12, "P must be strictly symmetric"

    def test_lyapunov_general_positive_definite_Q(self):
        """Verify A^T P + P A = -Q holds for arbitrary symmetric positive definite Q != I."""
        dim = 4
        # Construct stable Hurwitz A
        A = np.array([
            [-4.0,  1.0,  0.2, -0.1],
            [-0.5, -3.5,  0.8,  0.0],
            [ 0.0, -0.4, -5.0,  0.6],
            [ 0.2, -0.1, -0.5, -4.5],
        ], dtype=np.float64)

        # Construct non-trivial symmetric positive definite Q
        M = np.array([
            [2.0, 0.5, 0.1, 0.0],
            [0.1, 1.8, 0.3, 0.2],
            [0.0, 0.2, 2.5, 0.4],
            [0.3, 0.0, 0.1, 1.5],
        ], dtype=np.float64)
        Q = M.T @ M + np.eye(dim) * 0.5  # Guaranteed strictly positive definite

        P, min_eig_P, max_real_A, residual_norm = solve_lyapunov_direct(A, Q)

        assert min_eig_P > 0.0, "P must be positive definite for any Q > 0"
        assert residual_norm < 1e-10, f"Residual must be < 1e-10, got {residual_norm}"

    def test_lyapunov_candidate_dissipation_rate(self):
        """Verify dV/dt = x^T (A^T P + P A) x = -x^T Q x < 0 along sampled trajectories."""
        A = np.array([
            [-2.0,  0.5],
            [-0.5, -3.0],
        ], dtype=np.float64)
        Q = np.eye(2, dtype=np.float64)
        P, min_eig_P, max_real_A, _ = solve_lyapunov_direct(A, Q)

        rng = np.random.default_rng(2027)
        for _ in range(50):
            x = rng.normal(size=2)
            if np.linalg.norm(x) < 1e-6:
                continue
            # V(x) = x^T P x > 0
            V = float(x.T @ P @ x)
            assert V > 0.0, "Lyapunov function V(x) must be strictly positive"

            # V_dot = x^T (A^T P + P A) x == -x^T Q x
            V_dot_lyap = float(x.T @ (A.T @ P + P @ A) @ x)
            V_dot_Q = float(-x.T @ Q @ x)

            assert abs(V_dot_lyap - V_dot_Q) < 1e-10, "V_dot must equal -x^T Q x"
            assert V_dot_lyap < 0.0, "Time derivative of V(x) must be strictly negative"


# ============================================================================
# 2. HURWITZ STABILITY CHECK & EMERGENCY_SCRAM_VETO TRIGGERING
# ============================================================================

class TestHurwitzStabilityAndScramInterlock:
    """Verifies that unstable or non-strictly Hurwitz matrices trigger EMERGENCY_SCRAM_VETO."""

    def test_strictly_positive_eigenvalue_triggers_scram(self):
        """Verify positive real eigenvalue triggers EMERGENCY_SCRAM_VETO."""
        unstable_jac = [
            1.5,  0.0,  0.0,
            0.0, -2.5,  0.0,
            0.0,  0.0, -3.0,
        ]
        res = skill_verify_lyapunov(jacobian_flat=unstable_jac, dim=3)
        assert res["lyapunov_certified_stable"] is False
        assert res["safety_interlock_action"] == "EMERGENCY_SCRAM_VETO"
        assert res["max_real_eigenvalue_A"] >= 1.5

    def test_zero_real_eigenvalue_triggers_scram(self):
        """Verify zero real eigenvalue (neutral/marginal stability) fails check and triggers SCRAM."""
        # Purely imaginary poles +/- 2i (undamped harmonic oscillator)
        undamped_osc = [
            0.0,  2.0,
           -2.0,  0.0,
        ]
        res = skill_verify_lyapunov(jacobian_flat=undamped_osc, dim=2)
        assert res["lyapunov_certified_stable"] is False
        assert res["safety_interlock_action"] == "EMERGENCY_SCRAM_VETO"
        assert abs(res["max_real_eigenvalue_A"]) < 1e-5

    def test_complex_conjugate_unstable_pair_triggers_scram(self):
        """Verify growing oscillatory mode (positive real part in complex pole) triggers SCRAM."""
        # Poles: +0.5 +/- 3.0i
        flutter_jac = [
            0.5,  3.0,
           -3.0,  0.5,
        ]
        res = skill_verify_lyapunov(jacobian_flat=flutter_jac, dim=2)
        assert res["lyapunov_certified_stable"] is False
        assert res["safety_interlock_action"] == "EMERGENCY_SCRAM_VETO"
        assert res["max_real_eigenvalue_A"] > 0.0

    def test_scram_interlock_via_skill_registry(self):
        """Verify AEGIS-FORMAL role invocation via SKILL_REGISTRY enforces interlock veto."""
        unstable_jac = [
            0.8, -0.4,
            0.2, -1.5,
        ]
        res = SKILL_REGISTRY.invoke(
            skill_name="verify_lyapunov_stability",
            agent_id="AEGIS-FORMAL",
            agent_clearance=10,
            jacobian_flat=unstable_jac,
            dim=2,
        )
        assert res["payload"]["lyapunov_certified_stable"] is False
        assert res["payload"]["safety_interlock_action"] == "EMERGENCY_SCRAM_VETO"

    def test_engine_17_meta_verifier_veto(self):
        """Verify Engine 17 verify_continuous_lyapunov vetoes unstable system."""
        unstable_mat = [2.0, 0.0, 0.0, -1.0]
        verif = pug.verify_continuous_lyapunov(unstable_mat, dim=2)
        assert verif["certified_stable"] is False
        assert verif["max_real_pole"] > 0.0

    def test_lyapunov_nan_inf_inputs_trigger_scram_veto(self):
        """Verify unphysical NaN and Inf inputs immediately issue EMERGENCY_SCRAM_VETO without crashing."""
        nan_jac = [float("nan"), 0.0, 0.0, -1.0]
        res_nan = skill_verify_lyapunov(jacobian_flat=nan_jac, dim=2)
        assert res_nan["lyapunov_certified_stable"] is False
        assert res_nan["safety_interlock_action"] == "EMERGENCY_SCRAM_VETO"

        inf_jac = [float("inf"), 1.0, 0.0, -2.0]
        res_inf = skill_verify_lyapunov(jacobian_flat=inf_jac, dim=2)
        assert res_inf["lyapunov_certified_stable"] is False
        assert res_inf["safety_interlock_action"] == "EMERGENCY_SCRAM_VETO"


# ============================================================================
# 3. LYAPUNOV VERIFICATION ACROSS DIMENSIONS (dim = 2, 3, 4, 6)
# ============================================================================

class TestLyapunovAcrossDimensions:
    """Verifies Lyapunov equation solving across dimensions 2, 3, 4, and 6."""

    def test_dimension_2_planar_damped_drift(self):
        """Verify dim = 2: Damped 2nd-order harmonic oscillator / magnetic drift."""
        omega_n = 2.5
        zeta = 0.7  # Damped oscillator poles at -1.75 +/- 1.785i
        A_2d = [
            0.0, 1.0,
            -(omega_n**2), -2.0 * zeta * omega_n,
        ]
        res = skill_verify_lyapunov(jacobian_flat=A_2d, dim=2)
        assert res["lyapunov_certified_stable"] is True
        assert res["safety_interlock_action"] == "COMMIT_APPROVED"
        assert res["min_eigenvalue_P"] > 0.0
        assert res["max_real_eigenvalue_A"] < -1.0

    def test_dimension_3_iter_transport_jacobian(self):
        """Verify dim = 3: 3-state chemical / ITER scrape-off layer transport model."""
        A_3d = [
            -3.5,  0.9,  0.0,
            -0.9, -2.8,  0.3,
             0.0, -0.3, -4.2,
        ]
        res = skill_verify_lyapunov(jacobian_flat=A_3d, dim=3)
        assert res["lyapunov_certified_stable"] is True
        assert res["safety_interlock_action"] == "COMMIT_APPROVED"
        assert res["min_eigenvalue_P"] > 0.0
        assert res["max_real_eigenvalue_A"] < 0.0

    def test_dimension_4_tokamak_plasma_perturbation_matrix(self):
        """
        Verify dim = 4: Tokamak plasma perturbation matrix:
        State vector: x = [delta_psi, delta_j_phi, delta_v_r, delta_T_e]^T
        Coupled magnetic flux, toroidal current density, radial velocity displacement,
        and electron temperature perturbations under active poloidal magnetic coil feedback.
        """
        # Stable Tokamak Jacobian under active LQR magnetic feedback:
        # Strictly diagonally dominant / Hurwitz with all Gershgorin discs < 0
        A_tokamak_stable = [
            -4.5,  0.8, -1.2,  0.3,
            -0.6, -5.2,  0.4, -0.2,
             1.1, -0.5, -3.8,  0.5,
            -0.2,  0.3, -0.4, -6.1,
        ]
        res_stable = skill_verify_lyapunov(jacobian_flat=A_tokamak_stable, dim=4)
        assert res_stable["lyapunov_certified_stable"] is True
        assert res_stable["safety_interlock_action"] == "COMMIT_APPROVED"
        assert res_stable["min_eigenvalue_P"] > 0.0
        assert res_stable["max_real_eigenvalue_A"] < 0.0

        # Unstable Tokamak Jacobian: Tearing mode resistive wall instability (growth rate > 0)
        A_tokamak_unstable = [
             2.8,  1.2, -0.5,  0.1,  # Positive tearing growth rate gamma > 0
            -0.4, -4.0,  0.3, -0.2,
             0.9, -0.3, -3.1,  0.4,
            -0.1,  0.2, -0.3, -5.0,
        ]
        res_unstable = skill_verify_lyapunov(jacobian_flat=A_tokamak_unstable, dim=4)
        assert res_unstable["lyapunov_certified_stable"] is False
        assert res_unstable["safety_interlock_action"] == "EMERGENCY_SCRAM_VETO"
        assert res_unstable["max_real_eigenvalue_A"] > 0.0

    def test_dimension_6_orbital_laser_attitude_jacobian(self):
        """
        Verify dim = 6: Orbital laser terminal 6-DOF attitude control Jacobian:
        State vector: x = [phi, theta, psi, omega_x, omega_y, omega_z]^T
        Kinematics (3 Euler angles) and Dynamics (3 body angular rates)
        under stabilized proportional-derivative reaction wheel and magnetic torquer feedback.
        """
        # Linearized 6-DOF closed loop:
        # d/dt [theta_err] = [omega]
        # d/dt [omega] = -I^{-1} K_p [theta_err] - I^{-1} K_d [omega]
        # For diagonal inertia I = diag(100, 100, 80) kg*m^2,
        # K_p = diag(500, 500, 400), K_d = diag(300, 300, 240):
        # -I^{-1} K_p = diag(-5.0, -5.0, -5.0)
        # -I^{-1} K_d = diag(-3.0, -3.0, -3.0)
        # Block matrix:
        # [ 0,  0,  0,  1,  0,  0 ]
        # [ 0,  0,  0,  0,  1,  0 ]
        # [ 0,  0,  0,  0,  0,  1 ]
        # [-5,  0,  0, -3,  0,  0 ]
        # [ 0, -5,  0,  0, -3,  0 ]
        # [ 0,  0, -5,  0,  0, -3 ]
        A_orbital_laser_stable = [
             0.0,  0.0,  0.0,  1.0,  0.0,  0.0,
             0.0,  0.0,  0.0,  0.0,  1.0,  0.0,
             0.0,  0.0,  0.0,  0.0,  0.0,  1.0,
            -5.0,  0.0,  0.0, -3.0,  0.0,  0.0,
             0.0, -5.0,  0.0,  0.0, -3.0,  0.0,
             0.0,  0.0, -5.0,  0.0,  0.0, -3.0,
        ]
        res_stable = skill_verify_lyapunov(jacobian_flat=A_orbital_laser_stable, dim=6)
        assert res_stable["lyapunov_certified_stable"] is True
        assert res_stable["safety_interlock_action"] == "COMMIT_APPROVED"
        assert res_stable["min_eigenvalue_P"] > 0.0
        assert res_stable["max_real_eigenvalue_A"] < -1.0  # Real poles at -1.5

        # Unstable laser attitude Jacobian: Actuator polarity reversal / gyro drift runaway
        A_orbital_laser_unstable = list(A_orbital_laser_stable)
        A_orbital_laser_unstable[18] = 5.0  # Positive feedback on roll axis
        res_unstable = skill_verify_lyapunov(jacobian_flat=A_orbital_laser_unstable, dim=6)
        assert res_unstable["lyapunov_certified_stable"] is False
        assert res_unstable["safety_interlock_action"] == "EMERGENCY_SCRAM_VETO"
        assert res_unstable["max_real_eigenvalue_A"] > 0.0

    def test_dimension_mismatch_raises_value_error(self):
        """Verify invalid array lengths for specified dimension raise ValueError."""
        with pytest.raises(ValueError):
            skill_verify_lyapunov(jacobian_flat=[1.0, 2.0, 3.0], dim=2)  # Needs 4

        with pytest.raises(ValueError):
            skill_verify_lyapunov(jacobian_flat=[1.0] * 15, dim=4)  # Needs 16


# ============================================================================
# 4. NUMERICAL CONVERGENCE & CONSERVATION LAWS
# ============================================================================

class TestNumericalConservationLaws:
    """Verifies fundamental physical and architectural conservation invariants."""

    # ------------------------------------------------------------------------
    # a) Quantum Wavepacket Norm Unitarity (||psi||_2 == 1.0)
    # ------------------------------------------------------------------------
    def test_quantum_wavepacket_norm_unitarity_crank_nicolson(self):
        """
        Verify quantum wavepacket norm unitarity ||psi||_2 == 1.000000000000
        across time steps using unconditional Crank-Nicolson unitary propagator.
        i*hbar*d(psi)/dt = (-hbar^2/(2m) d^2/dx^2 + V(x)) psi
        Propagator: (I + i*dt/2 * H) psi^{n+1} = (I - i*dt/2 * H) psi^n
        """
        N = 128
        steps = 60
        dt = 0.02
        x = np.linspace(-10.0, 10.0, N)
        dx = x[1] - x[0]

        # Initial normalized Gaussian wavepacket traveling with momentum k0 = 2.5
        psi = np.exp(-0.5 * ((x + 3.0) / 1.0) ** 2) * np.exp(1j * 2.5 * x)
        initial_norm = float(np.sum(np.abs(psi) ** 2) * dx)
        psi /= np.sqrt(initial_norm)

        # Hamiltonian matrix with finite-difference kinetic energy + barrier potential
        V = np.where((x >= 0.0) & (x <= 1.0), 3.0, 0.0)
        diag = (1.0 / (dx**2)) + V
        off_diag = -0.5 / (dx**2) * np.ones(N - 1)
        H = np.diag(diag) + np.diag(off_diag, 1) + np.diag(off_diag, -1)

        # Cayley transform unitary propagator: U = (I + i*dt/2*H)^{-1} (I - i*dt/2*H)
        I_mat = np.eye(N, dtype=np.complex128)
        A_prop = I_mat + 0.5j * dt * H
        B_prop = I_mat - 0.5j * dt * H
        U = la.inv(A_prop) @ B_prop

        # Verify exact matrix unitarity U^\dagger U = I
        U_dagger_U = U.conj().T @ U
        assert la.norm(U_dagger_U - I_mat, "fro") < 1e-11, "Propagator U must be strictly unitary"

        # Propagate wavepacket and assert norm unitarity at every 10 steps
        for step in range(1, steps + 1):
            psi = U @ psi
            if step % 10 == 0:
                norm_step = float(np.sum(np.abs(psi) ** 2) * dx)
                assert abs(norm_step - 1.0) < 1e-10, (
                    f"Quantum wavepacket unitarity violated at step {step}: ||psi||_2 = {norm_step}"
                )

        final_norm = float(np.sum(np.abs(psi) ** 2) * dx)
        assert abs(final_norm - 1.0) < 1e-10, f"Final norm drift: {abs(final_norm - 1.0)}"

    # ------------------------------------------------------------------------
    # b) Double-Entry Ledger Zero-Sum Conservation (sum(B_i) == 0)
    # ------------------------------------------------------------------------
    def test_double_entry_ledger_zero_sum_conservation(self):
        """
        Verify double-entry ledger balance conservation:
        Sum(Balance_i) == 0 at all times across high-frequency multi-account transactions.
        """
        ledger = ImmutableDoubleEntryLedger()
        accounts = ["TREASURY", "ESCROW", "CLIENT_VAULT", "RESERVE", "SETTLEMENT"]

        # Initial state must be zero
        assert sum(ledger.balances_cents.values()) == 0

        # Execute 50 structured and cyclic transactions
        tx_plan = [
            ("tx_001", "TREASURY", "ESCROW", 500_000_00),
            ("tx_002", "ESCROW", "CLIENT_VAULT", 250_000_00),
            ("tx_003", "CLIENT_VAULT", "SETTLEMENT", 120_000_00),
            ("tx_004", "SETTLEMENT", "RESERVE", 100_000_00),
            ("tx_005", "RESERVE", "TREASURY", 50_000_00),
        ]

        for tx_id, debit, credit, amount in tx_plan:
            receipt = ledger.commit_transfer(
                idempotency_key=tx_id,
                debit_account=debit,
                credit_account=credit,
                amount_cents=amount,
            )
            assert receipt["zero_sum_invariant_verified"] is True
            assert len(receipt["tx_hash"]) == 128
            # Strict invariant check: Sum(Balances) == 0
            assert sum(ledger.balances_cents.values()) == 0, "Double-entry zero-sum violated!"

        # Random multi-party transfers
        rng = np.random.default_rng(2027)
        for i in range(50):
            d_idx, c_idx = rng.choice(len(accounts), size=2, replace=False)
            amount = int(rng.integers(100, 10_000_00))
            ledger.commit_transfer(
                idempotency_key=f"rand_tx_{i:04d}",
                debit_account=accounts[d_idx],
                credit_account=accounts[c_idx],
                amount_cents=amount,
            )
            assert sum(ledger.balances_cents.values()) == 0, (
                f"Ledger zero-sum violated after transaction rand_tx_{i:04d}"
            )

        # Idempotency replay check: identical key does not alter balances
        pre_balances = dict(ledger.balances_cents)
        replay_res = ledger.commit_transfer(
            idempotency_key="tx_001",
            debit_account="TREASURY",
            credit_account="ESCROW",
            amount_cents=500_000_00,
        )
        assert replay_res["idempotent_cache_hit"] is True
        assert ledger.balances_cents == pre_balances
        assert sum(ledger.balances_cents.values()) == 0

        # Invalid transfer: non-positive amounts rejected without altering zero-sum
        with pytest.raises(ValueError):
            ledger.commit_transfer("bad_tx_neg", "TREASURY", "ESCROW", -500)
        with pytest.raises(ValueError):
            ledger.commit_transfer("bad_tx_zero", "TREASURY", "ESCROW", 0)
        assert sum(ledger.balances_cents.values()) == 0

    # ------------------------------------------------------------------------
    # c) Divergence-Free Vector Potential Fields (div(u) == 0, div(B) == 0)
    # ------------------------------------------------------------------------
    def test_divergence_free_vector_potentials_numpy_and_pinn(self):
        """
        Verify that curl-based vector potential formulations mathematically and
        numerically guarantee div(u) == 0 and div(B) == 0 everywhere.
        u = curl(A_fluid) -> div(curl(A)) == 0
        B = curl(A_mag)   -> div(curl(A)) == 0
        """
        # Test 1: DivergenceFreeMHDPINN API check
        pinn = DivergenceFreeMHDPINN()
        x_pts = [0.15, 0.35, 0.65, 0.85]
        y_pts = [0.25, 0.45, 0.75, 0.95]
        z_pts = [0.10, 0.50, 0.80, 0.20]
        t_pts = [0.00, 0.05, 0.10, 0.15]

        div_result = pinn.verify_divergence_free(x_pts, y_pts, z_pts, t_pts)
        assert div_result["is_divergence_free"] is True
        assert div_result["max_abs_div_u"] < 1e-4, f"div(u) exceeded bound: {div_result['max_abs_div_u']}"
        assert div_result["max_abs_div_B"] < 1e-4, f"div(B) exceeded bound: {div_result['max_abs_div_B']}"

        # Test 2: Direct NumPy high-order central difference verification
        numpy_pinn = NumpyDivergenceFreeMHDPINN(hidden_dim=32, num_layers=2, seed=2027)
        for (xp, yp, zp, tp) in zip(x_pts, y_pts, z_pts, t_pts):
            u, v, w, Bx, By, Bz, _ = numpy_pinn.compute_fields(xp, yp, zp, tp)
            # Evaluate spatial derivatives with central finite difference
            h = 1e-4
            u_xp, _, _, _, _, _, _ = numpy_pinn.compute_fields(xp + h, yp, zp, tp)
            u_xm, _, _, _, _, _, _ = numpy_pinn.compute_fields(xp - h, yp, zp, tp)
            du_dx = (u_xp - u_xm) / (2.0 * h)

            _, v_yp, _, _, _, _, _ = numpy_pinn.compute_fields(xp, yp + h, zp, tp)
            _, v_ym, _, _, _, _, _ = numpy_pinn.compute_fields(xp, yp - h, zp, tp)
            dv_dy = (v_yp - v_ym) / (2.0 * h)

            _, _, w_zp, _, _, _, _ = numpy_pinn.compute_fields(xp, yp, zp + h, tp)
            _, _, w_zm, _, _, _, _ = numpy_pinn.compute_fields(xp, yp, zp - h, tp)
            dw_dz = (w_zp - w_zm) / (2.0 * h)

            div_u = du_dx + dv_dy + dw_dz
            assert abs(div_u) < 1e-4, f"Numerical div(u) at ({xp},{yp},{zp}) exceeded bound: {div_u}"

            Bx_xp, _, _, _, _, _, _ = numpy_pinn.compute_fields(xp + h, yp, zp, tp)
            Bx_xm, _, _, _, _, _, _ = numpy_pinn.compute_fields(xp - h, yp, zp, tp)
            # Check magnetic field divergence
            _, _, _, Bx_p, _, _, _ = numpy_pinn.compute_fields(xp + h, yp, zp, tp)
            _, _, _, Bx_m, _, _, _ = numpy_pinn.compute_fields(xp - h, yp, zp, tp)
            dBx_dx = (Bx_p - Bx_m) / (2.0 * h)

            _, _, _, _, By_p, _, _ = numpy_pinn.compute_fields(xp, yp + h, zp, tp)
            _, _, _, _, By_m, _, _ = numpy_pinn.compute_fields(xp, yp - h, zp, tp)
            dBy_dy = (By_p - By_m) / (2.0 * h)

            _, _, _, _, _, Bz_p, _ = numpy_pinn.compute_fields(xp, yp, zp + h, tp)
            _, _, _, _, _, Bz_m, _ = numpy_pinn.compute_fields(xp, yp, zp - h, tp)
            dBz_dz = (Bz_p - Bz_m) / (2.0 * h)

            div_B = dBx_dx + dBy_dy + dBz_dz
            assert abs(div_B) < 1e-4, f"Numerical div(B) at ({xp},{yp},{zp}) exceeded bound: {div_B}"

    # ------------------------------------------------------------------------
    # d) Thermodynamic Energy Bounds in DAG State Transitions
    # ------------------------------------------------------------------------
    def test_dag_state_transition_thermodynamic_energy_bounds(self):
        """
        Verify thermodynamic energy bounds in DAG state transitions:
        - Deltas within 1 Terawatt (|Delta E| <= 10^18 microWatts) succeed.
        - Deltas exceeding 1 Terawatt raise ThermodynamicEnergyConservationViolation.
        - Unsuccessful transitions maintain strict state immutability (rollback).
        """
        state = PlanetaryState.genesis()
        assert state.cumulative_energy_uw == 0
        genesis_root = state.state_root

        # 1. Valid energy delta: +450 Megawatts = +450 * 10^12 uW
        delta_valid_1 = 450_000_000_000_000
        t1 = PlanetaryStateTransition(
            epoch_round=1,
            timestamp_tai_ns=1_000_000_000,
            net_energy_delta_uw=delta_valid_1,
            tokamak_quench_flags=0,
            orbital_laser_azimuth_urad=1500,
        )
        root_1 = t1.verify_and_apply(state)
        assert len(root_1) == 64
        assert state.cumulative_energy_uw == delta_valid_1
        assert state.epoch_round == 1

        # 2. Maximum exact boundary condition: 10^18 uW (1 TW) must succeed
        max_delta = 1_000_000_000_000_000_000
        t_bound = PlanetaryStateTransition(
            epoch_round=2,
            timestamp_tai_ns=2_000_000_000,
            net_energy_delta_uw=max_delta,
            tokamak_quench_flags=0,
            orbital_laser_azimuth_urad=2000,
        )
        root_2 = t_bound.verify_and_apply(state)
        assert state.cumulative_energy_uw == delta_valid_1 + max_delta

        # 3. Violation: 10^18 + 1 uW exceeds thermodynamic bound -> must fail
        violating_delta = 1_000_000_000_000_000_001
        pre_violation_energy = state.cumulative_energy_uw
        pre_violation_root = state.state_root

        t_violating = PlanetaryStateTransition(
            epoch_round=3,
            timestamp_tai_ns=3_000_000_000,
            net_energy_delta_uw=violating_delta,
            tokamak_quench_flags=0,
            orbital_laser_azimuth_urad=2500,
        )
        with pytest.raises(ValueError, match="ThermodynamicEnergyConservationViolation"):
            t_violating.verify_and_apply(state)

        # Invariant: state must be strictly unchanged after failed transition
        assert state.cumulative_energy_uw == pre_violation_energy
        assert state.state_root == pre_violation_root
        assert state.epoch_round == 2

        # 4. Negative bound violation: -(10^18 + 1) uW must also fail
        t_neg_violating = PlanetaryStateTransition(
            epoch_round=3,
            timestamp_tai_ns=3_500_000_000,
            net_energy_delta_uw=-violating_delta,
            tokamak_quench_flags=0,
            orbital_laser_azimuth_urad=2500,
        )
        with pytest.raises(ValueError, match="ThermodynamicEnergyConservationViolation"):
            t_neg_violating.verify_and_apply(state)

        assert state.cumulative_energy_uw == pre_violation_energy
