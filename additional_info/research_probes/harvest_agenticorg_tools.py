import urllib.request
import re
import json
from pathlib import Path

def fetch(rel_path):
    url = f"https://raw.githubusercontent.com/mishrasanjeev/agentic-org/main/{rel_path}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        return f"Error: {e}"

def extract_tools(code):
    matches = re.findall(r'_tool_registry\[["\']([^"\']+)["\']\]', code)
    return matches

target_connectors = {
    "pinelabs_plural": "connectors/finance/pinelabs_plural.py",
    "whatsapp": "connectors/comms/whatsapp.py",
    "gstn": "connectors/finance/gstn.py",
    "tally": "connectors/finance/tally.py",
    "zoho_books": "connectors/finance/zoho_books.py",
    "account_aggregator": "connectors/finance/banking_aa.py",
    "twilio": "connectors/comms/twilio.py",
    "zendesk": "connectors/ops/zendesk.py",
    "jira": "connectors/ops/jira.py",
    "servicenow": "connectors/ops/servicenow.py",
    "pagerduty": "connectors/ops/pagerduty.py",
    "github": "connectors/comms/github_connector.py",
}

results = {}
for name, path in target_connectors.items():
    code = fetch(path)
    tools = extract_tools(code)
    results[name] = {
        "repo_path": path,
        "tools": tools,
        "count": len(tools)
    }
    print(f"[{name}] ({len(tools)} tools): {tools}")

output_path = Path(__file__).resolve().parent.parent / "databank" / "agenticorg_harvested_tools.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"\nSaved all harvested tools to {output_path}")
