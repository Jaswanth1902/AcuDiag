"""
AcuDiag Secure Tunnel Launcher for Mock Server & Connectors.
Spawns cloudflared or ngrok windowlessly (CREATE_NO_WINDOW per Law 8).
Provides a public HTTPS URL for Pine Labs AgenticOrg custom connector callbacks.
"""

import os
import sys
import shutil
import subprocess
import time
import urllib.request
import json
from pathlib import Path

CREATE_NO_WINDOW = 0x08000000

def launch_tunnel(port: int = 8000) -> str:
    """Launch cloudflared or ngrok tunnel windowlessly."""
    cloudflared = shutil.which("cloudflared")
    ngrok = shutil.which("ngrok")

    if cloudflared:
        print(f"[*] Starting cloudflared tunnel to localhost:{port} (windowless)...")
        proc = subprocess.Popen(
            [cloudflared, "tunnel", "--url", f"http://127.0.0.1:{port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=CREATE_NO_WINDOW,
            text=True
        )
        # Parse output for trycloudflare URL
        time.sleep(3)
        return f"Tunnel running (PID: {proc.pid}) via cloudflared."
    elif ngrok:
        print(f"[*] Starting ngrok tunnel to localhost:{port} (windowless)...")
        proc = subprocess.Popen(
            [ngrok, "http", str(port)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=CREATE_NO_WINDOW
        )
        time.sleep(2)
        try:
            req = urllib.request.Request("http://127.0.0.1:4040/api/tunnels")
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode())
                public_url = data["tunnels"][0]["public_url"]
                return f"Ngrok Public URL: {public_url}"
        except Exception:
            return f"Ngrok started (PID: {proc.pid}). Connect to 127.0.0.1:4040 to view public URL."
    else:
        return "[!] Neither cloudflared nor ngrok found in PATH. Server remains on http://127.0.0.1:8000."

if __name__ == "__main__":
    msg = launch_tunnel(8000)
    print(msg)
