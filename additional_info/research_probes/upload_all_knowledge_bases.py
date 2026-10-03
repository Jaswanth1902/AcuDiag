"""
AcuDiag Enterprise Knowledge Base Multi-Doc Uploader
Uploads all 6 modular domain knowledge bases to Pine Labs AgenticOrg (/knowledge):
1. Washing Machines Acoustic Kinematics
2. Refrigerators Compressor Thermodynamics
3. Air Conditioners Inverter Acoustics
4. Zero-Trust Anti-Spoofing & Fraud Gating Manual
5. Standardized Rate Card & Escrow SOP
6. OEM Warranty Intercept Directory
"""

import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def upload_all_knowledge_bases():
    b = PineLabsAgenticBridge()
    kb_dir = proj_root / "databank" / "knowledge_base"
    
    docs = [
        ("01_Washing_Machines_Acoustic_Kinematics.md", "appliances_washing_machines", "Washing Machine Acoustic Kinematics & BPFO Bearing Profiles"),
        ("02_Refrigerators_Compressor_Thermodynamics.md", "appliances_refrigerators", "Refrigerator Compressor Acoustics & Thermodynamic Fault Profiles"),
        ("03_Air_Conditioners_Inverter_Acoustics.md", "appliances_air_conditioners", "Air Conditioner Inverter Waveforms & Refrigerant Gas Leaks"),
        ("04_Zero_Trust_Anti_Spoofing_Manual.md", "security_anti_spoofing", "Zero-Trust Physical Anti-Spoofing & Speaker Replay Detection Manual"),
        ("05_Standardized_Rate_Card_and_Escrow_SOP.md", "finance_escrow_operations", "India Standardized Appliance Tariff, HSN Codes & Plural Escrow SOP"),
        ("06_OEM_Warranty_Intercept_Directory.md", "warranty_consumer_protection", "Manufacturer Warranty Rules, Extended Compressor Coverage & Fraud Intercept"),
        ("07_Microwaves_and_Water_Purifiers_Diagnostics.md", "appliances_microwaves_ro", "Microwave Magnetron Arcing & RO Booster Pump Cavitation Profiles"),
        ("08_Delhivery_Reverse_Logistics_and_Transit_SOP.md", "logistics_parts_fulfillment", "Delhivery SLA, Forward Dispatch & Tamper-Proof Reverse Return SOP")
    ]
    
    print(f"Uploading {len(docs)} enterprise knowledge bases to AgenticOrg (Tenant: {b.tenant_id})...")
    
    results = {}
    for filename, category, desc in docs:
        file_path = kb_dir / filename
        if not file_path.exists():
            print(f"Warning: {filename} does not exist!")
            continue
            
        print(f"\nProcessing {filename} [{category}]...")
        res = b.upload_knowledge_base(
            file_path=str(file_path),
            category=category,
            description=desc
        )
        status = res.get("status", "UNKNOWN")
        results[filename] = res
        print(f"  Result: {status}")
        
    summary_path = proj_root / "databank" / "knowledge_base_manifest.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print(f"\nSuccessfully processed all {len(results)} knowledge bases! Manifest saved to {summary_path}")

if __name__ == "__main__":
    upload_all_knowledge_bases()
