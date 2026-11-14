"""
ATLAS NEXUS: Mission 04 - Simulation & Digital Twin Studio
Real-time state synchronization, drift telemetry, and numerical Runge-Kutta integration.
"""

from typing import Callable, Dict, List, Tuple


class DigitalTwin:
    def __init__(self, system_id: str, nominal_state: Dict[str, float]) -> None:
        self.system_id = system_id
        self.nominal_state = nominal_state
        self.current_state = dict(nominal_state)
        self.is_healthy = True
        self.last_drift = 0.0

    def record_telemetry(self, readings: Dict[str, float]) -> float:
        self.current_state.update(readings)
        total_drift = 0.0
        count = 0

        for key, nominal_val in self.nominal_state.items():
            if key in readings:
                denom = abs(nominal_val) if nominal_val != 0 else 1.0
                total_drift += abs(readings[key] - nominal_val) / denom
                count += 1

        drift = total_drift / count if count > 0 else 0.0
        self.last_drift = drift
        # Flag unhealthy if relative drift exceeds 20%
        self.is_healthy = drift < 0.20
        return drift


class ScenarioSimulator:
    def rk4_integrate(
        self,
        derivs: Callable[[float, List[float]], List[float]],
        initial_state: List[float],
        t_span: Tuple[float, float],
        steps: int = 20,
    ) -> List[Tuple[float, List[float]]]:
        t0, tf = t_span
        h = (tf - t0) / steps
        t = t0
        y = list(initial_state)
        history: List[Tuple[float, List[float]]] = [(t, list(y))]

        for _ in range(steps):
            k1 = derivs(t, y)
            y_k2 = [y[i] + 0.5 * h * k1[i] for i in range(len(y))]
            k2 = derivs(t + 0.5 * h, y_k2)
            y_k3 = [y[i] + 0.5 * h * k2[i] for i in range(len(y))]
            k3 = derivs(t + 0.5 * h, y_k3)
            y_k4 = [y[i] + h * k3[i] for i in range(len(y))]
            k4 = derivs(t + h, y_k4)

            for i in range(len(y)):
                y[i] += (h / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i])
            t += h
            history.append((t, list(y)))

        return history
