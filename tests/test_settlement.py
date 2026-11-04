import pytest
from omniverse.modules.settlement.clearing import GlobalClearingHouse, CurrencyCode, SettlementTransaction

def test_multi_currency_atomic_settlement():
    clearing = GlobalClearingHouse()
    tx = clearing.execute_atomic_settlement(
        sender_id="CLIENT-IN-001",
        recipient_id="OMNIVERSE-TREASURY",
        source_currency=CurrencyCode.USD,
        target_currency=CurrencyCode.INR,
        source_amount=10000.0
    )
    
    assert isinstance(tx, SettlementTransaction)
    assert tx.status == "SETTLED"
    assert tx.settlement_hash.startswith("0x")
    assert tx.target_amount > 800000.0 # 10,000 USD is > 800,000 INR
    assert tx.hedged_fx_rate > 80.0

def test_clearing_house_liquidity_reserve():
    clearing = GlobalClearingHouse()
    reserves = clearing.get_liquidity_reserves()
    assert CurrencyCode.INR in reserves
    assert CurrencyCode.USD in reserves
    assert CurrencyCode.EUR in reserves
    assert reserves[CurrencyCode.INR] > 1000000.0
