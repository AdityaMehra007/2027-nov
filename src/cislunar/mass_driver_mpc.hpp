// ============================================================================
// PROJECT AETHER-OMEGA (2027) — CISLUNAR MASS DRIVER MODEL PREDICTIVE CONTROLLER
// File: src/cislunar/mass_driver_mpc.hpp
// Standard: C++23 Header-Only Hard Real-Time Library
// Constraints: Zero Dynamic Heap Allocation, Deterministic Microsecond Commutation,
//              40km Electromagnetic Launch Track targeting 2375.01 m/s L1 injection
// ============================================================================

#pragma once

#include <cmath>
#include <cstdint>
#include <algorithm>

namespace AetherOmega::Cislunar {

    /// Telemetry frame sampled from the electromagnetic launch sled along the 40km lunar track
    struct SledTelemetry {
        double position_m;          ///< Sled position along the track (0.0 to 40,000.0 m)
        double velocity_m_s;        ///< Instantaneous sled velocity (m/s)
        double levitation_gap_mm;   ///< Halbach array magnetic levitation gap clearance (mm)
        double coil_temp_kelvin;    ///< Stator coil cryogenic temperature (K)
        double payload_mass_kg;     ///< Effective payload + sled mass (kg)
    };

    /// Actuation commands dispatched to stator coil Linear Synchronous Motor (LSM) drivers
    struct StatorCoilCommand {
        bool emergency_scram;              ///< True if emergency eddy-current brake is engaged
        double synchronous_frequency_hz;   ///< LSM stator commutation frequency (Hz)
        double phase_current_ka;           ///< Commutated 3-phase drive current (kA)
        double lorentz_thrust_n;           ///< Commanded electromagnetic Lorentz thrust (N)
        double halbach_damping_n;          ///< Restoring / damping force from Halbach levitation (N)
        double target_velocity_m_s;        ///< Nominal escape velocity target (2375.01 m/s)
    };

    /// Model Predictive Controller for Lunar Mass Driver Synchronous Commutation
    class CislunarMassDriverMPC {
    public:
        // Physical Constants and Mission Requirements
        static constexpr double TARGET_INJECTION_VELOCITY_M_S = 2375.01; ///< L1 Earth-Moon injection target
        static constexpr double TRACK_LENGTH_M = 40000.0;                 ///< Total 40 km electromagnetic track
        static constexpr double POLE_PITCH_M = 0.50;                     ///< Coil pole pitch tau_p (m)
        static constexpr double CRITICAL_COIL_TEMP_K = 77.0;             ///< Cryogenic LN2 boiling threshold (K)
        static constexpr double MIN_SAFE_GAP_MM = 3.0;                   ///< Track strike avoidance floor (mm)
        static constexpr double NOMINAL_LEVITATION_GAP_MM = 15.0;        ///< Equilibrium Halbach levitation gap (mm)
        static constexpr double MAX_PHASE_CURRENT_KA = 150.0;            ///< Inverter thermal limit (kA)
        static constexpr double LORENTZ_CURRENT_COEFF = 1.85e-4;         ///< Thrust-to-current factor (kA/N)
        static constexpr double HALBACH_STIFFNESS_N_MM = 4500.0;         ///< Magnetic gap stiffness (N/mm)
        static constexpr double VELOCITY_TRACKING_GAIN = 12.0;           ///< MPC closed-loop velocity tracking gain

        // Nominal constant-acceleration trajectory: a_nom = v_target^2 / (2 * L_track)
        static constexpr double NOMINAL_ACCELERATION_M_S2 =
            (TARGET_INJECTION_VELOCITY_M_S * TARGET_INJECTION_VELOCITY_M_S) / (2.0 * TRACK_LENGTH_M);

    public:
        constexpr CislunarMassDriverMPC() noexcept = default;

        [[nodiscard]] static constexpr double nominal_acceleration() noexcept {
            return NOMINAL_ACCELERATION_M_S2;
        }

