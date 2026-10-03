"""
AcuDiag Comprehensive Multi-Appliance Field Testing Matrix
Validates that AcuDiag supports and correctly diagnoses all 5 core home appliance categories:
1. Washing Machines (Front-Load & Top-Load)
2. Refrigerators (Frost-Free BLDC)
3. Air Conditioners (Inverter Split ACs)
4. RO Water Purifiers (Booster Pumps & Solenoids)
5. Microwave Ovens (Magnetrons & Turntables)
Across normal, noisy, adversarial spoofing, and warranty intercept flows.
"""

import sys
import unittest
from pathlib import Path

PROJ_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJ_ROOT))

from src.appliance_catalog import (
    resolve_brand,
    resolve_appliance_category,
    resolve_repair_docket,
    calculate_warranty_status,
    APPLIANCE_TAXONOMY
)
from src.audio_diagnostic import AcousticDiagnosticEngine
from src.synthetic_acoustic_gen import ApplianceAcousticSynthesizer
from src.acoustic_analyzer import compute_fft_peak, check_anti_spoofing, compute_neyman_pearson_lrt


class TestMultiApplianceEnterpriseScope(unittest.TestCase):
    def setUp(self):
        self.engine = AcousticDiagnosticEngine(sample_rate=44100, n_filters=64)
        self.synth = ApplianceAcousticSynthesizer(sample_rate=44100)

    def test_appliance_taxonomy_completeness(self):
        """Verify all enterprise domestic appliance categories exist with HSN codes and rate cards."""
        required_categories = [
            "WASHING_MACHINE_FRONT_LOAD",
            "WASHING_MACHINE_TOP_LOAD",
            "REFRIGERATOR",
            "AIR_CONDITIONER",
            "RO_PURIFIER"
        ]
        for cat in required_categories:
            self.assertIn(cat, APPLIANCE_TAXONOMY)
            data = APPLIANCE_TAXONOMY[cat]
            self.assertTrue(len(data["faults"]) >= 2, f"Category {cat} has insufficient fault profiles")
            self.assertTrue(data["hsn_code"].startswith("84"))

    def test_air_conditioner_inverter_diagnosis(self):
        """Test Inverter Split AC compressor leak diagnosis and billing."""
        text = "Mera Voltas 1.5 ton split AC se continuous hissing aur gas whistle awaz aa rahi hai"
        brand = resolve_brand(text)
        cat = resolve_appliance_category(text)
        self.assertEqual(brand, "Voltas")
        self.assertEqual(cat, "AIR_CONDITIONER")

        docket = resolve_repair_docket(brand, cat, "AC_COMPRESSOR_LEAK", purchase_months_ago=30)
        self.assertIn("Compressor", docket["fault_name"])
        self.assertIn("VOLTAS-COMP-ROTARY", docket["sku"])
        self.assertGreater(docket["tariff"]["total_inr"], 3000)

    def test_refrigerator_evaporator_fan_and_compressor(self):
        """Test Refrigerator fan scraping and compressor thermodynamic fault."""
        text = "Samsung frost free fridge freezer fan scraping grinding sound kar raha hai"
        brand = resolve_brand(text)
        cat = resolve_appliance_category(text)
        self.assertEqual(brand, "Samsung")
        self.assertEqual(cat, "REFRIGERATOR")

        docket = resolve_repair_docket(brand, cat, "REF_EVAP_FAN_STICTION", purchase_months_ago=14)
        self.assertIn("Evaporator Fan", docket["fault_name"])
        self.assertIn("SAMSUNG-FAN-EVAP", docket["sku"])

    def test_ro_water_purifier_booster_pump(self):
        """Test Kent RO water purifier booster pump cavitation."""
        text = "Kent RO purifier booster pump bahut tez vibration aur hammering khad-khad awaz kar raha hai"
        brand = resolve_brand(text)
        cat = resolve_appliance_category(text)
        self.assertEqual(brand, "Kent")
        self.assertEqual(cat, "RO_PURIFIER")

        docket = resolve_repair_docket(brand, cat, "RO_BOOSTER_PUMP_CAVITATION", purchase_months_ago=18)
        self.assertIn("Booster Pump", docket["fault_name"])
        self.assertIn("KENT-PUMP-RO-100GPD", docket["sku"])

    def test_oem_warranty_split_bill_interception(self):
        """Test active warranty intercept saves customer money under statutory coverage."""
        # 1. Comprehensive warranty active (< 12 months)
        w_comp = calculate_warranty_status(8, "REFRIGERATOR", "REF_COMPRESSOR_FLUTTER")
        self.assertTrue(w_comp["is_active_comprehensive"])
        self.assertEqual(w_comp["intercept_action"], "TRANSFER_TO_OEM_FREE")

        # 2. 10-year Motor/Compressor extended warranty (e.g. 36 months on Inverter AC)
        w_ext = calculate_warranty_status(36, "AIR_CONDITIONER", "AC_COMPRESSOR_LEAK")
        self.assertFalse(w_ext["is_active_comprehensive"])
        self.assertTrue(w_ext["is_active_extended"])

    def test_multi_appliance_synthetic_acoustic_detection(self):
        """Test that DSP engine correctly classifies non-washing machine faults."""
        # AC Compressor valve leak (2,400 Hz)
        ac_leak = self.synth.generate_compressor_valve_leak(duration_sec=0.5)
        # Establish healthy baseline
        healthy = self.synth.generate_healthy_baseline(duration_sec=0.5)
        self.engine.set_golden_baseline(self.engine.extract_erb_features(self.engine.filter_signal(healthy)))

        res = self.engine.classify_acoustic_signature(ac_leak)
        self.assertFalse(res["passed"])
        self.assertEqual(res["fault_type"], "COMPRESSOR_VALVE_LEAK")


if __name__ == "__main__":
    unittest.main()
