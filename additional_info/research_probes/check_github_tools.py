import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def check_github_tools():
    b = PineLabsAgenticBridge()
    res = b._request("GET", "/tools")
    tools = res.get("tools", [])
    gh_tools = [t for t in tools if "github" in t.lower() or "git" in t.lower()]
    print(f"Total GitHub/Git tools found: {len(gh_tools)}")
    print(json.dumps(gh_tools, indent=2))

if __name__ == "__main__":
    check_github_tools()
