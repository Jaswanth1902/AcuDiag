import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def test_bearer_auth():
    b = PineLabsAgenticBridge()
    jwt_token = b.session_cookie
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Cookie": f"agenticorg_session={b.session_cookie}; agenticorg_csrf={b.csrf_token}",
        "X-CSRF-Token": b.csrf_token,
        "Authorization": f"Bearer {jwt_token}"
    }
    
    endpoints = ["/knowledge", "/scopes", "/sla", "/observatory"]
    results = {}
    for ep in endpoints:
        url = f"{b.base_url}{ep}"
        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                results[ep] = {"code": resp.code, "body": json.loads(resp.read().decode())}
        except urllib.error.HTTPError as e:
            results[ep] = {"code": e.code, "error": e.read().decode()}
        except Exception as e:
            results[ep] = {"error": str(e)}
            
    print("=== BEARER AUTH TEST RESULTS ===")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    test_bearer_auth()
