"""
BENGALURU CASH-IN-TRANSIT (CIT) & CURRENCY CHEST FLEET LOGISTICS ENGINE
Cashflow Infinity: Omniverse Platform

Simulates armored vehicle fleet dispatch, currency chest balancing,
and traffic choke-point avoidance across Bengaluru (Silk Board, Marathahalli, Tin Factory, Hebbal).
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum
import time

class BangaloreTrafficChokePoint(str, Enum):
    SILK_BOARD_JUNCTION = "SILK_BOARD_JUNCTION"
    MARATHAHALLI_BRIDGE = "MARATHAHALLI_BRIDGE"
    TIN_FACTORY_KR_PURAM = "TIN_FACTORY_KR_PURAM"
    HEBBAL_FLYOVER = "HEBBAL_FLYOVER"
    GORAGUNTEPALYA_JUNCTION = "GORAGUNTEPALYA_JUNCTION"
    KADOOBEESANAHALLI_ORR = "KADOOBEESANAHALLI_ORR"

class SecurityEscortTier(str, Enum):
    HIGH_THREAT_ARMORED = "HIGH_THREAT_ARMORED"        # 2 Armed guards, GPS geofencing, remote immobilizer
    STANDARD_COMMERCIAL = "STANDARD_COMMERCIAL"        # 1 Armed guard, twin-custody lockboxes

class CurrencyChestHub(BaseModel):
    chest_id: str
    bank_name: str
    location: str
    holding_capacity_inr_cr: float
    current_cash_inr_cr: float
    armed_guard_complement: int
    rbi_approval_ref: str

class ArmoredDispatchRoute(BaseModel):
    route_id: str
    van_id: str
    origin_chest: str
    destinations: List[str]
    cash_payload_inr_cr: float
    escort_tier: SecurityEscortTier
    departure_time_window: str
    estimated_transit_minutes: int
    chokepoints_mitigated: List[BangaloreTrafficChokePoint]
    risk_index: float  # 0.0 (Safe) to 1.0 (High Risk)
    geofence_status: str

class BangaloreCITLogisticsEngine:
    """Manages cash-in-transit fleet logistics and currency chests in Bengaluru."""

    def __init__(self):
        self.chests = [
            CurrencyChestHub(
                chest_id="CHEST-BLR-01",
                bank_name="Canara Bank Global Head Office",
                location="J.C. Road, Town Hall Circle, Bengaluru 560002",
                holding_capacity_inr_cr=500.0,
                current_cash_inr_cr=342.5,
                armed_guard_complement=14,
                rbi_approval_ref="RBI/BLR/CC/2024/098"
            ),
            CurrencyChestHub(
                chest_id="CHEST-BLR-02",
                bank_name="State Bank of India (Local Head Office)",
                location="St. Mark's Road, Shanthala Nagar, Bengaluru 560001",
                holding_capacity_inr_cr=750.0,
                current_cash_inr_cr=520.0,
                armed_guard_complement=18,
                rbi_approval_ref="RBI/BLR/CC/2023/142"
            ),
            CurrencyChestHub(
                chest_id="CHEST-BLR-03",
                bank_name="HDFC Bank Regional Currency Chest",
                location="Peenya Industrial Area Phase 1, Bengaluru 560058",
                holding_capacity_inr_cr=400.0,
                current_cash_inr_cr=265.0,
                armed_guard_complement=12,
                rbi_approval_ref="RBI/BLR/CC/2024/215"
            ),
        ]

    def get_chests(self) -> List[CurrencyChestHub]:
        return self.chests

    def plan_armored_dispatch(
        self,
        origin_chest_id: str = "CHEST-BLR-01",
        target_branches: Optional[List[str]] = None,
        cash_needed_inr_cr: float = 24.50,
        departure_hour: int = 6  # 6 AM off-peak window recommended
    ) -> ArmoredDispatchRoute:
        """
        Plans secure cash transit while avoiding peak Bengaluru traffic windows
        (9 AM - 11 AM and 5 PM - 8 PM) and notorious choke points.
        """
        if not target_branches:
            target_branches = [
                "Indiranagar 100ft Road Wealth Branch",
                "Bellandur EcoWorld Digital Branch",
                "Whitefield ITPL Branch"
            ]

        # Calculate traffic delay penalty
        is_peak = (9 <= departure_hour <= 11) or (17 <= departure_hour <= 20)
        transit_multiplier = 2.4 if is_peak else 1.0

        base_minutes = 45 + (len(target_branches) * 20)
        transit_time = int(base_minutes * transit_multiplier)

        # Choke points encountered/mitigated
        mitigated = [
            BangaloreTrafficChokePoint.SILK_BOARD_JUNCTION,
            BangaloreTrafficChokePoint.MARATHAHALLI_BRIDGE,
            BangaloreTrafficChokePoint.TIN_FACTORY_KR_PURAM
        ]

        # Risk scoring
        risk = 0.15 if not is_peak else 0.45
        if cash_needed_inr_cr > 20.0:
            escort_tier = SecurityEscortTier.HIGH_THREAT_ARMORED
        else:
            escort_tier = SecurityEscortTier.STANDARD_COMMERCIAL

        return ArmoredDispatchRoute(
            route_id=f"CIT-BLR-{int(time.time())}",
            van_id="KA-01-AG-8899 (Tata 407 Armored Heavy)",
            origin_chest=origin_chest_id,
            destinations=target_branches,
            cash_payload_inr_cr=cash_needed_inr_cr,
            escort_tier=escort_tier,
            departure_time_window=f"{departure_hour:02d}:00 HRS IST ({'OFF-PEAK' if not is_peak else 'PEAK CONGESTION'})",
            estimated_transit_minutes=transit_time,
            chokepoints_mitigated=mitigated,
            risk_index=round(risk, 2),
            geofence_status="ACTIVE_SECURE_GEOFENCE"
        )
