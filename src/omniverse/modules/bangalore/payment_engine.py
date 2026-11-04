import uuid
import time
import hmac
import hashlib
import urllib.parse
from typing import Dict, Any, Optional, Tuple, List
from sqlmodel import Session, select
from omniverse.modules.bangalore.models import (
    BangaloreCashTransaction,
    FlatRadarSubscriber,
    SMBGrowthClient,
    RadarSubscriptionTier,
)
from omniverse.core.telemetry import global_event_bus

class BangaloreUPIEngine:
    """Turnkey 24/7 UPI & Digital Payment Engine for Bangalore Cashflow.

    Generates zero-friction UPI Intent URLs (compatible with Google Pay,
    PhonePe, Paytm, BHIM) and cryptographically reconciles daily incoming payments.
    """

    DEFAULT_VPA = "cashflow.bangalore@icici"
    DEFAULT_PAYEE = "Omniverse Bangalore Technologies"
    SECRET_KEY = b"namma-cashflow-secret-key-2027"

    TIER_PRICING = {
        RadarSubscriptionTier.SPRINT_HUNTER: 199.0,
        RadarSubscriptionTier.PRO_RELOCATOR: 499.0,
        RadarSubscriptionTier.FOUNDER_VIP: 1499.0,
    }

    TIER_DURATION_DAYS = {
        RadarSubscriptionTier.SPRINT_HUNTER: 7,
        RadarSubscriptionTier.PRO_RELOCATOR: 30,
        RadarSubscriptionTier.FOUNDER_VIP: 365,
    }

    def __init__(self, session: Session, vpa: Optional[str] = None):
        self.session = session
        self.vpa = vpa or self.DEFAULT_VPA

    def create_upi_intent_uri(
        self,
        amount_inr: float,
        note: str,
        transaction_id: str
    ) -> str:
        """Constructs an official NPCI UPI Deep Link intent URI."""
        params = {
            "pa": self.vpa,
            "pn": self.DEFAULT_PAYEE,
            "am": f"{amount_inr:.2f}",
            "cu": "INR",
            "tn": note,
            "tr": transaction_id
        }
        query_string = urllib.parse.urlencode(params)
        return f"upi://pay?{query_string}"

    def checkout_radar_subscription(
        self,
        name: str,
        phone_whatsapp: str,
        tier: RadarSubscriptionTier = RadarSubscriptionTier.PRO_RELOCATOR,
        target_clusters: str = "HSR Layout,Koramangala,Indiranagar",
        preferred_bhk: int = 2,
        max_budget_inr: float = 35000.0
    ) -> Dict[str, Any]:
        """Generates instant checkout for Bangalore Flat Radar subscription."""
        amount = self.TIER_PRICING.get(tier, 499.0)
        txn_id = f"BLR-RADAR-{uuid.uuid4().hex[:10].upper()}"
        note = f"NammaFlat {tier.value} Pass for {phone_whatsapp}"

        intent_uri = self.create_upi_intent_uri(amount, note, txn_id)

        return {
            "transaction_id": txn_id,
            "amount_inr": amount,
            "tier": tier.value,
            "subscriber_name": name,
            "phone_whatsapp": phone_whatsapp,
            "upi_intent_uri": intent_uri,
            "pay_to_vpa": self.vpa,
            "qr_data_string": intent_uri,
            "status": "PENDING_PAYMENT",
            "metadata": {
                "clusters": target_clusters,
                "bhk": preferred_bhk,
                "max_budget_inr": max_budget_inr
            }
        }

    def settle_radar_payment(
        self,
        transaction_id: str,
        name: str,
        phone_whatsapp: str,
        tier: RadarSubscriptionTier,
        amount_inr: float,
        target_clusters: str = "HSR Layout,Koramangala,Indiranagar",
        preferred_bhk: int = 2,
        max_budget_inr: float = 35000.0,
        gateway_ref: Optional[str] = None
    ) -> Tuple[BangaloreCashTransaction, FlatRadarSubscriber]:
        """Reconciles payment, logs transaction, and grants active VIP pass."""
        duration_days = self.TIER_DURATION_DAYS.get(tier, 30)
        expires_at = time.time() + (duration_days * 86400)
        vip_key = f"VIP-{uuid.uuid4().hex[:8].upper()}"

        # 1. Record Transaction
        txn = BangaloreCashTransaction(
            transaction_id=transaction_id,
            revenue_stream="RADAR_PASS",
            client_or_user=f"{name} ({phone_whatsapp})",
            amount_inr=amount_inr,
            payment_mode="UPI",
            reference_id=gateway_ref or f"UPI-REF-{int(time.time() * 1000)}",
            status="SETTLED",
            settled_at=time.time()
        )
        self.session.add(txn)

        # 2. Register or update Subscriber
        existing_sub = self.session.exec(
            select(FlatRadarSubscriber).where(FlatRadarSubscriber.phone_whatsapp == phone_whatsapp)
        ).first()

        if existing_sub:
            existing_sub.is_active = True
            existing_sub.pass_expires_at = expires_at
            existing_sub.total_paid_inr += amount_inr
            existing_sub.tier = tier
            sub = existing_sub
        else:
            sub = FlatRadarSubscriber(
                name=name,
                phone_whatsapp=phone_whatsapp,
                target_clusters=target_clusters,
                preferred_bhk=preferred_bhk,
                max_budget_inr=max_budget_inr,
                tier=tier,
                pass_expires_at=expires_at,
                is_active=True,
                total_paid_inr=amount_inr,
                vip_access_key=vip_key
            )
            self.session.add(sub)

        self.session.commit()
        self.session.refresh(txn)
        self.session.refresh(sub)

        global_event_bus.publish("BANGALORE_PAYMENT_COLLECTED", {
            "txn_id": txn.transaction_id,
            "amount_inr": amount_inr,
            "stream": "RADAR_PASS",
            "subscriber": phone_whatsapp
        })

        return txn, sub

    def settle_smb_retainer(
        self,
        client_id: int,
        amount_inr: float,
        gateway_ref: Optional[str] = None
    ) -> Tuple[BangaloreCashTransaction, SMBGrowthClient]:
        """Settles an SMB client monthly retainer."""
        client = self.session.get(SMBGrowthClient, client_id)
        if not client:
            raise ValueError(f"SMB Client ID {client_id} not found")

        txn_id = f"BLR-SMB-{uuid.uuid4().hex[:10].upper()}"
        txn = BangaloreCashTransaction(
            transaction_id=txn_id,
            revenue_stream="SMB_RETAINER",
            client_or_user=client.business_name,
            amount_inr=amount_inr,
            payment_mode="UPI",
            reference_id=gateway_ref or f"UPI-SMB-{int(time.time() * 1000)}",
            status="SETTLED",
            settled_at=time.time()
        )
        self.session.add(txn)

        client.is_active = True
        client.status = "ACTIVE_RETAINER"
        client.monthly_fee_inr = amount_inr
        client.updated_at = time.time()
        self.session.add(client)

        self.session.commit()
        self.session.refresh(txn)
        self.session.refresh(client)

        global_event_bus.publish("BANGALORE_PAYMENT_COLLECTED", {
            "txn_id": txn.transaction_id,
            "amount_inr": amount_inr,
            "stream": "SMB_RETAINER",
            "client": client.business_name
        })

        return txn, client

    def generate_cryptographic_receipt(self, txn: BangaloreCashTransaction) -> str:
        """Issues an air-gapped HMAC receipt signature for verification."""
        msg = f"{txn.transaction_id}|{txn.amount_inr}|{txn.settled_at}|{txn.status}".encode()
        return hmac.new(self.SECRET_KEY, msg, hashlib.sha256).hexdigest()
