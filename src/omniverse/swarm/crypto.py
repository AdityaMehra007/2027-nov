"""Cryptographic identity and digital signature utilities for OmniSwarm."""

from __future__ import annotations

import hashlib
import json
from typing import Any
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519


class SwarmCrypto:
    """Manages Ed25519 key generation, node address derivation, signing, and verification."""

    @staticmethod
    def generate_keypair() -> tuple[ed25519.Ed25519PrivateKey, ed25519.Ed25519PublicKey]:
        """Generates an Ed25519 private/public keypair."""
        private_key = ed25519.Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def derive_node_id(public_key: ed25519.Ed25519PublicKey) -> str:
        """Derives a deterministic node fingerprint string from an Ed25519 public key."""
        raw_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        digest = hashlib.sha256(raw_bytes).hexdigest()[:16]
        return f"node_{digest}"

    @classmethod
    def canonical_bytes(cls, envelope_dict: dict[str, Any]) -> bytes:
        """Serializes envelope to canonical JSON bytes (omits 'signature' key)."""
        data = {k: v for k, v in envelope_dict.items() if k != "signature"}
        canonical_str = json.dumps(data, sort_keys=True, separators=(",", ":"))
        return canonical_str.encode("utf-8")

    @classmethod
    def sign_message(
        cls,
        private_key: ed25519.Ed25519PrivateKey,
        envelope_dict: dict[str, Any],
    ) -> str:
        """Computes Ed25519 digital signature over the canonical JSON representation."""
        payload_bytes = cls.canonical_bytes(envelope_dict)
        signature = private_key.sign(payload_bytes)
        return signature.hex()

    @classmethod
    def verify_signature(
        cls,
        public_key: ed25519.Ed25519PublicKey,
        envelope_dict: dict[str, Any],
        signature_hex: str,
    ) -> bool:
        """Verifies whether the Ed25519 signature is valid for the canonical envelope."""
        try:
            sig_bytes = bytes.fromhex(signature_hex)
            payload_bytes = cls.canonical_bytes(envelope_dict)
            public_key.verify(sig_bytes, payload_bytes)
            return True
        except (InvalidSignature, ValueError):
            return False
