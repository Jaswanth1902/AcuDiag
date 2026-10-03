"""
AcuDiag Comprehensive Static Security Audit Scanner
Analyzes:
1. Hardcoded secrets, keys, and tokens in source code and documentation.
2. Unsafe network calls (SSRF in media fetchers).
3. Path traversal vulnerabilities in file ingestion.
4. Command injection or subprocess vulnerabilities (missing CREATE_NO_WINDOW).
5. Unrestricted webhook access & missing authentication.
6. Denial of Service vectors (unbounded inputs, memory bloat).
"""

import os
import re
import ast
from pathlib import Path

PROJ_ROOT = Path(__file__).resolve().parent.parent

def scan_secrets():
    findings = []
    secret_patterns = [
        ("JWT / Pine Labs Token", re.compile(r'eyJ[a-zA-Z0-9_\-]{20,}\.[a-zA-Z0-9_\-]{20,}')),
        ("Gnani API Key", re.compile(r'vach_[a-zA-Z0-9_\-]{20,}')),
        ("GitHub Personal Access Token", re.compile(r'ghp_[a-zA-Z0-9]{30,}')),
        ("AWS Access Key", re.compile(r'AKIA[0-9A-Z]{16}')),
        ("Generic Hardcoded Secret", re.compile(r'(?i)(api_key|secret_key|private_key|token)\s*=\s*[\'"][a-zA-Z0-9_\-]{16,}[\'"]'))
    ]

    for root, dirs, files in os.walk(PROJ_ROOT):
        if any(skip in root for skip in ['node_modules', '.git', '__pycache__', 'auth_session', 'credentials']):
            continue
        for f in files:
            if f.endswith(('.py', '.js', '.json', '.md', '.html', '.txt')):
                file_path = Path(root) / f
                rel_path = file_path.relative_to(PROJ_ROOT)
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    for name, pat in secret_patterns:
                        for m in pat.finditer(content):
                            # Avoid flagging harmless doc references or examples
                            val = m.group(0)
                            if "your_" in val.lower() or "example" in val.lower() or "placeholder" in val.lower():
                                continue
                            line_no = content[:m.start()].count('\n') + 1
                            findings.append({
                                "type": "SECRET_LEAK",
                                "severity": "HIGH",
                                "rule": name,
                                "file": str(rel_path),
                                "line": line_no,
                                "snippet": val[:10] + "..." + val[-6:] if len(val) > 20 else val
                            })
                except Exception as e:
                    pass
    return findings

def scan_ssrf_and_paths():
    findings = []
    for root, dirs, files in os.walk(PROJ_ROOT / "src"):
        if '__pycache__' in root:
            continue
        for f in files:
            if f.endswith('.py'):
                file_path = Path(root) / f
                rel_path = file_path.relative_to(PROJ_ROOT)
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                
                # Check for urllib with dynamic untrusted user URLs
                if "urlopen" in content or "requests.get" in content:
                    lines = content.splitlines()
                    for idx, line in enumerate(lines, 1):
                        if "urlopen" in line or "requests.get" in line:
                            # Flag only if user-supplied variable is fetched without security warden
                            context_lines = "\n".join(lines[max(0, idx-10):idx])
                            is_user_input = any(v in line for v in ["audio_source", "audio_path", "media_url", "dl_req"])
                            if is_user_input and "safe_fetch_media_bytes" not in context_lines and "validate_url_safe" not in context_lines:
                                findings.append({
                                    "type": "SSRF_VULNERABILITY",
                                    "severity": "CRITICAL",
                                    "rule": "Unrestricted Outbound HTTP Request (SSRF)",
                                    "file": str(rel_path),
                                    "line": idx,
                                    "snippet": line.strip()
                                })

                # Check for direct file open with untrusted paths
                if "open(" in content:
                    lines = content.splitlines()
                    for idx, line in enumerate(lines, 1):
                        if "open(" in line and any(v in line for v in ["audio_source", "target_path", "audio_path", "media_url"]):
                            context_lines = "\n".join(lines[max(0, idx-10):idx])
                            if "safe_resolve_audio_path" not in context_lines and "safe_fetch_media_bytes" not in context_lines and "resolve" not in context_lines:
                                findings.append({
                                    "type": "PATH_TRAVERSAL",
                                    "severity": "HIGH",
                                    "rule": "Potential Arbitrary File Read / Path Traversal",
                                    "file": str(rel_path),
                                    "line": idx,
                                    "snippet": line.strip()
                                })

    return findings

def scan_webhook_security():
    findings = []
    bridge_path = PROJ_ROOT / "src" / "whatsapp_agentic_bridge.py"
    if bridge_path.exists():
        content = bridge_path.read_text(encoding='utf-8', errors='ignore')
        if "webhook" in content:
            has_auth = any(k in content for k in ["ACUDIAG_WEBHOOK_SECRET", "X-AcuDiag-Secret", "verify_signature", "hmac", "X-Hub-Signature"])
            if not has_auth:
                findings.append({
                    "type": "UNAUTHENTICATED_WEBHOOK",
                    "severity": "CRITICAL",
                    "rule": "Missing Webhook Signature / Token Verification",
                    "file": "src/whatsapp_agentic_bridge.py",
                    "line": 105,
                    "snippet": "Endpoint accepts unauthenticated POST requests from any source."
                })
            has_rate_limit = any(k in content for k in ["rate_limiter", "RateLimiter", "rate_limit"])
            if not has_rate_limit:
                findings.append({
                    "type": "RATE_LIMIT_MISSING",
                    "severity": "HIGH",
                    "rule": "No Rate Limiting on Inbound Webhook (DoS Risk)",
                    "file": "src/whatsapp_agentic_bridge.py",
                    "line": 105,
                    "snippet": "Unbounded request rate can exhaust server CPU / memory / external credits."
                })
    return findings

def scan_subprocesses():
    findings = []
    for root, dirs, files in os.walk(PROJ_ROOT):
        if any(skip in root for skip in ['node_modules', '.git', '__pycache__']):
            continue
        for f in files:
            if f.endswith('.py'):
                file_path = Path(root) / f
                rel_path = file_path.relative_to(PROJ_ROOT)
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                if "subprocess.Popen" in content or "subprocess.run" in content or "subprocess.check_output" in content:
                    lines = content.splitlines()
                    for idx, line in enumerate(lines, 1):
                        if any(sub in line for sub in ["subprocess.Popen", "subprocess.run", "subprocess.check_output"]):
                            context_lines = "\n".join(lines[idx-1:min(len(lines), idx+5)])
                            if "CREATE_NO_WINDOW" not in context_lines and "0x08000000" not in context_lines and "creationflags" not in context_lines:
                                findings.append({
                                    "type": "SUBPROCESS_WINDOW_LEAK",
                                    "severity": "MEDIUM",
                                    "rule": "Windows Subprocess Visibility Invariant Violation (Law 8)",
                                    "file": str(rel_path),
                                    "line": idx,
                                    "snippet": line.strip()
                                })
    return findings

if __name__ == "__main__":
    s = scan_secrets()
    u = scan_ssrf_and_paths()
    w = scan_webhook_security()
    p = scan_subprocesses()
    all_findings = s + u + w + p
    print(f"Total Security Findings: {len(all_findings)}")
    for f in all_findings:
        print(f"[{f['severity']}] {f['type']} - {f['file']}:{f.get('line', '?')} - {f['rule']}")
        print(f"   Snippet: {f['snippet']}")
