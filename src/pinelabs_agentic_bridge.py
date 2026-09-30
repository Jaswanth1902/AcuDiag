"""
Pine Labs AgenticOrg Bridge & Autonomous Connection Engine
Connects Antigravity runtime to the Pine Labs AgenticOrg Platform (v4.8.0 / LangGraph v1.1).
Zero external dependencies (uses standard library urllib).
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, Optional, List

class PineLabsAgenticBridge:
    def __init__(self, env_path: Optional[str] = None):
        self.base_url = "https://agenticorg.hackathon.pinelabs.com/api/v1"
        self.env_path = env_path or str(Path(__file__).resolve().parent.parent / "credentials" / "credentials.env")
        self.config = self._load_env(self.env_path)
        
        self.session_cookie = self.config.get("PINELABS_SESSION_COOKIE", "").strip('"\'')
        self.csrf_token = self.config.get("PINELABS_CSRF_TOKEN", "").strip('"\'')
        self.tenant_id = self.config.get("PINELABS_TENANT_ID", "").strip('"\'')
        self.user_id = self.config.get("PINELABS_USER_ID", "").strip('"\'')

    def _load_env(self, path: str) -> Dict[str, str]:
        config = {}
        if not os.path.exists(path):
            return config
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    config[k.strip()] = v.strip()
        return config

    def _get_headers(self, is_json: bool = True) -> Dict[str, str]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Cookie": f"agenticorg_session={self.session_cookie}; agenticorg_csrf={self.csrf_token}"
        }
        if self.csrf_token:
            headers["X-CSRF-Token"] = self.csrf_token
        if is_json:
            headers["Content-Type"] = "application/json"
        return headers

    def _request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers(is_json=(data is not None))
        req_data = json.dumps(data).encode("utf-8") if data is not None else None
        
        req = urllib.request.Request(url, data=req_data, headers=headers, method=method.upper())
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read().decode("utf-8")
                return json.loads(content)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            try:
                err_json = json.loads(err_body)
                return {"error": err_json, "status": e.code}
            except Exception:
                return {"error": err_body, "status": e.code}
        except Exception as e:
            return {"error": str(e), "status": 500}

    def list_agents(self) -> Dict[str, Any]:
        """Fetch list of provisioned agents."""
        return self._request("GET", "/agents")

    def list_connectors(self) -> Dict[str, Any]:
        """Fetch all connected connectors."""
        return self._request("GET", "/connectors")

    def list_workflows(self) -> Dict[str, Any]:
        """Fetch configured workflows."""
        return self._request("GET", "/workflows")

    def list_schemas(self) -> Dict[str, Any]:
        """Fetch schema registry entries."""
        return self._request("GET", "/schemas")

    def list_approvals(self, status: str = "pending") -> Dict[str, Any]:
        """Fetch approvals queue."""
        return self._request("GET", f"/approvals?status={status}")

    def list_audit_logs(self, limit: int = 10) -> Dict[str, Any]:
        """Fetch latest audit events."""
        return self._request("GET", f"/audit?per_page={limit}")

    def register_connector(
        self,
        connector_id: str,
        name: str,
        base_url: str,
        connector_type: str = "rest",
        endpoints: Optional[List[str]] = None,
        scopes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Register a custom connector with Pine Labs AgenticOrg."""
        payload = {
            "id": connector_id,
            "name": name,
            "base_url": base_url,
            "type": connector_type,
            "endpoints": endpoints or [],
            "scopes": scopes or ["read", "write"],
            "tenant_id": self.tenant_id
        }
        res = self._request("POST", "/connectors", payload)
        if "error" in res:
            # Fallback/Local registry persistence with unvarnished status
            self._save_local_registry("connectors", connector_id, {**payload, "registered_locally": True, "remote_error": res["error"]})
            return {"status": "LOCAL_FALLBACK", "connector": payload, "remote_response": res}
        return res

    def upload_knowledge_base(
        self,
        file_path: str,
        category: str = "appliances",
        description: str = "AcuDiag Appliance Acoustic Knowledge Base"
    ) -> Dict[str, Any]:
        """Upload markdown or text knowledge base to AgenticOrg /knowledge."""
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}", "status": 404}
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        filename = os.path.basename(file_path)
        payload = {
            "title": filename,
            "category": category,
            "description": description,
            "content": content,
            "filename": filename,
            "tenant_id": self.tenant_id
        }
        res = self._request("POST", "/knowledge", payload)
        if "error" in res:
            self._save_local_registry("knowledge", filename, {**payload, "registered_locally": True, "remote_error": res["error"]})
            return {"status": "LOCAL_FALLBACK", "knowledge_doc": filename, "remote_response": res}
        return res

    def provision_agent(
        self,
        name: str = "AcuDiag Orchestrator",
        role: str = "Autonomous Appliance Reliability & Escrow Orchestrator",
        system_prompt: Optional[str] = None,
        authorized_connectors: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Provision the virtual employee agent in AgenticOrg fleet."""
        default_prompt = (
            "You are AcuDiag, the Autonomous Appliance Reliability & Escrow Orchestrator.\n"
            "You operate under zero-trust physical verification across Gnani (Voice), Pine Labs (Payments), and Delhivery (Logistics).\n\n"
            "STRICT INVARIANTS:\n"
            "1. VOICE INTAKE: Process user voice via Gnani STT. Parse Hinglish and regional code-switching. Isolate appliance symptoms into [SUBSYSTEM_FAULT].\n"
            "2. ESCROW GATE: Never dispatch a technician or parts until Pine Labs confirms PRE_AUTH_LOCKED. If declined (402), send WhatsApp payment link and halt.\n"
            "3. NOISE GATING: Before evaluating acoustic diagnostics, check SNR. If SNR < 15 dB, REJECT test with instruction: \"Ambient noise too high, please close doors and re-record.\"\n"
            "4. ANTI-SPOOFING: Inspect phase variance and low-frequency rumble (<120Hz). If audio originates from a speaker rather than physical machine vibration, trigger REJECTED_REPLAY_ATTACK and alert customer.\n"
            "5. ESCROW RELEASE CONDITION: Call Pine Labs capture ONLY when Neyman-Pearson LRT <= 2.45 AND Anti-Spoofing is TRUE.\n"
            "6. FAKE REPAIR PROTOCOL: If post-repair test FAILS, KEEP ESCROW LOCKED. Notify technician: \"Diagnostic test failed. Payout withheld. Scheduling secondary audit.\"\n"
            "7. TIMEOUT IDEMPOTENCY: On 504 Gateway Timeout, never retry duplicate charges. Queue transaction with SHA-256 idempotency key and poll Plural webhook."
        )
        payload = {
            "name": name,
            "role": role,
            "system_prompt": system_prompt or default_prompt,
            "version": "3.0.0",
            "connectors": authorized_connectors or ["delhivery_acudiag", "gnani_acudiag", "pinelabs_plural"],
            "tenant_id": self.tenant_id,
            "status": "ACTIVE"
        }
        res = self._request("POST", "/agents", payload)
        if "error" in res:
            self._save_local_registry("agents", name, {**payload, "registered_locally": True, "remote_error": res["error"]})
            return {"status": "LOCAL_FALLBACK", "agent": payload, "remote_response": res}
        return res

    def _save_local_registry(self, category: str, item_id: str, data: Dict[str, Any]):
        """Persist platform objects locally when remote endpoint is unauthenticated."""
        cache_dir = Path(__file__).resolve().parent.parent / ".cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        reg_file = cache_dir / "agenticorg_registry.json"
        
        registry = {}
        if reg_file.exists():
            try:
                with open(reg_file, "r", encoding="utf-8") as f:
                    registry = json.load(f)
            except Exception:
                registry = {}
        
        if category not in registry:
            registry[category] = {}
        registry[category][item_id] = data

        with open(reg_file, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2)

    def provision_full_acudiag_stack(self, mock_server_url: str = "http://127.0.0.1:8000") -> Dict[str, Any]:
        """Execute end-to-end provisioning: connectors, knowledge, and orchestrator agent."""
        results = {}

        # 1. Register Delhivery Connector
        results["delhivery_connector"] = self.register_connector(
            connector_id="delhivery_acudiag",
            name="Delhivery Express & CMU Logistics",
            base_url=f"{mock_server_url}",
            endpoints=["/api/cmu/pincode", "/api/cmu/create.json", "/fm/request/new/", "/api/v1/packages/json/"],
            scopes=["cmu:create", "cmu:read", "pincode:read", "fm:create"]
        )

        # 2. Register Gnani Connector
        results["gnani_connector"] = self.register_connector(
            connector_id="gnani_acudiag",
            name="Gnani Indic Speech Engine",
            base_url=f"{mock_server_url}",
            endpoints=["/stt/v3", "/api/v1/tts/inference"],
            scopes=["stt:transcribe", "tts:synthesize"]
        )

        # 3. Upload Appliance Knowledge Base
        kb_path = str(Path(__file__).resolve().parent.parent / "docs" / "acudiag_appliance_specs.md")
        results["knowledge_base"] = self.upload_knowledge_base(
            file_path=kb_path,
            category="appliance_diagnostics",
            description="AcuDiag Acoustic Failure Signatures & Decision Boundaries"
        )

        # 4. Provision AcuDiag Orchestrator
        results["orchestrator_agent"] = self.provision_agent(
            name="AcuDiag Orchestrator",
            role="Autonomous Appliance Reliability & Escrow Orchestrator",
            authorized_connectors=["delhivery_acudiag", "gnani_acudiag", "pinelabs_plural"]
        )

        return results

    def get_status_summary(self) -> Dict[str, Any]:
        """Verify full connectivity and return a unified platform status summary."""
        agents_res = self.list_agents()
        connectors_res = self.list_connectors()
        audit_res = self.list_audit_logs(limit=5)
        
        agents_count = len(agents_res.get("items", [])) if "items" in agents_res else 0
        connectors_count = len(connectors_res.get("items", [])) if "items" in connectors_res else 0
        active_connectors = [c.get("name") for c in connectors_res.get("items", [])]
        
        # Check local registry if remote is offline
        cache_dir = Path(__file__).resolve().parent.parent / ".cache"
        reg_file = cache_dir / "agenticorg_registry.json"
        local_registry = {}
        if reg_file.exists():
            try:
                with open(reg_file, "r", encoding="utf-8") as f:
                    local_registry = json.load(f)
            except Exception:
                pass

        return {
            "connected": bool(agents_count or "items" in agents_res),
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "total_agents": agents_count or len(local_registry.get("agents", {})),
            "total_connectors": connectors_count or len(local_registry.get("connectors", {})),
            "active_connectors": active_connectors or list(local_registry.get("connectors", {}).keys()),
            "audit_events_count": len(audit_res.get("items", [])) if "items" in audit_res else 0,
            "local_fallback_active": bool(local_registry)
        }

if __name__ == "__main__":
    bridge = PineLabsAgenticBridge()
    print("Testing PineLabs AgenticOrg Bridge Connection...")
    status = bridge.get_status_summary()
    print(json.dumps(status, indent=2))

