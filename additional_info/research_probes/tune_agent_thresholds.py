import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

AGENT_ID = "c56edea9-8cd1-4e31-bf93-48e024d445d5"

def tune_thresholds():
    bridge = PineLabsAgenticBridge()
    print(f"Tuning HITL thresholds for agent {AGENT_ID} on AgenticOrg...")
    # Lower confidence floor to 0.50 and set HITL condition to empty or low threshold
    res = bridge.update_agent_thresholds(
        agent_id=AGENT_ID,
        confidence_floor=0.50,
        hitl_condition=""
    )
    if "error" not in res:
        print("Success! Agent thresholds updated: confidence_floor=0.50, hitl_condition=''")
        print(f"Updated config: {res}")
    else:
        print(f"Update failed (check cookie): {res.get('error')}")

if __name__ == "__main__":
    tune_thresholds()
