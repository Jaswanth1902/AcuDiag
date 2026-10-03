import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def inspect_schemas():
    b = PineLabsAgenticBridge()
    schemas = b.list_schemas()
    print("=== SCHEMAS ===")
    print(json.dumps(schemas, indent=2))

if __name__ == "__main__":
    inspect_schemas()
