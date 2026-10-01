import urllib.request
import json

def fetch_well_known():
    url = "https://agenticorg.hackathon.pinelabs.com/.well-known/oauth-protected-resource/api/v1/marketplace-surface/hosted-mcp"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            print("Status:", resp.code)
            print("Body:", json.dumps(json.loads(resp.read().decode()), indent=2))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    fetch_well_known()
