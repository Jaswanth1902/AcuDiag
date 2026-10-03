"""
Gnani.ai Speech Engine Client (AcuDiag Partner Rail 1)
Supports Speech-to-Text (Prisma v2.5) and Text-to-Speech (Timbre v2.5).
Pure standard library implementation (urllib) with robust mock fallbacks for offline testing.
"""

import os
import sys
import json
import uuid
import mimetypes
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, Optional, List

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class GnaniVoiceClient:
    def __init__(self, api_key: Optional[str] = None, env_path: Optional[str] = None):
        self.env_path = env_path or str(Path(__file__).resolve().parent.parent / "credentials" / "credentials.env")
        config = self._load_env(self.env_path)
        
        self.api_key = api_key or config.get("GNANI_API_KEY", "").strip('"\'')
        self.stt_url = "https://api.vachana.ai/stt/v3"
        self.tts_url = "https://api.vachana.ai/api/v1/tts/inference"

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

    def transcribe_audio(
        self,
        audio_path: str,
        language_code: str = "hi-IN",
        bias_list: Optional[List[str]] = None,
        bias_score: int = 3
    ) -> Dict[str, Any]:
        """
        Transcribe an audio file using Gnani Prisma v2.5.
        Falls back to local acoustic-transcription simulator if offline/mock.
        """
        if not self.api_key:
            # Synthetic / Simulated Ground Truth Response
            return {
                "success": True,
                "mock": True,
                "request_id": f"req_sim_{uuid.uuid4().hex[:8]}",
                "language_code": language_code,
                "transcript": "मेरी गोदरेज वॉशिंग मशीन स्पिन साइकिल में बहुत तेज़ खड़-खड़ आवाज़ कर रही है।"
            }

        # Fetch audio bytes securely with strict SSRF and path traversal defenses
        from src.security_warden import safe_fetch_media_bytes
        audio_bytes, err = safe_fetch_media_bytes(audio_path, allow_localhost_dev=True)
        if err or not audio_bytes:
            return {"success": False, "error": f"Security Ingress Protection: {err}"}

        try:
            # Build multipart/form-data payload
            boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
            body = bytearray()

            def add_field(name: str, value: str):
                body.extend(f"--{boundary}\r\n".encode("utf-8"))
                body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
                body.extend(f"{value}\r\n".encode("utf-8"))

            add_field("language_code", language_code)
            add_field("format", "transcribe")
            add_field("itn_native_numerals", "true")
            add_field("enable_substitution", "true")
            
            if bias_list:
                add_field("bias_list", json.dumps(bias_list))
                add_field("bias_score", str(bias_score))

            # Add file field
            filename = os.path.basename(audio_path) or "audio.wav"
            content_type = mimetypes.guess_type(filename)[0] or "audio/wav"
            body.extend(f"--{boundary}\r\n".encode("utf-8"))
            body.extend(f'Content-Disposition: form-data; name="audio_file"; filename="{filename}"\r\n'.encode("utf-8"))
            body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
            body.extend(audio_bytes)
            body.extend(b"\r\n")
            body.extend(f"--{boundary}--\r\n".encode("utf-8"))

            headers = {
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "X-API-Key-ID": self.api_key,
                "User-Agent": "AcuDiag-Client/1.0"
            }

            req = urllib.request.Request(self.stt_url, data=bytes(body), headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="ignore")
            return {"success": False, "status": e.code, "error": err}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def synthesize_speech(
        self,
        text: str,
        voice: str = "Nalini",
        language: str = "hi-IN",
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Synthesize speech using Gnani Timbre v2.5.
        Returns audio bytes or saves to disk.
        """
        if not self.api_key:
            return {
                "success": True,
                "mock": True,
                "voice": voice,
                "language": language,
                "text": text,
                "message": "Simulated TTS audio output (API key not configured)"
            }

        payload = {
            "text": text,
            "voice": voice,
            "model": "timbre-v2.5",
            "language": language,
            "speed": 1.0,
            "audio_config": {
                "sample_rate": 24000,
                "num_channels": 1,
                "sample_width": 2,
                "encoding": "linear_pcm",
                "container": "wav"
            }
        }

        data = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "X-API-Key-ID": self.api_key,
            "User-Agent": "AcuDiag-Client/1.0"
        }

        req = urllib.request.Request(self.tts_url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                audio_bytes = resp.read()
                if output_path:
                    with open(output_path, "wb") as f:
                        f.write(audio_bytes)
                return {
                    "success": True,
                    "bytes_received": len(audio_bytes),
                    "output_path": output_path
                }
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8")
            return {"success": False, "status": e.code, "error": err}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def test_connection(self) -> Dict[str, Any]:
        """Validates Gnani Vachana API credentials by sending a lightweight check."""
        if not self.api_key:
            return {"connected": False, "error": "GNANI_API_KEY is not configured in credentials.env"}
        
        payload = {
            "text": "परीक्षण",
            "voice": "Nalini",
            "model": "timbre-v2.5",
            "language": "hi-IN",
            "speed": 1.0,
            "audio_config": {
                "sample_rate": 16000,
                "num_channels": 1,
                "sample_width": 2,
                "encoding": "linear_pcm",
                "container": "wav"
            }
        }
        data = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "X-API-Key-ID": self.api_key,
            "User-Agent": "AcuDiag-Client/1.0"
        }
        req = urllib.request.Request(self.tts_url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    return {"connected": True, "status": 200, "message": "Gnani Vachana API authenticated successfully"}
                return {"connected": False, "status": resp.status}
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="ignore")
            return {"connected": False, "status": e.code, "error": err}
        except Exception as e:
            return {"connected": False, "error": str(e)}

if __name__ == "__main__":
    client = GnaniVoiceClient()
    print("Testing GnaniVoiceClient...")
    res = client.transcribe_audio("dummy.wav")
    print("STT Result:", json.dumps(res, ensure_ascii=False, indent=2))
    tts_res = client.synthesize_speech("नमस्ते, आपकी मशीन ठीक हो गई है।")
    print("TTS Result:", json.dumps(tts_res, ensure_ascii=False, indent=2))
