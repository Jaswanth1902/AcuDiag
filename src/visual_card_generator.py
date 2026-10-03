"""
AcuDiag Visual Health Scorecard & ASCII/SVG Component Architecture
Transforms raw DSP metrics (SNR dB, Neyman-Pearson LRT ratio) into human-readable visual scorecards,
exploded blueprint diagrams, and before/after acoustic spectral charts for WhatsApp & Cockpit HUD.
"""

from typing import Dict, Any, Optional

def generate_ascii_health_gauge(lrt_ratio: float, snr_db: float, is_spoof: bool) -> str:
    """Generates an intuitive visual ASCII health gauge for WhatsApp chats."""
    if is_spoof:
        return (
            "🚨 *MECHANICAL HEALTH STATUS: FRAUD ALERT*\n"
            "┌──────────────────────────────┐\n"
            "│ 🔴 [████████████] CRITICAL FRAUD │\n"
            "└──────────────────────────────┘\n"
            "• Acoustic Signal: Loudspeaker Replay Detected (Zero Chassis Contact)"
        )

    if lrt_ratio <= 2.45:
        # Healthy status
        percentage = max(0, min(20, int((lrt_ratio / 2.45) * 20)))
        bar = "█" * (percentage // 2) + "░" * (10 - (percentage // 2))
        return (
            "✅ *MECHANICAL HEALTH STATUS: HEALTHY / REPAIRED*\n"
            f"┌──────────────────────────────┐\n"
            f"│ 🟢 [{bar}] {percentage}% Anomaly  │\n"
            f"└──────────────────────────────┘\n"
            f"• Signal Quality: Clean ({snr_db} dB SNR)\n"
            "• Structural Vibration: Normal smooth rotation (Zero resonant spalls)"
        )
    elif lrt_ratio <= 5.0:
        # Moderate defect
        percentage = min(75, int(25 + (lrt_ratio - 2.45) * 15))
        bar = "█" * (percentage // 10) + "░" * (10 - (percentage // 10))
        return (
            "⚠️ *MECHANICAL HEALTH STATUS: DEFECT DETECTED*\n"
            f"┌──────────────────────────────┐\n"
            f"│ 🟡 [{bar}] {percentage}% Anomaly  │\n"
            f"└──────────────────────────────┘\n"
            f"• Signal Quality: Validated ({snr_db} dB SNR)\n"
            "• Resonance: Mechanical fatigue / wear harmonic detected"
        )
    else:
        # Severe defect
        percentage = min(98, int(75 + (lrt_ratio - 5.0) * 5))
        bar = "█" * (percentage // 10) + "░" * (10 - (percentage // 10))
        return (
            "🛑 *MECHANICAL HEALTH STATUS: CRITICAL FAILURE*\n"
            f"┌──────────────────────────────┐\n"
            f"│ 🔴 [{bar}] {percentage}% Anomaly  │\n"
            f"└──────────────────────────────┘\n"
            f"• Signal Quality: Validated ({snr_db} dB SNR)\n"
            "• Warning: Severe component spall or breakdown active"
        )

def generate_exploded_blueprint_ascii(appliance_type: str, fault_code: str, sku: str) -> str:
    """Generates an ASCII Da Vinci style exploded component diagram."""
    if "BEARING" in fault_code:
        return (
            "📐 *OEM SUBASSEMBLY SCHEMATIC: DRUM & SHAFT ASSEMBLY*\n"
            "```\n"
            "       [ Front Drum Tub ]\n"
            "              │\n"
            "     ═════════╪═════════ (Outer Bearing Housing)\n"
            "     ║   [●]  │  [●]   ║ <-- ⚠️ DEFECT: Drum Bearing\n"
            "     ║  (SKF 6205-2RS) ║     SKU: " + sku + "\n"
            "     ═════════╪═════════\n"
            "              │\n"
            "       [ Drive Pulley ] ──(Poly-V Belt)── [ BLDC Motor ]\n"
            "```\n"
            "• *Location:* Rear bearing spindle behind spider assembly.\n"
            "• *Action:* Replace bearing + dual lip rubber seal to restore water tightness."
        )
    elif "CAVITATION" in fault_code or "PUMP" in fault_code:
        return (
            "📐 *OEM SUBASSEMBLY SCHEMATIC: DRAIN HYDRAULICS*\n"
            "```\n"
            "       [ Sump Bellows Hose ]\n"
            "                 │\n"
            "       ┌─────────┴─────────┐\n"
            "       │  [Impeller Cavity]│ <-- ⚠️ DEFECT: Cavitation/Lock\n"
            "       │    ( ✹ ✹ ✹ )      │     SKU: " + sku + "\n"
            "       └─────────┬─────────┘\n"
            "                 │\n"
            "       [ Discharge Hose ] ──> Standpipe Drain\n"
            "```\n"
            "• *Location:* Bottom-right chassis front access door.\n"
            "• *Action:* Clean filter debris and replace 30W magnetic synchronous pump."
        )
    elif "COMPRESSOR" in fault_code or "LEAK" in fault_code:
        return (
            "📐 *OEM SUBASSEMBLY SCHEMATIC: REFRIGERANT CIRCUIT*\n"
            "```\n"
            "       [ Evaporator Coil ] ──(Suction 5/8\")──┐\n"
            "                                             │\n"
            "       ┌───────────────────────────────┐     │\n"
            "       │  [Twin-Rotary Inverter ODU]   │ <───┘\n"
            "       │  ⚠️ Discharge Flapper Valve   │     SKU: " + sku + "\n"
            "       └───────────────┬───────────────┘\n"
            "                       │\n"
            "       (Discharge 3/8\")┴──> [ Condenser Coil ]\n"
            "```\n"
            "• *Location:* Outdoor unit hermetic compressor casing.\n"
            "• *Action:* Recover refrigerant, vacuum to 500 microns, replace valve/compressor."
        )
    else:
        return (
            "📐 *OEM COMPONENT SCHEMATIC: SUBSYSTEM*\n"
            "```\n"
            "       [ Power Relay ] ─── [ Component: " + sku + " ] ─── [ Ground ]\n"
            "```\n"
            "• *Action:* Direct standardized OEM replacement."
        )
