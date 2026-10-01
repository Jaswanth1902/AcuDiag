import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def inspect_agent():
    b = PineLabsAgenticBridge()
    agents = b.list_agents().get("items", [])
    acudiag = [a for a in agents if a.get("name") == "AcuDiag Orchestrator"]
    if acudiag:
        print(json.dumps(acudiag[0], indent=2))
    else:
        print("AcuDiag Orchestrator not found in agents list.")

if __name__ == "__main__":
    inspect_agent()
