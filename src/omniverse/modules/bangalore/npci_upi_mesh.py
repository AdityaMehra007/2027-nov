"""NPCI UPI 2.0 / UPI Lite Switch Mesh and Real-Time Traffic Simulator for Bengaluru.

Simulates high-density payment switching across Bengaluru tech corridors,
including VPA routing, telco fiber round-trip latency, peak-load TPS stress,
UPI Autopay mandate executions, and RBI deemed-approval reconciliation.
"""

from __future__ import annotations

import random
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class UPITransactionStatus(str, Enum):
    SUCCESS = "SUCCESS"
    DEEMED_APPROVED = "DEEMED_APPROVED"  # Auto-reconciled under RBI T+1 norms
    TECHNICAL_DECLINE = "TECHNICAL_DECLINE"  # Bank switch timeout / NPCI switch lag
    BUSINESS_DECLINE = "BUSINESS_DECLINE"  # Incorrect PIN / Insufficient Balance
    PENDING_REVERSAL = "PENDING_REVERSAL"


class UPICorridorCluster(str, Enum):
    INDIRANAGAR_100FT = "Indiranagar 100ft Road"
    KORAMANGALA_SONY = "Koramangala 80ft & Sony World"
    ORR_ECOSPACE = "Outer Ring Road (Bellandur/Ecospace)"
    WHITEFIELD_ITPL = "Whitefield ITPL Corridor"
    ELECTRONIC_CITY = "Electronic City Infosys Gate"
    CBD_COMMERCIAL_ST = "CBD & Commercial Street"
    CHICKPET_MARKET = "Chickpet Wholesale Market"


class VPARouteInfo(BaseModel):
    vpa: str
    bank_name: str
    ifsc_prefix: str
    switch_latency_ms: float
    cbs_backend: str


# Pre-mapped VPA suffixes to banking switches in Bangalore
VPA_HANDLE_DIRECTORY: Dict[str, Dict[str, Any]] = {
    "oksbi": {"bank": "State Bank of India", "ifsc": "SBIN0000813", "latency_ms": 42.0, "cbs": "TCS BaNCS"},
    "okhdfcbank": {"bank": "HDFC Bank", "ifsc": "HDFC0000001", "latency_ms": 35.0, "cbs": "Finacle / Murex"},
    "okaxis": {"bank": "Axis Bank", "ifsc": "UTIB0000001", "latency_ms": 38.0, "cbs": "Finacle 11"},
    "okicici": {"bank": "ICICI Bank", "ifsc": "ICIC0000002", "latency_ms": 32.0, "cbs": "BaNCS Core"},
    "cnrb": {"bank": "Canara Bank Bangalore HQ", "ifsc": "CNRB0000001", "latency_ms": 45.0, "cbs": "Infosys Finacle"},
    "paytm": {"bank": "Paytm Payments Bank Switch", "ifsc": "PYTM0123456", "latency_ms": 28.0, "cbs": "In-house Microservices"},
    "ybl": {"bank": "YES Bank / PhonePe Switch", "ifsc": "YESB0000001", "latency_ms": 30.0, "cbs": "Finacle Modernized"},
}


class UPISimulatedTransaction(BaseModel):
    txn_id: str = Field(default_factory=lambda: f"UPI-{uuid.uuid4().hex[:12].upper()}")
    npci_rrn: str = Field(default_factory=lambda: f"RRN{random.randint(100000000000, 999999999999)}")
    remitter_vpa: str
    beneficiary_vpa: str
    amount_inr: float
    corridor: UPICorridorCluster
    channel: str = "UPI_STANDARD"  # UPI_STANDARD or UPI_LITE (<= INR 500 offline)
    status: UPITransactionStatus
    network_latency_ms: float
    switch_response_time_ms: float
    total_time_ms: float
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    decline_reason: Optional[str] = None


class UPIMeshClusterTelemetry(BaseModel):
    corridor: UPICorridorCluster
    active_tps: int
    peak_tps_capacity: int
    utilization_pct: float
    avg_latency_ms: float
    success_rate_pct: float
    total_volume_inr_last_hour: float
    top_merchant_categories: List[str]


