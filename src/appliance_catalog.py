"""
AcuDiag Enterprise Appliance Catalog & Rate Card Engine
Standardized multi-appliance diagnostic taxonomy, rate cards (HSN 8450, 8418, 8415, 8421),
warranty calculation rules, and dynamic replacement SKU resolution.
Strictly grounded in Databank Knowledge Base 01-08.
"""

from typing import Dict, Any, Optional, Tuple
import re

APPLIANCE_TAXONOMY = {
    "WASHING_MACHINE_FRONT_LOAD": {
        "display_name": "Front-Load Washing Machine",
        "hsn_code": "8450.90",
        "default_warranty_months": 24,
        "extended_motor_months": 120,
        "faults": {
            "WM_BEARING_SPALL": {
                "name": "Drum Bearing Outer Race Wear (BPFO 1,450 Hz)",
                "freq_range": (1380.0, 1520.0),
                "sku_suffix": "BEAR-6205-2RS",
                "part_cost": 850.0,
                "labor_cost": 400.0,
                "description": "Outer race micro-spall causing metallic friction resonance during spin cycle."
            },
            "WM_DRAIN_CAVITATION": {
                "name": "Drain Pump Impeller Flutter & Cavitation",
                "freq_range": (280.0, 380.0),
                "sku_suffix": "PUMP-DRAIN-02",
                "part_cost": 600.0,
                "labor_cost": 350.0,
                "description": "Magnetic synchronous drain pump impeller obstruction or blade cavitation."
            },
            "WM_DRIVE_BELT_SLIP": {
                "name": "Poly-V Drive Belt Slip & Glaze",
                "freq_range": (200.0, 260.0),
                "sku_suffix": "BELT-V-POLY",
                "part_cost": 450.0,
                "labor_cost": 300.0,
                "description": "Elastomer thermal decay causing continuous rotational friction slip under load."
            },
            "WM_SUSPENSION_DECAY": {
                "name": "Suspension Strut Damper Fatigue",
                "freq_range": (12.0, 70.0),
                "sku_suffix": "STRUT-SUSP-FL",
                "part_cost": 900.0,
                "labor_cost": 500.0,
                "description": "Friction damper piston grease dry-out causing unconstrained drum precession."
            }
        }
    },
    "WASHING_MACHINE_TOP_LOAD": {
        "display_name": "Top-Load Washing Machine",
        "hsn_code": "8450.90",
        "default_warranty_months": 24,
        "extended_motor_months": 120,
        "faults": {
            "WM_SUSPENSION_FAIL": {
                "name": "Suspension Damper Rod Fatigue",
                "freq_range": (12.0, 70.0),
                "sku_suffix": "DAMP-SAM-4X",
                "part_cost": 450.0,
                "labor_cost": 300.0,
                "description": "Suspension rod spring decay causing tub knocking and out-of-balance error."
            },
            "WM_DRAIN_CAVITATION": {
                "name": "Drain Valve Flapper & Cavitation Flutter",
                "freq_range": (280.0, 380.0),
                "sku_suffix": "VALVE-DRAIN-TL",
                "part_cost": 500.0,
                "labor_cost": 350.0,
                "description": "Drain valve obstruction causing cavitation airlock during discharge."
            }
        }
    },
    "REFRIGERATOR": {
        "display_name": "Frost-Free Refrigerator",
        "hsn_code": "8418.99",
        "default_warranty_months": 12,
        "extended_motor_months": 120,
        "faults": {
            "REF_COMPRESSOR_FLUTTER": {
                "name": "Inverter BLDC Compressor Valve Flutter",
                "freq_range": (1750.0, 1950.0),
                "sku_suffix": "COMP-INV-BLDC-01",
                "part_cost": 3800.0,
                "labor_cost": 2000.0,
                "description": "Suction flapper valve fatigue causing thermodynamic pressure loss."
            },
            "REF_RELAY_CHATTER": {
                "name": "PTC Starter Relay + TOP Thermal Chattering",
                "freq_range": (90.0, 150.0),
                "sku_suffix": "RELAY-PTC-TOP-04",
                "part_cost": 450.0,
                "labor_cost": 350.0,
                "description": "Locked rotor condition cycling thermal protector under high inrush current."
            },
            "REF_EVAP_FAN_STICTION": {
                "name": "Evaporator Fan Motor Stiction & Ice Rub",
                "freq_range": (780.0, 860.0),
                "sku_suffix": "FAN-EVAP-12V-DC",
                "part_cost": 750.0,
                "labor_cost": 450.0,
                "description": "Evaporator fan bearing stiction or blade contact against frost buildup."
            },
            "REF_CAPILLARY_CAVITATION": {
                "name": "Refrigerant Line Capillary Cavitation (R600a)",
                "freq_range": (2100.0, 2600.0),
                "sku_suffix": "VALVE-EXP-04",
                "part_cost": 950.0,
                "labor_cost": 700.0,
                "description": "Moisture restriction in capillary tube causing liquid boiling hiss."
            }
        }
    },
    "AIR_CONDITIONER": {
        "display_name": "Inverter Split Air Conditioner",
        "hsn_code": "8415.90",
        "default_warranty_months": 12,
        "extended_motor_months": 120,
        "faults": {
            "AC_COMPRESSOR_LEAK": {
                "name": "Rotary Inverter Compressor Discharge Valve Leak",
                "freq_range": (2200.0, 2600.0),
                "sku_suffix": "COMP-ROTARY-1.5T-R32",
                "part_cost": 6500.0,
                "labor_cost": 3400.0,
                "description": "High-velocity gas jet whistle from carbonized compressor discharge valve."
            },
            "AC_BLOWER_BUSH_SQUEAL": {
                "name": "Cross-Flow IDU Fan Sleeve Bushing Squeal",
                "freq_range": (600.0, 700.0),
                "sku_suffix": "BEAR-BUSH-IDU-RUBBER",
                "part_cost": 350.0,
                "labor_cost": 500.0,
                "description": "Dried bronze sleeve bearing causing continuous indoor blower squeal."
            },
            "AC_EEV_VALVE_JAM": {
                "name": "Electronic Expansion Valve (EEV) Stepper Motor Jam",
                "freq_range": (28.0, 35.0),
                "sku_suffix": "VALVE-EEV-COIL-500S",
                "part_cost": 1200.0,
                "labor_cost": 650.0,
                "description": "Copper shaving particulate jamming linear needle valve in outdoor unit."
            }
        }
    },
    "RO_PURIFIER": {
        "display_name": "RO Water Purifier",
        "hsn_code": "8421.99",
        "default_warranty_months": 12,
        "extended_motor_months": 36,
        "faults": {
            "RO_BOOSTER_PUMP_CAVITATION": {
                "name": "RO Booster Pump Diaphragm Cavitation & Bearing Wear",
                "freq_range": (600.0, 700.0),
                "sku_suffix": "PUMP-RO-100GPD",
                "part_cost": 1450.0,
                "labor_cost": 350.0,
                "description": "Eccentric cam bearing calcification causing severe metallic hammering."
            },
            "RO_SOLENOID_CHATTER": {
                "name": "Inlet Solenoid Valve AC Chatter & Plunger Jam",
                "freq_range": (90.0, 210.0),
                "sku_suffix": "VALVE-SOLENOID-24V",
                "part_cost": 400.0,
                "labor_cost": 300.0,
                "description": "Scale deposit causing magnetic coil flutter and water hammer chatter."
            }
        }
    }
}

