"""
AcuDiag Digital Warranty Certificate Generator
Creates tamper-evident cryptographic digital repair warranty certificates
honoring statutory Indian consumer protection laws and Pine Labs Plural settlement tokens.
Persists certificate records directly to Central Blackboard SQLite WAL (Law 14).
"""

from __future__ import annotations

import json
import time
import hashlib
import hmac
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
BLACKBOARD_DB = REPO_ROOT / ".cache" / "blackboard.sqlite"

class DigitalWarrantyEngine:
    """Issues and verifies cryptographic digital warranty certificates for AcuDiag repairs."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or BLACKBOARD_DB
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._secret = b"acudiag_digital_warranty_salt_ken_2026"
        self._init_db()

    def _init_db(self):
        import sqlite3
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS acudiag_warranties (
                    certificate_id TEXT PRIMARY KEY,
                    case_id TEXT NOT NULL,
                    customer_phone TEXT NOT NULL,
                    customer_name TEXT NOT NULL,
                    appliance_brand TEXT NOT NULL,
                    appliance_type TEXT NOT NULL,
                    defect_resolved TEXT NOT NULL,
                    sku_installed TEXT NOT NULL,
                    technician_name TEXT NOT NULL,
                    escrow_order_id TEXT NOT NULL,
                    coverage_days INTEGER DEFAULT 90,
                    issued_at TEXT NOT NULL,
                    valid_until TEXT NOT NULL,
                    digital_signature TEXT NOT NULL,
                    verification_hash TEXT NOT NULL,
                    status TEXT NOT NULL
                )
            """)
            conn.commit()

    def generate_certificate(
        self,
        case_id: str,
        customer_phone: str,
        customer_name: str,
        appliance_brand: str,
        appliance_type: str,
        defect_resolved: str,
        sku_installed: str,
        technician_name: str,
        escrow_order_id: str,
        coverage_days: int = 90
    ) -> Dict[str, Any]:
        """Generates a signed digital warranty certificate."""
        now = datetime.now(timezone.utc)
        valid_until = now + timedelta(days=coverage_days)
        
        # Deterministic certificate ID
        cert_id = f"WAR-{appliance_brand.upper().replace(' ', '')}-{case_id[-6:] if len(case_id)>=6 else int(time.time()) % 100000}"
        
        # Cryptographic verification signature
        canonical = f"{cert_id}:{case_id}:{customer_phone}:{sku_installed}:{escrow_order_id}:{coverage_days}"
        sig = hmac.new(self._secret, canonical.encode("utf-8"), hashlib.sha256).hexdigest()
        v_hash = hashlib.sha256(f"{canonical}:{sig}".encode("utf-8")).hexdigest()[:16].upper()

        cert_data = {
            "certificate_id": cert_id,
            "case_id": case_id,
            "customer_phone": customer_phone,
            "customer_name": customer_name,
            "appliance_brand": appliance_brand,
            "appliance_type": appliance_type,
            "defect_resolved": defect_resolved,
            "sku_installed": sku_installed,
            "technician_name": technician_name,
            "escrow_order_id": escrow_order_id,
            "coverage_days": coverage_days,
            "issued_at": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "valid_until": valid_until.strftime("%Y-%m-%d"),
            "digital_signature": sig,
            "verification_hash": f"VRF-{v_hash}",
            "status": "ACTIVE_VERIFIED"
        }

        import sqlite3
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO acudiag_warranties (
                    certificate_id, case_id, customer_phone, customer_name,
                    appliance_brand, appliance_type, defect_resolved, sku_installed,
                    technician_name, escrow_order_id, coverage_days, issued_at,
                    valid_until, digital_signature, verification_hash, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                cert_id, case_id, customer_phone, customer_name,
                appliance_brand, appliance_type, defect_resolved, sku_installed,
                technician_name, escrow_order_id, coverage_days, cert_data["issued_at"],
                cert_data["valid_until"], sig, cert_data["verification_hash"], "ACTIVE_VERIFIED"
            ))
            conn.commit()

        return cert_data

    def verify_certificate(self, certificate_id: str) -> Dict[str, Any]:
        """Validates a certificate against the Central Blackboard cryptographic record."""
        import sqlite3
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.execute("SELECT * FROM acudiag_warranties WHERE certificate_id = ?", (certificate_id,))
            row = cur.fetchone()
            if not row:
                return {"valid": False, "reason": "Certificate not found in registry."}
            
            data = dict(row)
            canonical = f"{data['certificate_id']}:{data['case_id']}:{data['customer_phone']}:{data['sku_installed']}:{data['escrow_order_id']}:{data['coverage_days']}"
            expected_sig = hmac.new(self._secret, canonical.encode("utf-8"), hashlib.sha256).hexdigest()
            
            if hmac.compare_digest(expected_sig, data["digital_signature"]):
                return {
                    "valid": True,
                    "certificate": data,
                    "coverage_active": True,
                    "verification_token": data["verification_hash"]
                }
            return {"valid": False, "reason": "Cryptographic signature mismatch / tampering detected."}
