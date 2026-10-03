"""
AcuDiag Visual Component & Cryptographic Warranty Verification Tests
Validates:
1. ASCII Health Gauge rendering across healthy, moderate, critical, and fraud states.
2. Exploded OEM Subassembly Schematics generation for washing machines, pumps, and ACs.
3. Cryptographic Digital Warranty issuance, Central Blackboard WAL storage, and HMAC-SHA256 tamper verification.
"""

import sys
import unittest
import sqlite3
from pathlib import Path

PROJ_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJ_ROOT))

from src.visual_card_generator import (
    generate_ascii_health_gauge,
    generate_exploded_blueprint_ascii,
)
from src.digital_warranty import DigitalWarrantyEngine

class TestVisualAndWarranty(unittest.TestCase):
    def setUp(self):
        self.engine = DigitalWarrantyEngine()

    def test_ascii_health_gauge_healthy(self):
        gauge = generate_ascii_health_gauge(lrt_ratio=0.45, snr_db=25.2, is_spoof=False)
        self.assertIn("HEALTHY / REPAIRED", gauge)
        self.assertIn("25.2 dB SNR", gauge)
        self.assertIn("Zero resonant spalls", gauge)

    def test_ascii_health_gauge_defect(self):
        gauge = generate_ascii_health_gauge(lrt_ratio=3.8, snr_db=22.1, is_spoof=False)
        self.assertIn("DEFECT DETECTED", gauge)
        self.assertIn("wear harmonic detected", gauge)

    def test_ascii_health_gauge_critical(self):
        gauge = generate_ascii_health_gauge(lrt_ratio=7.5, snr_db=18.0, is_spoof=False)
        self.assertIn("CRITICAL FAILURE", gauge)
        self.assertIn("Severe component spall", gauge)

    def test_ascii_health_gauge_spoof(self):
        gauge = generate_ascii_health_gauge(lrt_ratio=0.3, snr_db=30.0, is_spoof=True)
        self.assertIn("FRAUD ALERT", gauge)
        self.assertIn("Loudspeaker Replay Detected", gauge)

    def test_exploded_blueprint_bearing(self):
        bp = generate_exploded_blueprint_ascii("Washing Machine", "WM_BEARING_SPALL", "SKF-6205-2RS")
        self.assertIn("OEM SUBASSEMBLY SCHEMATIC: DRUM & SHAFT ASSEMBLY", bp)
        self.assertIn("SKF-6205-2RS", bp)
        self.assertIn("Rear bearing spindle behind spider assembly", bp)

    def test_exploded_blueprint_pump(self):
        bp = generate_exploded_blueprint_ascii("Washing Machine", "WM_DRAIN_CAVITATION", "PUMP-30W-SYNC")
        self.assertIn("OEM SUBASSEMBLY SCHEMATIC: DRAIN HYDRAULICS", bp)
        self.assertIn("PUMP-30W-SYNC", bp)

    def test_exploded_blueprint_compressor(self):
        bp = generate_exploded_blueprint_ascii("Air Conditioner", "AC_COMPRESSOR_LEAK", "COMP-INVERTER-TWIN")
        self.assertIn("OEM SUBASSEMBLY SCHEMATIC: REFRIGERANT CIRCUIT", bp)
        self.assertIn("COMP-INVERTER-TWIN", bp)

    def test_digital_warranty_lifecycle(self):
        cert = self.engine.generate_certificate(
            case_id="CAS_884102",
            customer_phone="919845011042",
            customer_name="Priya Sharma",
            appliance_brand="Godrej",
            appliance_type="Washing Machine",
            defect_resolved="Outer Bearing Spall Eradicated",
            sku_installed="GODREJ-BEAR-6205-2RS",
            technician_name="Suresh Kumar",
            escrow_order_id="ESC_PLURAL_884102",
            coverage_days=90
        )
        self.assertEqual(cert["status"], "ACTIVE_VERIFIED")
        self.assertTrue(cert["certificate_id"].startswith("WAR-GODREJ-"))
        self.assertTrue(cert["verification_hash"].startswith("VRF-"))

        # Verify cryptographic integrity
        val = self.engine.verify_certificate(cert["certificate_id"])
        self.assertTrue(val["valid"])
        self.assertTrue(val["coverage_active"])
        self.assertEqual(val["verification_token"], cert["verification_hash"])

    def test_digital_warranty_tamper_detection(self):
        cert = self.engine.generate_certificate(
            case_id="CAS_772101",
            customer_phone="919876543210",
            customer_name="Arun Verma",
            appliance_brand="LG",
            appliance_type="Refrigerator",
            defect_resolved="Evaporator Fan Stiction Fixed",
            sku_installed="LG-FAN-9W-BLDC",
            technician_name="Ramesh",
            escrow_order_id="ESC_PLURAL_772101"
        )
        cert_id = cert["certificate_id"]

        # Directly tamper with record in Central Blackboard DB
        with sqlite3.connect(str(self.engine.db_path)) as conn:
            conn.execute(
                "UPDATE acudiag_warranties SET sku_installed = 'COUNTERFEIT_PART' WHERE certificate_id = ?",
                (cert_id,)
            )
            conn.commit()

        # Verification must now fail
        val = self.engine.verify_certificate(cert_id)
        self.assertFalse(val["valid"])
        self.assertIn("tampering detected", val["reason"])

if __name__ == "__main__":
    unittest.main()
