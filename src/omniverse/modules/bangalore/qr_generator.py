import urllib.parse
from typing import Dict, Any

class BangaloreUPIQRGenerator:
    """Generates instant QR code assets, HTML widgets, and terminal ASCII layouts

    for NPCI UPI payment requests (Google Pay, PhonePe, Paytm, BHIM).
    """

    @staticmethod
    def get_qr_image_url(upi_intent_uri: str, size: int = 250) -> str:
        """Returns a high-resolution QR Code image URL for web and app checkout."""
        encoded_data = urllib.parse.quote(upi_intent_uri)
        return f"https://api.qrserver.com/v1/create-qr-code/?size={size}x{size}&margin=10&data={encoded_data}"

    @staticmethod
    def get_ascii_terminal_card(
        upi_intent_uri: str,
        amount_inr: float,
        vpa: str,
        order_id: str,
        note: str
    ) -> str:
        """Renders a clean terminal payment box for CLI checkout."""
        qr_url = BangaloreUPIQRGenerator.get_qr_image_url(upi_intent_uri, size=200)
        card = (
            "┌────────────────────────────────────────────────────────────┐\n"
            "│           🇮🇳 NPCI UPI INSTANT PAYMENT GATEWAY              │\n"
            "├────────────────────────────────────────────────────────────┤\n"
            f"│  Amount Due   : ₹{amount_inr:,.2f} INR                         \n"
            f"│  Payee VPA    : {vpa}               \n"
            f"│  Order Ref    : {order_id}                     \n"
            f"│  Description  : {note[:40]}... \n"
            "├────────────────────────────────────────────────────────────┤\n"
            "│  📱 Supported Apps: Google Pay • PhonePe • Paytm • BHIM    │\n"
            "│  🔗 Scan / Open QR Code URL in Browser:                    │\n"
            f"│     {qr_url}\n"
            "│  ⚡ 1-Click Mobile Intent:                                 │\n"
            f"│     {upi_intent_uri[:55]}...\n"
            "└────────────────────────────────────────────────────────────┘"
        )
        return card

    @staticmethod
    def get_embeddable_html_widget(
        upi_intent_uri: str,
        amount_inr: float,
        vpa: str,
        order_id: str,
        subscriber_name: str
    ) -> str:
        """Renders an embeddable, responsive HTML card with a live scannable QR code."""
        qr_url = BangaloreUPIQRGenerator.get_qr_image_url(upi_intent_uri, size=220)
        return f"""
        <div style="background: #0f172a; border: 1px solid #38bdf8; border-radius: 12px; padding: 20px; max-width: 380px; text-align: center; color: #f8fafc; font-family: sans-serif;">
            <div style="font-size: 11px; font-weight: 800; color: #38bdf8; letter-spacing: 1px; text-transform: uppercase;">Instant UPI Payment</div>
            <div style="font-size: 28px; font-weight: 900; margin: 8px 0; color: #10b981;">₹{amount_inr:,.2f}</div>
            <div style="font-size: 12px; color: #94a3b8; margin-bottom: 16px;">Subscriber: <strong>{subscriber_name}</strong> • Ref: {order_id}</div>
            
            <div style="background: #ffffff; padding: 12px; border-radius: 8px; display: inline-block; box-shadow: 0 4px 12px rgba(0,0,0,0.4);">
                <img src="{qr_url}" alt="UPI Payment QR Code" width="200" height="200" style="display: block;" />
            </div>
            
            <div style="margin-top: 14px; font-size: 12px; color: #cbd5e1;">
                Scan with <strong>Google Pay</strong>, <strong>PhonePe</strong>, or <strong>Paytm</strong>
            </div>
            
            <div style="margin-top: 12px;">
                <a href="{upi_intent_uri}" style="display: block; background: #2563eb; color: #ffffff; text-decoration: none; padding: 10px; border-radius: 6px; font-weight: 700; font-size: 13px;">
                    📱 Tap to Pay on Mobile
                </a>
            </div>
            <div style="margin-top: 8px; font-size: 10px; color: #64748b;">VPA: {vpa}</div>
        </div>
        """