        /// Check whether sled telemetry violates safety boundaries (quench or rail strike)
        [[nodiscard]] static constexpr bool is_scram_condition(
            double coil_temp_k,
            double levitation_gap_mm
        ) noexcept {
            return (coil_temp_k > CRITICAL_COIL_TEMP_K) || (levitation_gap_mm < MIN_SAFE_GAP_MM);
        }

        /// Compute theoretical reference velocity at position x along the track: v_ref(x) = sqrt(2 * a_nom * x)
        [[nodiscard]] static inline double compute_reference_velocity(double position_m) noexcept {
            const double pos_clamped = (position_m > 0.0) ? position_m : 0.0;
            return std::sqrt(2.0 * NOMINAL_ACCELERATION_M_S2 * pos_clamped);
        }

        /// Linear Synchronous Motor synchronous frequency: f_sync = v / (2 * tau_p) = v / 1.0 = v Hz
        [[nodiscard]] static constexpr double compute_synchronous_frequency(double velocity_m_s) noexcept {
            const double v = (velocity_m_s > 0.0) ? velocity_m_s : 0.0;
            return v / (2.0 * POLE_PITCH_M);
        }

        /// Closed-loop Lorentz thrust command: F = m * (a_nom + K_v * (v_ref - v))
        [[nodiscard]] static constexpr double compute_lorentz_thrust(
            double payload_mass_kg,
            double reference_velocity_m_s,
            double actual_velocity_m_s
        ) noexcept {
            const double velocity_error = reference_velocity_m_s - actual_velocity_m_s;
            const double commanded_accel = NOMINAL_ACCELERATION_M_S2 + (VELOCITY_TRACKING_GAIN * velocity_error);
            const double thrust = payload_mass_kg * commanded_accel;
            return (thrust > 0.0) ? thrust : 0.0;
        }

        /// Stator 3-phase current conversion with inverter saturation clamping: I = clamp(F * factor, 0, 150 kA)
        [[nodiscard]] static constexpr double compute_phase_current_ka(double thrust_n) noexcept {
            const double raw_current_ka = thrust_n * LORENTZ_CURRENT_COEFF;
            return std::clamp(raw_current_ka, 0.0, MAX_PHASE_CURRENT_KA);
        }

        /// Halbach magnetic array passive restoring and damping force: F_damp = k_gap * (gap_nominal - gap_actual)
        [[nodiscard]] static constexpr double compute_halbach_damping(double gap_mm) noexcept {
            return HALBACH_STIFFNESS_N_MM * (NOMINAL_LEVITATION_GAP_MM - gap_mm);
        }

        /// Compute microsecond MPC stator commutation command
        [[nodiscard]] inline StatorCoilCommand step(const SledTelemetry& t) const noexcept {
            StatorCoilCommand cmd{};
            cmd.target_velocity_m_s = TARGET_INJECTION_VELOCITY_M_S;

            // 1. Safety Interlock: Quench temperature or track contact floor violation
            if (is_scram_condition(t.coil_temp_kelvin, t.levitation_gap_mm)) {
                cmd.emergency_scram = true;
                cmd.synchronous_frequency_hz = 0.0;
                cmd.phase_current_ka = 0.0;
                cmd.lorentz_thrust_n = 0.0;
                cmd.halbach_damping_n = compute_halbach_damping(t.levitation_gap_mm);
                return cmd;
            }

            // 2. Nominal MPC Tracking
            cmd.emergency_scram = false;
            const double v_ref = compute_reference_velocity(t.position_m);
            cmd.synchronous_frequency_hz = compute_synchronous_frequency(t.velocity_m_s);
            cmd.lorentz_thrust_n = compute_lorentz_thrust(t.payload_mass_kg, v_ref, t.velocity_m_s);
            cmd.phase_current_ka = compute_phase_current_ka(cmd.lorentz_thrust_n);
            cmd.halbach_damping_n = compute_halbach_damping(t.levitation_gap_mm);

            return cmd;
        }

        /// Alias matching interface convention
        [[nodiscard]] inline StatorCoilCommand compute_command(const SledTelemetry& t) const noexcept {
            return step(t);
        }
    };

} // namespace AetherOmega::Cislunar
