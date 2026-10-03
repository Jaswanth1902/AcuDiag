import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def check_www_auth_header():
    b = PineLabsAgenticBridge()
    url = f"{b.base_url}/knowledge"
    req = urllib.request.Request(url, headers=b._get_headers())
    try:
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print("HTTP Status:", e.code)
        print("Headers:")
        for k, v in e.headers.items():
            if "auth" in k.lower():
                print(f"  {k}: {v}")
        print("Body:", e.read().decode())

if __name__ == "__main__":
    check_www_auth_header()
