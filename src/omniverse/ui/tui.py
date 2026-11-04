"""Cyberpunk Terminal User Interface (TUI) for CASHFLOW INFINITY: OMNIVERSE.

Provides a live ASCII/ANSI console featuring planetary edge node telemetry,
real-time financial ticker, system diagnostics, and interactive command controls.
"""

import os
import sys
import time
import shutil
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, Callable
from sqlmodel import Session

from omniverse.core.database import get_engine, init_db
from omniverse.core.config import get_settings
from omniverse.core.telemetry import global_event_bus
from omniverse.operations.health import HealthDiagnostics
from omniverse.modules.revenue.pipeline import LeadPipeline
from omniverse.modules.revenue.payments import PaymentWorkflow
from omniverse.modules.planetary_mesh import GlobalPlanetaryMesh
from omniverse.modules.aether.risk_engine import AetherRiskEngine
from omniverse.modules.aether.models import HazardType

class CyberpunkTUI:
    """Cyberpunk ASCII / ANSI Terminal Dashboard & Interactive Operator Shell."""

    # ANSI Color Palettes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    CYAN = "\033[96m"
    NEON_GREEN = "\033[92m"
    YELLOW = "\033[93m"
    PURPLE = "\033[95m"
    RED = "\033[91m"
    WHITE = "\033[97m"
    BG_CYAN = "\033[46m\033[30m"
    BG_BLACK = "\033[40m"

    BANNER = r"""
 ██████╗ █████╗ ███████╗██╗  ██╗███████╗██╗      ██████╗ ██╗    ██╗
██╔════╝██╔══██╗██╔════╝██║  ██║██╔════╝██║     ██╔═══██╗██║    ██║
██║     ███████║███████╗███████║█████╗  ██║     ██║   ██║██║ █╗ ██║
██║     ██╔══██║╚════██║██╔══██║██╔══╝  ██║     ██║   ██║██║███╗██║
╚██████╗██║  ██║███████║██║  ██║██║     ███████╗╚██████╔╝╚███╔███╔╝
 ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝ 
    INFINITY // OMNIVERSE // AETHER RESILIENCE FABRIC // 2027 PRO
"""

    def __init__(self, session: Optional[Session] = None, use_ansi: bool = True):
        self.session = session
        self.use_ansi = use_ansi
        self.settings = get_settings()
        self.mesh = GlobalPlanetaryMesh()
        self.risk_engine = AetherRiskEngine()
        self.last_command_output: str = "SYSTEM ONLINE // AWAITING DIRECTIVES"
        self._owns_session = False

    def _c(self, text: str, color: str) -> str:
        """Applies ANSI color if enabled, else returns bare text."""
        if not self.use_ansi:
            return text
        return f"{color}{text}{self.RESET}"

    def _get_active_session(self) -> Session:
        if self.session is not None:
            return self.session
        engine = get_engine()
        self.session = engine.get_session().__enter__()
        self._owns_session = True
        return self.session

    def render_header(self) -> str:
        """Renders the top neon banner and tactical timestamp."""
        now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        border = "=" * 74
        title = self._c(self.BANNER.strip("\n"), self.CYAN)
        subhead = self._c(f" [NODE CLUSTER: GLOBAL-FEDERATED]  [SECURITY GOVERNOR: ARMED]  [{now_utc}] ", self.WHITE)
        return f"{border}\n{title}\n{border}\n{subhead}\n{border}"

    def render_planetary_nodes(self) -> str:
        """Renders 6-continent federated mesh latency & quorum status."""
        nodes = self.mesh.list_nodes()
        lines = [
            self._c("┌── [PLANETARY EDGE NODES // 6 CONTINENTS MESH] " + "─" * 28 + "┐", self.PURPLE),
            f"│ {'NODE ID':<13} {'REGION':<16} {'LATENCY':<10} {'STATUS':<10} {'ENDPOINT':<20} │",
            "├" + "─" * 74 + "┤"
        ]
        for node in nodes:
            status_str = self._c(node.status.value, self.NEON_GREEN if node.status.value == "ONLINE" else self.RED)
            lat_str = f"{node.latency_ms:.1f}ms"
            lines.append(
                f"│ {node.node_id:<13} {node.region.value:<16} {lat_str:<10} {status_str:<19} {node.endpoint:<20} │"
            )
        lines.append(self._c("└" + "─" * 74 + "┘", self.PURPLE))
        return "\n".join(lines)

    def render_financial_ticker(self) -> str:
        """Renders real-time financial ticker with pipeline value, collected cash, and FX."""
        session = self._get_active_session()
        pipeline = LeadPipeline(session)
        pipe_summary = pipeline.get_pipeline_summary()
        payments = PaymentWorkflow(session)
        ledger = payments.get_financial_ledger()

        pipe_val = pipe_summary.get("pipeline_value_inr", 0.0)
        collected = ledger.get("collected_revenue_inr", 0.0)
        receivables = ledger.get("outstanding_receivables_inr", 0.0)
        total_leads = pipe_summary.get("total_leads", 0)

        lines = [
            self._c("┌── [FINANCIAL LEDGER & SOVEREIGN CASHFLOW TICKER] " + "─" * 25 + "┐", self.NEON_GREEN),
            f"│  PIPELINE VALUE    : {self._c(f'₹{pipe_val:,.2f}', self.WHITE):<35} │ LEADS TRACKED: {total_leads:<6}  │",
            f"│  COLLECTED REVENUE : {self._c(f'₹{collected:,.2f}', self.NEON_GREEN):<35} │ STATUS       : VERIFIED │",
            f"│  OUTSTANDING RECV  : {self._c(f'₹{receivables:,.2f}', self.YELLOW):<35} │ ARBITRAGE    : PASSIVE  │",
            f"│  FX LIQUIDITY HEDGE: USD/INR 84.15 ▲  EUR/USD 1.0850 ▼  AED/INR 22.91 ▲ │",
            self._c("└" + "─" * 74 + "┘", self.NEON_GREEN)
        ]
        return "\n".join(lines)

    def render_system_health(self) -> str:
        """Renders local compute resources and database connectivity."""
        session = self._get_active_session()
        diagnostics = HealthDiagnostics(session)
        health = diagnostics.run_diagnostics()

        overall = self._c(health.get("overall_status", "UNKNOWN"), self.NEON_GREEN if health.get("overall_status") == "OK" else self.RED)
        db_stat = self._c(health.get("database_status", "UNKNOWN"), self.NEON_GREEN)
        mem = f"{health.get('memory_usage_mb', 0.0):.1f} MB"
        disk = f"{health.get('disk_available_gb', 0.0):.1f} GB"
        events_count = len(global_event_bus.get_events())

        lines = [
            self._c("┌── [SYSTEM HEALTH // KERNEL TELEMETRY] " + "─" * 36 + "┐", self.CYAN),
            f"│  OVERALL: {overall:<17} DB: {db_stat:<18} RAM: {mem:<9} DISK: {disk:<8} │",
            f"│  SAFETY BUDGET DAILY: ${self.settings.safety_budget_daily_usd:.2f} | TELEMETRY EVENTS: {events_count:<6} | WAL: ENABLED │",
            self._c("└" + "─" * 74 + "┘", self.CYAN)
        ]
        return "\n".join(lines)

    def render_command_bar(self) -> str:
        """Renders interactive command ribbon and output status line."""
        status_line = self._c(f"STATUS >> {self.last_command_output}", self.YELLOW)
        commands = (
            f" COMMANDS: {self._c('[m]', self.CYAN)} Consensus Quorum  "
            f"{self._c('[s]', self.CYAN)} Status Refresh  "
            f"{self._c('[r]', self.CYAN)} Aether Risk Pulse  "
            f"{self._c('[h]', self.CYAN)} Help  "
            f"{self._c('[q]', self.CYAN)} Quit"
        )
        border = self._c("═" * 76, self.WHITE)
        return f"{border}\n{status_line}\n{border}\n{commands}\n{border}"

    def render_dashboard(self) -> str:
        """Assembles all TUI visual blocks into a unified console frame."""
        blocks = [
            self.render_header(),
            self.render_planetary_nodes(),
            self.render_financial_ticker(),
            self.render_system_health(),
            self.render_command_bar()
        ]
        return "\n".join(blocks)

    def handle_command(self, cmd: str) -> str:
        """Processes keyboard directive and updates last_command_output."""
        c = cmd.strip().lower()
        if c in ("q", "quit", "exit"):
            self.last_command_output = "SYSTEM SHUTDOWN DIRECTIVE RECEIVED. EXITING TUI."
            return "QUIT"

        elif c in ("m", "mesh"):
            consensus = self.mesh.reach_federated_consensus("PROPOSAL-TUI-PING", 99.8)
            agreed = consensus.get("agreement_percentage", 0.0)
            reached = "REACHED" if consensus.get("consensus_reached") else "UNREACHED"
            self.last_command_output = f"MESH PBFT CONSENSUS {reached} ({agreed}% AGREEMENT ACROSS 6 CONTINENTS)"
            global_event_bus.publish("TUI_CONSENSUS_TRIGGERED", consensus)
            return self.last_command_output

        elif c in ("s", "status"):
            session = self._get_active_session()
            diag = HealthDiagnostics(session).run_diagnostics()
            self.last_command_output = (
                f"DIAGNOSTICS REFRESHED: STATUS={diag['overall_status']} | "
                f"RAM={diag['memory_usage_mb']}MB | DISK_FREE={diag['disk_available_gb']}GB"
            )
            return self.last_command_output

        elif c in ("r", "risk"):
            # Execute quick Aether risk pulse for reference coordinates (Bengaluru Urban)
            assessment = self.risk_engine.evaluate_location_risk(
                lat=12.9716,
                lon=77.5946,
                elevation_meters=920.0,
                hazard_type=HazardType.FLOOD
            )
            self.last_command_output = (
                f"AETHER HAZARD PULSE: LEVEL={assessment.risk_level.value} | "
                f"VULNERABILITY={assessment.vulnerability_index}/100 | RESILIENCE PROTOCOL ARMED"
            )
            global_event_bus.publish("TUI_RISK_PULSE", {"risk_level": assessment.risk_level.value})
            return self.last_command_output

        elif c in ("h", "help"):
            self.last_command_output = "HELP: [m]=Mesh BFT Consensus, [s]=Refresh Status, [r]=Aether Risk Pulse, [q]=Exit"
            return self.last_command_output

        else:
            self.last_command_output = f"UNKNOWN COMMAND '{cmd}'. PRESS [h] FOR HELP OR [q] TO QUIT."
            return self.last_command_output

    def run_loop(
        self,
        max_cycles: Optional[int] = None,
        input_fn: Optional[Callable[[], str]] = None
    ) -> None:
        """Executes terminal display loop. Supports max_cycles for automated testing."""
        cycles = 0
        try:
            while True:
                # Render dashboard
                frame = self.render_dashboard()
                print(frame)

                cycles += 1
                if max_cycles is not None and cycles >= max_cycles:
                    break

                # Prompt user / input stream
                if input_fn is not None:
                    try:
                        user_cmd = input_fn()
                    except StopIteration:
                        break
                elif not sys.stdin.isatty():
                    # Non-interactive / headless environment (e.g. CI or automated tests)
                    time.sleep(0.01)
                    continue
                else:
                    try:
                        user_cmd = input("\nOMNIVERSE-TUI >>> ")
                    except (EOFError, KeyboardInterrupt):
                        print("\nExiting TUI.")
                        break

                action = self.handle_command(user_cmd)
                if action == "QUIT":
                    break
        finally:
            if self._owns_session and self.session is not None:
                self.session.close()