class BangaloreNPCIUPIMesh:
    """Enterprise high-throughput UPI switch simulation and telemetry mesh."""

    def __init__(self) -> None:
        self.transactions: List[UPISimulatedTransaction] = []

    @staticmethod
    def resolve_vpa(vpa: str) -> Optional[VPARouteInfo]:
        """Resolves VPA to its destination bank routing switch and IFSC code."""
        if "@" not in vpa:
            return None
        parts = vpa.lower().split("@")
        handle = parts[1]
        route_meta = VPA_HANDLE_DIRECTORY.get(handle)
        if not route_meta:
            # Fallback generic switch
            return VPARouteInfo(
                vpa=vpa,
                bank_name="NPCI Generic Member Bank",
                ifsc_prefix="PUNB0000001",
                switch_latency_ms=50.0,
                cbs_backend="Finacle Generic",
            )
        return VPARouteInfo(
            vpa=vpa,
            bank_name=route_meta["bank"],
            ifsc_prefix=route_meta["ifsc"],
            switch_latency_ms=route_meta["latency_ms"],
            cbs_backend=route_meta["cbs"],
        )

    def execute_payment(
        self,
        remitter_vpa: str,
        beneficiary_vpa: str,
        amount_inr: float,
        corridor: UPICorridorCluster = UPICorridorCluster.KORAMANGALA_SONY,
        force_failure_simulation: bool = False,
    ) -> UPISimulatedTransaction:
        """Executes a single end-to-end UPI payment through NPCI simulated switch."""
        rem_route = self.resolve_vpa(remitter_vpa)
        ben_route = self.resolve_vpa(beneficiary_vpa)

        # Base network fiber transit delay across Bangalore metro ring
        net_latency = round(random.uniform(12.0, 28.0), 2)
        rem_switch_ms = rem_route.switch_latency_ms if rem_route else 40.0
        ben_switch_ms = ben_route.switch_latency_ms if ben_route else 40.0
        total_time = round(net_latency + rem_switch_ms + ben_switch_ms + random.uniform(5.0, 15.0), 2)

        is_upi_lite = amount_inr <= 500.0 and random.random() < 0.35
        channel = "UPI_LITE" if is_upi_lite else "UPI_STANDARD"

        decline_reason = None
        if force_failure_simulation:
            status = UPITransactionStatus.TECHNICAL_DECLINE
            decline_reason = "NPCI_SWITCH_TIMEOUT_HTTP_504"
        elif total_time > 180.0:
            status = UPITransactionStatus.DEEMED_APPROVED
            decline_reason = "LATENCY_THRESHOLD_EXCEEDED_AUTO_RECONCILE_T1"
        elif random.random() < 0.02:  # 2% standard drop rate in urban peak traffic
            status = UPITransactionStatus.TECHNICAL_DECLINE
            decline_reason = "ISSUER_BANK_CBS_CONNECTION_RESET"
        else:
            status = UPITransactionStatus.SUCCESS

        txn = UPISimulatedTransaction(
            remitter_vpa=remitter_vpa,
            beneficiary_vpa=beneficiary_vpa,
            amount_inr=amount_inr,
            corridor=corridor,
            channel=channel,
            status=status,
            network_latency_ms=net_latency,
            switch_response_time_ms=round(rem_switch_ms + ben_switch_ms, 2),
            total_time_ms=total_time,
            decline_reason=decline_reason,
        )
        self.transactions.append(txn)
        return txn

    def simulate_traffic_burst(
        self,
        transaction_count: int = 100,
        corridor: Optional[UPICorridorCluster] = None,
    ) -> Dict[str, Any]:
        """Simulates a rapid burst of UPI payments across Bengaluru corridors."""
        corridors = [corridor] if corridor else list(UPICorridorCluster)
        vpa_remitters = ["techie.blr@oksbi", "rahul.startup@okhdfcbank", "priya.gcc@okaxis", "kiran.ecity@cnrb"]
        vpa_merchants = ["swiggy.blr@okicici", "starbucks.indiranagar@okhdfcbank", "thirdwave.koramangala@ybl", "metro.bmrc@paytm"]

        results: List[UPISimulatedTransaction] = []
        for _ in range(transaction_count):
            rem = random.choice(vpa_remitters)
            ben = random.choice(vpa_merchants)
            amt = round(random.uniform(40.0, 4500.0), 2)
            c = random.choice(corridors)
            txn = self.execute_payment(rem, ben, amt, c)
            results.append(txn)

        success_count = sum(1 for t in results if t.status == UPITransactionStatus.SUCCESS)
        total_vol = sum(t.amount_inr for t in results)
        avg_latency = sum(t.total_time_ms for t in results) / len(results) if results else 0.0

        return {
            "burst_size": transaction_count,
            "success_rate_pct": round((success_count / transaction_count) * 100, 2),
            "total_volume_inr": round(total_vol, 2),
            "average_latency_ms": round(avg_latency, 2),
            "sample_transactions": [t.model_dump() for t in results[:10]],
        }

    def get_mesh_telemetry(self) -> List[UPIMeshClusterTelemetry]:
        """Provides real-time health telemetry across all major Bengaluru UPI clusters."""
        telemetry: List[UPIMeshClusterTelemetry] = []
        cluster_configs = [
            (UPICorridorCluster.INDIRANAGAR_100FT, 850, 1500, 68.2, 98.4, 4200000.0, ["Fine Dining", "Apparel", "Pubs & Breweries"]),
            (UPICorridorCluster.KORAMANGALA_SONY, 1420, 2200, 78.5, 99.1, 8900000.0, ["Quick Commerce", "Food Tech", "Coworking"]),
            (UPICorridorCluster.ORR_ECOSPACE, 1890, 2800, 84.1, 98.8, 14500000.0, ["Corporate Food Courts", "Cab Aggregators", "Corporate Retail"]),
            (UPICorridorCluster.WHITEFIELD_ITPL, 1120, 1800, 72.0, 97.9, 7300000.0, ["Metro Transit", "Tech Park Retail", "Supermarkets"]),
            (UPICorridorCluster.ELECTRONIC_CITY, 960, 1600, 69.5, 98.2, 5800000.0, ["Campus Canteens", "Hostel Living", "SMBs"]),
            (UPICorridorCluster.CBD_COMMERCIAL_ST, 1310, 2000, 76.8, 97.5, 9100000.0, ["Traditional Jewelry", "Apparel", "Electronics"]),
            (UPICorridorCluster.CHICKPET_MARKET, 740, 1200, 64.0, 96.8, 6200000.0, ["Textile Wholesale", "Hardware", "Cashless Mandis"]),
        ]

        for c, tps, cap, lat, s_rate, vol, cats in cluster_configs:
            util = round((tps / cap) * 100.0, 1)
            telemetry.append(
                UPIMeshClusterTelemetry(
                    corridor=c,
                    active_tps=tps,
                    peak_tps_capacity=cap,
                    utilization_pct=util,
                    avg_latency_ms=lat,
                    success_rate_pct=s_rate,
                    total_volume_inr_last_hour=vol,
                    top_merchant_categories=cats,
                )
            )
        return telemetry
