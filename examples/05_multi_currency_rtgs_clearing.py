#!/usr/bin/env python3
"""Example 05: Multi-Currency Atomic Settlement & Foreign Exchange Hedging.

Demonstrates real-time gross settlement (RTGS) between sovereign currencies,
Central Bank Digital Currencies (e-Rupee), and automated foreign exchange risk hedging.
"""

import sys
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from omniverse.modules.settlement import GlobalClearingHouse, CurrencyCode

def main():
    print("================================================================")
    print("  05. INSTITUTIONAL MULTI-CURRENCY ATOMIC CLEARING HOUSE (RTGS)")
    print("================================================================")

    clearing = GlobalClearingHouse()

    # 1. Inspect Treasury Reserves
    print("\n🏦 Step 1: Initial Liquidity Reserves:")
    reserves = clearing.get_liquidity_reserves()
    for curr, amt in reserves.items():
        print(f" • {curr.value:5}: {amt:15,.2f}")

    # 2. Execute USD -> INR Cross-Border Settlement
    print("\n⚡ Step 2: Settling Cross-Border Client Payment (USD -> INR)...")
    tx1 = clearing.execute_atomic_settlement(
        sender_id="CLIENT-GLOBAL-TECH-US",
        recipient_id="OMNIVERSE-HQ-INDIA",
        source_currency=CurrencyCode.USD,
        target_currency=CurrencyCode.INR,
        source_amount=25000.0  # $25,000 USD
    )
    print(f" • Settlement Hash : {tx1.settlement_hash}")
    print(f" • Gross Inbound   : {tx1.source_currency.value} {tx1.source_amount:,.2f}")
    print(f" • Gross Credited  : {tx1.target_currency.value} {tx1.target_amount:,.2f}")
    print(f" • Hedged FX Rate  : 1 USD = {tx1.hedged_fx_rate:.2f} INR")
    print(f" • RTGS Status     : {tx1.status}")

    # 3. Execute Sovereign e-Rupee (CBDC) Instant Transfer
    print("\n🇮🇳 Step 3: Settling Domestic Central Bank Digital Currency (eINR)...")
    tx2 = clearing.execute_atomic_settlement(
        sender_id="ENTERPRISE-PAYROLL-MUMBAI",
        recipient_id="SUPPLIER-BENGALURU",
        source_currency=CurrencyCode.DIGITAL_RUPEE,
        target_currency=CurrencyCode.INR,
        source_amount=500000.0  # ₹5,00,000 eINR
    )
    print(f" • Settlement Hash : {tx2.settlement_hash}")
    print(f" • Value Exchanged : {tx2.source_currency.value} {tx2.source_amount:,.2f} -> {tx2.target_currency.value} {tx2.target_amount:,.2f}")
    print(f" • Parity Rate     : {tx2.hedged_fx_rate:.2f} (1:1 CBDC Settlement)")
    print(f" • Status          : {tx2.status}")
    print("================================================================")

if __name__ == "__main__":
    main()
