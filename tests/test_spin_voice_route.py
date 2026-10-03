import json
import sys
from pathlib import Path

PROJ_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJ_ROOT))

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from fastapi.testclient import TestClient
from src.whatsapp_agentic_bridge import app

client = TestClient(app)

def _send_webhook(payload, label):
    resp = client.post("/api/whatsapp/webhook", json=payload)
    data = resp.json()
    print(f"\n--- {label} ---")
    reply = data.get("reply", "")
    print(f"Status: {resp.status_code}")
    print("Reply Header:", reply.split("\n")[0] if "\n" in reply else reply[:60])
    first_lines = [l for l in reply.split("\n")[:5] if l.strip()]
    for l in first_lines:
        print(" ", l[:80])
    return reply

if __name__ == "__main__":
    test_user = "31066001813604"
    
    # TEST 1: Initial Complaint Voice Note Transcript (Hindi)
    res1 = _send_webhook({
        "Body": "मेरे गुटरेज वाशिंग मशीन स्पिन साइकिल के दौरान रखने और क्लिक करने जैसे आवाज कर रहा है मैंने इस लगभग २६ महीने पहले खरीदा था",
        "From": test_user
    }, "TEST 1: Voice Complaint (Hindi)")
    assert "Autonomous Diagnostic Report" in res1, "Failed: Voice complaint did not route to Diagnostic Report!"
    
    # TEST 2: Customer Approves
    res2 = _send_webhook({
        "Body": "Approve",
        "From": test_user
    }, "TEST 2: Customer sends 'Approve'")
    assert "Service Confirmed & Escrow Locked" in res2, "Failed: 'Approve' did not route to Service Confirmed!"
    
    # TEST 3: Post-Repair Voice Test (Hindi: 'स्पिन टेस्ट सक्सेसफुल')
    res3 = _send_webhook({
        "Body": "स्पिन टेस्ट सक्सेसफुल",
        "From": test_user
    }, "TEST 3: Post-Repair Voice Test 'स्पिन टेस्ट सक्सेसफुल'")
    assert "Post-Repair Settlement Verdict" in res3, "Failed: Post-repair did not route to Settlement Verdict!"
    
    # TEST 4: Post-Repair Voice Test (Hindi: 'रिपेयर कम्प्लीटेड परफॉर्म दी स्पिन टेस्टिंग नाउ')
    res4 = _send_webhook({
        "Body": "रिपेयर कम्प्लीटेड परफॉर्म दी स्पिन टेस्टिंग नाउ",
        "From": test_user
    }, "TEST 4: Post-Repair Voice Test 'रिपेयर कम्प्लीटेड'")
    assert "Post-Repair Settlement Verdict" in res4, "Failed: Post-repair did not route to Settlement Verdict!"
    
    # TEST 5: English text: 'Spin test'
    res5 = _send_webhook({
        "Body": "Spin test",
        "From": test_user
    }, "TEST 5: English 'Spin test'")
    assert "Post-Repair Settlement Verdict" in res5, "Failed: 'Spin test' did not route to Settlement Verdict!"
    
    # TEST 6: Subsequent complaint resets session back to INTAKE
    res6 = _send_webhook({
        "Body": "My washing machine has a new grinding sound issue",
        "From": test_user
    }, "TEST 6: New complaint resets session to INTAKE")
    assert "Autonomous Diagnostic Report" in res6, "Failed: New complaint did not reset to Diagnostic Report!"
    
    print("\n\nALL 6 DISAMBIGUATION TESTS PASSED PERFECTLY!")
