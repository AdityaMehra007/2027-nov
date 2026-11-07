import pytest
from omniverse.modules.agency.upi_gateway import InstantUPIEngine, UPIPaymentIntent
from omniverse.modules.agency.crypto_gateway import Web3CryptoEscrow, CryptoDepositIntent, CryptoChain


def test_instant_upi_engine_intent_generation():
    engine = InstantUPIEngine(vpa="agency@icici", payee_name="Omniverse Agency")
    intent = engine.generate_upi_intent(order_id="ord_upi_101", amount_usd=100.0, exchange_rate=86.0)

    assert isinstance(intent, UPIPaymentIntent)
    assert intent.order_id == "ord_upi_101"
    assert intent.vpa == "agency@icici"
    assert intent.amount_inr == 8600.0
    assert intent.currency == "INR"
    assert intent.intent_url.startswith("upi://pay?")
    assert "agency" in intent.intent_url
    assert "8600.00" in intent.intent_url
    assert intent.qr_svg or intent.qr_payload


def test_instant_upi_engine_payment_confirmation():
    engine = InstantUPIEngine(vpa="agency@icici", payee_name="Omniverse Agency")
    intent = engine.generate_upi_intent(order_id="ord_upi_102", amount_usd=50.0)

    # First settlement
    result = engine.confirm_upi_payment(order_id="ord_upi_102", utr_number="UTR123456789012")
    assert result["settled"] is True
    assert result["status"] == "SETTLED"
    assert result["utr"] == "UTR123456789012"

    # Replay protection: same UTR cannot be re-used
    replay = engine.confirm_upi_payment(order_id="ord_upi_other", utr_number="UTR123456789012")
    assert replay["settled"] is False
    assert "already redeemed" in replay["error"].lower()


def test_web3_crypto_escrow_deposit_intent():
    escrow = Web3CryptoEscrow()

    # Solana intent
    sol_intent = escrow.create_deposit_intent(order_id="ord_sol_1", amount_usd=1200.0, chain=CryptoChain.SOLANA)
    assert isinstance(sol_intent, CryptoDepositIntent)
    assert sol_intent.chain == CryptoChain.SOLANA
    assert sol_intent.expected_amount_usdc == 1200.0
    assert len(sol_intent.deposit_address) >= 32

    # Base intent
    base_intent = escrow.create_deposit_intent(order_id="ord_base_1", amount_usd=2500.0, chain=CryptoChain.BASE)
    assert base_intent.chain == CryptoChain.BASE
    assert base_intent.deposit_address.startswith("0x")
    assert len(base_intent.deposit_address) == 42


def test_web3_crypto_escrow_verification_and_replay_protection():
    escrow = Web3CryptoEscrow()
    order_id = "ord_crypto_verify_1"
    escrow.create_deposit_intent(order_id=order_id, amount_usd=1500.0, chain=CryptoChain.BASE)

    # Invalid transaction hash
    invalid_res = escrow.verify_transaction(order_id=order_id, tx_hash="not_a_valid_hash")
    assert invalid_res["verified"] is False

    # Valid Base tx hash (0x + 64 hex characters)
    valid_tx = "0x" + "a" * 64
    valid_res = escrow.verify_transaction(order_id=order_id, tx_hash=valid_tx)
    assert valid_res["verified"] is True
    assert valid_res["settled_usd"] == 1500.0

    # Replay attack prevention: same hash for another order
    escrow.create_deposit_intent(order_id="ord_crypto_verify_2", amount_usd=800.0, chain=CryptoChain.BASE)
    replay_res = escrow.verify_transaction(order_id="ord_crypto_verify_2", tx_hash=valid_tx)
    assert replay_res["verified"] is False
    assert "replay" in replay_res["error"].lower() or "already redeemed" in replay_res["error"].lower()