OEM_BRANDS = [
    "Godrej", "LG", "Samsung", "Whirlpool", "IFB", "Bosch",
    "Panasonic", "Daikin", "Voltas", "Blue Star", "Kent", "Aquaguard"
]

def resolve_brand(text: str) -> str:
    """Extracts OEM brand dynamically from text tokens with Hinglish & phonetics support."""
    t = text.lower()
    mapping = {
        "godrej": "Godrej", "गोदरेज": "Godrej", "गुटरेज": "Godrej", "गूदरेज": "Godrej",
        "lg": "LG", "एलजी": "LG",
        "samsung": "Samsung", "सैमसंग": "Samsung", "सेमसंग": "Samsung",
        "whirlpool": "Whirlpool", "व्हर्लपूल": "Whirlpool",
        "ifb": "IFB", "आईएफबी": "IFB",
        "bosch": "Bosch", "बॉश": "Bosch",
        "panasonic": "Panasonic", "पैनासोनिक": "Panasonic",
        "daikin": "Daikin", "डायकिन": "Daikin",
        "voltas": "Voltas", "वोल्टास": "Voltas",
        "blue star": "Blue Star", "ब्लू स्टार": "Blue Star",
        "kent": "Kent", "केंट": "Kent",
        "aquaguard": "Aquaguard", "एक्वागार्ड": "Aquaguard"
    }
    for token, brand in mapping.items():
        if token in t:
            return brand
    return "Generic"

def resolve_appliance_category(text: str) -> str:
    """Resolves appliance category key from natural language."""
    t = text.lower()
    if any(k in t for k in ["ac", "air conditioner", "split ac", "inverter ac", "कूलिंग", "एसी", "hiss"]):
        return "AIR_CONDITIONER"
    elif any(k in t for k in ["fridge", "refrigerator", "फ्रीज", "रेफ्रिजरेटर", "chiller"]):
        return "REFRIGERATOR"
    elif any(k in t for k in ["ro", "water purifier", "purifier", "kent", "aquaguard", "प्यूरिफायर"]):
        return "RO_PURIFIER"
    elif any(k in t for k in ["top load", "टॉप लोड"]):
        return "WASHING_MACHINE_TOP_LOAD"
    else:
        return "WASHING_MACHINE_FRONT_LOAD"

