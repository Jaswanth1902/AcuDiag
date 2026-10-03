import os
import sys
import json
from pathlib import Path

# Add project root to sys.path
proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def run_deep_probe():
    bridge = PineLabsAgenticBridge()
    endpoints_to_probe = [
        ("GET", "/agents"),
        ("GET", "/connectors"),
        ("GET", "/workflows"),
        ("GET", "/schemas"),
        ("GET", "/approvals"),
        ("GET", "/audit?per_page=5"),
        ("GET", "/scopes"),
        ("GET", "/knowledge"),
        ("GET", "/sla"),
        ("GET", "/agent-templates"),
        ("GET", "/observatory"),
    ]
    
    results = {}
    for method, ep in endpoints_to_probe:
        res = bridge._request(method, ep)
        # Summarize result keys and counts
        if "error" in res:
            results[ep] = {"status": "ERROR", "detail": res}
        else:
            if isinstance(res, dict):
                summary = {
                    "keys": list(res.keys()),
                    "total": res.get("total", len(res.get("items", [])) if "items" in res else None),
                }
                if "items" in res and res["items"]:
                    summary["sample_item_keys"] = list(res["items"][0].keys())
                    if "name" in res["items"][0]:
                        summary["sample_item_names"] = [i.get("name") for i in res["items"][:5]]
                    elif "id" in res["items"][0]:
                        summary["sample_item_ids"] = [i.get("id") for i in res["items"][:5]]
                results[ep] = summary
            elif isinstance(res, list):
                results[ep] = {"type": "list", "count": len(res), "sample": res[:2]}
            else:
                results[ep] = {"type": type(res).__name__, "content": str(res)[:100]}

    print("=== AGENTICORG DEEP ENDPOINT PROBE RESULTS ===")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    run_deep_probe()