def calculate_warranty_status(
    purchase_months_ago: Optional[int],
    category_key: str,
    fault_code: str
) -> Dict[str, Any]:
    """
    Computes statutory manufacturer warranty coverage per Databank KB 06.
    Returns warranty metadata, status string, and whether paid escrow should proceed.
    """
    app_meta = APPLIANCE_TAXONOMY.get(category_key, APPLIANCE_TAXONOMY["WASHING_MACHINE_FRONT_LOAD"])
    std_limit = app_meta["default_warranty_months"]
    ext_limit = app_meta["extended_motor_months"]

    if purchase_months_ago is None:
        return {
            "status": "UNKNOWN_ASSUMED_OUT_OF_WARRANTY",
            "is_active_comprehensive": False,
            "is_active_extended": False,
            "description": "Purchase date unverified. Standardized Escrow protection active.",
            "part_discount_ratio": 0.0
        }

    if purchase_months_ago <= std_limit:
        return {
            "status": "ACTIVE_COMPREHENSIVE_OEM",
            "is_active_comprehensive": True,
            "is_active_extended": True,
            "description": f"Appliance ({purchase_months_ago} mo) is within {std_limit}-month Comprehensive OEM Warranty.",
            "part_discount_ratio": 1.0,
            "labor_discount_ratio": 1.0,
            "intercept_action": "TRANSFER_TO_OEM_FREE"
        }
    elif purchase_months_ago <= ext_limit and any(k in fault_code for k in ["COMPRESSOR", "MOTOR", "BLDC", "ROTARY"]):
        return {
            "status": "ACTIVE_EXTENDED_MOTOR_OEM",
            "is_active_comprehensive": False,
            "is_active_extended": True,
            "description": f"Comprehensive expired, but {ext_limit}-month Motor/Compressor warranty active. Part ₹0 co-pay applied.",
            "part_discount_ratio": 1.0,
            "labor_discount_ratio": 0.0,
            "intercept_action": "CO_PAY_LABOR_ONLY"
        }
    else:
        return {
            "status": "EXPIRED",
            "is_active_comprehensive": False,
            "is_active_extended": False,
            "description": f"Appliance age ({purchase_months_ago} mo) exceeds coverage ({std_limit} mo). Out-of-Warranty Escrow Active.",
            "part_discount_ratio": 0.0,
            "labor_discount_ratio": 0.0,
            "intercept_action": "PROCEED_ESCROW"
        }

def resolve_repair_docket(
    brand: str,
    category_key: str,
    fault_code: str,
    purchase_months_ago: Optional[int] = None
) -> Dict[str, Any]:
    """Generates standardized diagnostic repair quotation docket."""
    app_meta = APPLIANCE_TAXONOMY.get(category_key, APPLIANCE_TAXONOMY["WASHING_MACHINE_FRONT_LOAD"])
    fault_meta = app_meta["faults"].get(fault_code)
    if not fault_meta:
        # Fallback to first fault in category
        fault_code = next(iter(app_meta["faults"].keys()))
        fault_meta = app_meta["faults"][fault_code]

    warranty = calculate_warranty_status(purchase_months_ago, category_key, fault_code)
    
    sku_prefix = brand.upper().replace(" ", "")
    sku = f"{sku_prefix}-{fault_meta['sku_suffix']}"
    
    raw_part = fault_meta["part_cost"]
    raw_labor = fault_meta["labor_cost"]
    
    if warranty.get("intercept_action") == "TRANSFER_TO_OEM_FREE":
        billable_part = 0.0
        billable_labor = 0.0
    elif warranty.get("intercept_action") == "CO_PAY_LABOR_ONLY":
        billable_part = 0.0
        billable_labor = raw_labor
    else:
        billable_part = raw_part
        billable_labor = raw_labor

    total_inr = billable_part + billable_labor

    return {
        "brand": brand,
        "appliance": app_meta["display_name"],
        "hsn_code": app_meta["hsn_code"],
        "fault_code": fault_code,
        "fault_name": fault_meta["name"],
        "description": fault_meta["description"],
        "sku": sku,
        "tariff": {
            "part_inr": billable_part,
            "labor_inr": billable_labor,
            "total_inr": total_inr,
            "raw_part_inr": raw_part,
            "raw_labor_inr": raw_labor
        },
        "warranty": warranty
    }
