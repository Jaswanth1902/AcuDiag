"""
AcuDiag Enterprise Multi-Session Incident, Technician & Supervisor Telemetry Store
Manages two-sided WhatsApp messaging (Customer & Technician), chronological audit timelines,
DSP proof envelopes, and Human-in-the-Loop (HITL) Supervisor Overrides.
"""

import time
import copy
import uuid

INITIAL_SESSIONS = {
    "SES_1042_PRIYA": {
        "id": "SES_1042_PRIYA",
        "ticket_no": "1042",
        "customer_name": "Priya Sharma",
        "phone": "+91 98450 11042",
        "location": "Kengeri, Bengaluru 560059",
        "pincode": "560059",
        "appliance": "Godrej 7kg Front-Load",
        "model_no": "Eon Allure GDE-70",
        "fault_name": "Drum Bearing Outer Race Wear (BPFO)",
        "fault_code": "WM_BEARING_SPALL",
        "sku": "BEAR-6205-2RS",
        "state": "VERIFIED_SETTLED",
        "alarm": "NONE",
        "alarm_text": "Zero anomalies. Complete physical repair verified acoustically.",
        "created_at": "10:14:02 IST",
        "last_updated": "11:43:00 IST",
        "cost": {"part": 850, "labor": 400, "total": 1250},
        "technician": {
            "name": "Suresh Kumar",
            "phone": "+91 98450 12345",
            "badge": "Godrej Certified Lead #4012",
            "upi_vpa": "suresh.kumar@okhdfcbank",
            "rating": "4.92 / 5.0"
        },
        "escrow": {
            "order_id": "PL_ORD_8A92B1C4",
            "amount": 1250.0,
            "status": "CAPTURED_SETTLED",
            "provider": "Pine Labs Plural",
            "upi_vpa": "suresh.kumar@okhdfcbank"
        },
        "logistics": {
            "waybill": "DEL16100984210",
            "hub": "Godrej Peenya GW -> BLR_KENGERI_GW",
            "status": "DELIVERED_POD",
            "reverse_docket": "DEL_REV_881920"
        },
        "telemetry": {
            "snr_db": 22.1,
            "snr_status": "CLEAN",
            "peak_freq_hz": 1450.0,
            "lrt_score": 0.38,
            "lrt_threshold": 2.45,
            "lrt_verdict": "PASS",
            "anti_spoofing": "PASSED (Low-Freq Rumble: 34.2 dB, DAC Jitter: 0.04)"
        },
        "supervisor_docket": {
            "docket_id": "DOC_SUP_804",
            "status": "AUTO_RESOLVED_CLEAN",
            "assigned_supervisor": "Inspector R. Sundaram (#804)",
            "notes": "Acoustic kinematics mathematically confirmed. Bearing harmonic eliminated. Auto-capture approved.",
            "override_history": []
        },
        "audit_timeline": [
            {"time": "10:14:02", "event": "Voice Ingested", "detail": "Gnani STT Prisma v2.5 (hi-IN) - Parsed Hinglish drum rattling"},
            {"time": "10:14:28", "event": "Noise Floor Verified", "detail": "SNR 22.1 dB >= 15 dB threshold (Acoustic capture valid)"},
            {"time": "10:15:10", "event": "Kinematic Fault Isolated", "detail": "CWRU 1,450 Hz BPFO harmonic detected (SKF 6205-2RS)"},
            {"time": "10:15:22", "event": "Pine Labs Pre-Auth Locked", "detail": "Order PL_ORD_8A92B1C4 locked ₹1,250.00 escrow hold"},
            {"time": "10:15:35", "event": "Delhivery Part Dispatched", "detail": "Waybill DEL16100984210 manifested from Godrej Peenya Hub"},
            {"time": "10:15:40", "event": "Technician WhatsApp Dispatched", "detail": "Job details & Delhivery tracking sent to Suresh Kumar (+91 98450 12345)"},
            {"time": "11:42:15", "event": "Post-Repair Audio Ingested", "detail": "WebAudio 44.1kHz uncompressed diagnostic stream"},
            {"time": "11:42:20", "event": "Anti-Spoofing Audit Passed", "detail": "Physical motor rumble verified (p_replay = 0.004 < 0.05)"},
            {"time": "11:42:25", "event": "Neyman-Pearson LRT Passed", "detail": "LRT Lambda = 0.38 <= 2.45; 1,450 Hz harmonic eradicated"},
            {"time": "11:42:28", "event": "Escrow Captured & Settled", "detail": "₹1,250.00 released to technician Suresh Kumar via Plural UPI"},
            {"time": "11:42:40", "event": "Delhivery Reverse Scheduled", "detail": "Reverse pickup docket DEL_REV_881920 generated for core recycling"},
            {"time": "11:43:00", "event": "Warranty Digital Token Issued", "detail": "WAR-GODREJ-98214 active for 90 days"}
        ],
        "messages_customer": [
            {"sender": "user", "time": "10:14:02", "text": "Washing machine spin karte waqt drum se ajeeb khat-khat awaz aa rahi hai.", "is_audio": True, "audio_label": "Voice Note (0:04)"},
            {"sender": "agent", "time": "10:14:05", "text": "मैंने आपकी वॉशिंग मशीन का ड्रम खड़-खड़ लक्षण नोट कर लिया है। कृपया फोन को मशीन के पिछले हिस्से के पास 5 सेमी पर रखें।", "is_audio": True, "audio_label": "Gnani Voice Reply (0:05)"},
            {"sender": "agent", "time": "10:15:10", "type": "diagnostic_card", "title": "AcuDiag Diagnostic Report", "appliance": "Godrej 7kg Front-Load", "defect": "Drum Bearing Outer Race Wear (BPFO 1,450 Hz)", "sku": "BEAR-6205-2RS", "cost": "Part ₹850 + Labor ₹400 = Total ₹1,250", "action": "Approve Repair & Lock Escrow"},
            {"sender": "user", "time": "10:15:22", "text": "Approve Repair & Lock Escrow"},
            {"sender": "agent", "time": "10:15:35", "text": "✅ Pine Labs Escrow Locked (₹1,250 held).\n\n• Order ID: PL_ORD_8A92B1C4\n• Delhivery Waybill: DEL16100984210\n• Assigned Tech: Suresh Kumar (+91 98450 12345)\n• ETA: Tomorrow by 11:30 AM\n\nFunds will only be released after you run a 10s post-repair spin test."},
            {"sender": "tech", "time": "11:42:00", "text": "Technician Suresh: Bearing replacement complete. Please start spin cycle for verification test."},
            {"sender": "agent", "time": "11:42:25", "type": "verification_card", "title": "Acoustic Verification: PASSED", "lrt": "0.38 (Threshold 2.45)", "status": "Clean Acoustic Profile", "text": "🎉 Post-repair acoustic check verified! The 1,450 Hz bearing spall peak has been eradicated."},
            {"sender": "agent", "time": "11:42:28", "text": "💰 Pine Labs Escrow Released!\n\n₹1,250.00 settled to technician Suresh Kumar.\n\n📄 90-Day Digital Warranty active: WAR-GODREJ-98214.\nThank you for using AcuDiag! ⭐⭐⭐⭐⭐"}
        ],
        "messages_technician": [
            {"sender": "agent", "time": "10:15:40", "text": "📍 *NEW JOB DISPATCH - ACUDIAG*\n\n• *Customer:* Priya Sharma (+91 98450 11042)\n• *Location:* Kengeri, Bengaluru 560059\n• *Appliance:* Godrej 7kg Front-Load\n• *Issue:* Drum Bearing Spall (SKU: BEAR-6205-2RS)\n• *Escrow Pre-Auth:* ₹1,250 Locked in Pine Labs Plural\n• *Parts Logistics:* Delhivery Waybill DEL16100984210 en route from Peenya Hub."},
            {"sender": "tech", "time": "11:15:00", "text": "Suresh: Reached customer location. Delhivery part received and seal inspected. Opening drum assembly now."},
            {"sender": "tech", "time": "11:41:30", "text": "Suresh: Old bearing removed. New OEM Godrej bearing seated and torqued. Starting verification spin test."},
            {"sender": "agent", "time": "11:42:25", "text": "✅ *ACOUSTIC TEST VERIFIED (PASS)*\n\n• Neyman-Pearson LRT: 0.38 <= 2.45\n• Anti-Spoofing: Verified Physical Motor Rumble"},
            {"sender": "agent", "time": "11:42:28", "text": "💰 *ESCROW PAYOUT RELEASED*\n\n₹1,250.00 settled to your UPI: `suresh.kumar@okhdfcbank`\n\n📦 *Reverse Pickup Mandatory:* Please place old defective bearing in Delhivery Return Bag. Docket: `DEL_REV_881920`."}
        ]
    },
    "SES_1043_VIKRAM": {
        "id": "SES_1043_VIKRAM",
        "ticket_no": "1043",
        "customer_name": "Vikram Singh",
        "phone": "+91 98110 44219",
        "location": "Saket, New Delhi 110017",
        "pincode": "110017",
        "appliance": "LG 1.5 Ton Dual Inverter AC",
        "model_no": "MS-Q18HNZA",
        "fault_name": "Compressor Discharge Valve Leak & Cavitation",
        "fault_code": "AC_COMPRESSOR_LEAK",
        "sku": "VALVE-LG-4011",
        "state": "AWAITING_APPROVAL",
        "alarm": "QUOTE_DECLINED",
        "alarm_text": "🚨 User declined ₹4,600 repair quote. Escrow hold cancelled. Zero funds charged.",
        "created_at": "11:18:10 IST",
        "last_updated": "11:20:18 IST",
        "cost": {"part": 3600, "labor": 1000, "total": 4600},
        "technician": {
            "name": "Unassigned",
            "phone": "N/A",
            "badge": "LG Certified Network",
            "upi_vpa": "N/A",
            "rating": "N/A"
        },
        "escrow": {
            "order_id": "PL_ORD_CANCELLED",
            "amount": 4600.0,
            "status": "UNBOOKED_CANCELLED",
            "provider": "Pine Labs Plural",
            "technician": "None Assigned"
        },
        "logistics": {
            "waybill": "UNMANIFESTED",
            "hub": "DEL_OKHLA_GW",
            "status": "NOT_DISPATCHED",
            "reverse_docket": "N/A"
        },
        "telemetry": {
            "snr_db": 19.4,
            "snr_status": "CLEAN",
            "peak_freq_hz": 3200.0,
            "lrt_score": 6.84,
            "lrt_threshold": 2.45,
            "lrt_verdict": "FAIL",
            "anti_spoofing": "PASSED"
        },
        "supervisor_docket": {
            "docket_id": "DOC_SUP_811",
            "status": "CUSTOMER_DECLINED_ARCHIVED",
            "assigned_supervisor": "Inspector R. Sundaram (#804)",
            "notes": "High quote (₹4,600) rejected by customer. Zero escrow locked. Ticket retained in CRM for 30 days.",
            "override_history": []
        },
        "audit_timeline": [
            {"time": "11:18:10", "event": "Symptom Ingested", "detail": "User reported loud whistling hiss from outdoor AC unit"},
            {"time": "11:19:00", "event": "Spectral Fault Match", "detail": "High-frequency refrigerant cavitation detected at 3,200 Hz"},
            {"time": "11:19:02", "event": "Quote Generated", "detail": "OEM Valve ₹3,600 + Labor ₹1,000 = Total ₹4,600"},
            {"time": "11:20:15", "event": "User Declined Quote", "detail": "User replied: 'Nahi bhai, ₹4,600 bohot zyada hai. Abhi repair nahi karana.'"},
            {"time": "11:20:18", "event": "Workflow Gracefully Paused", "detail": "System Prompt Invariant: Do not charge card. Diagnostic dossier archived."}
        ],
        "messages_customer": [
            {"sender": "user", "time": "11:18:10", "text": "AC outdoor unit se continuous hiss aur whistling sound aa rahi hai, cooling bilkul band hai."},
            {"sender": "agent", "time": "11:19:00", "type": "diagnostic_card", "title": "AcuDiag Diagnostic Report", "appliance": "LG Dual Inverter AC", "defect": "Compressor Discharge Valve Cavitation (3,200 Hz)", "sku": "VALVE-LG-4011", "cost": "Part ₹3,600 + Labor ₹1,000 = Total ₹4,600", "action": "Approve Repair & Lock Escrow"},
            {"sender": "user", "time": "11:20:15", "text": "Nahi bhai, ₹4,600 bohot zyada hai. Abhi repair nahi karana."},
            {"sender": "agent", "time": "11:20:18", "text": "समझ गया विक्रम जी। रिपेयर रोक दी गई है।\n\nआपके बैंक या कार्ड से कोई शुल्क नहीं काटा गया है। आपकी डायग्नोस्टिक रिपोर्ट 30 दिनों तक सुरक्षित है यदि आप बाद में रिपेयर कराना चाहें। धन्यवाद!"}
        ],
        "messages_technician": [
            {"sender": "agent", "time": "11:20:19", "text": "ℹ️ Job allocation cancelled. Customer Vikram Singh declined quote prior to dispatch."}
        ]
    },
    "SES_1044_ANANYA": {
        "id": "SES_1044_ANANYA",
        "ticket_no": "1044",
        "customer_name": "Ananya Patel",
        "phone": "+91 97412 88310",
        "location": "Whitefield, Bengaluru 560066",
        "pincode": "560066",
        "appliance": "Samsung 6.5kg Wobble Top-Load",
        "model_no": "WA65T4262",
        "fault_name": "Suspension Damper Rod Fatigue",
        "fault_code": "SUSPENSION_FAIL",
        "sku": "DAMP-SAM-4X",
        "state": "AWAITING_RETRY",
        "alarm": "LOW_SNR_ALERT",
        "alarm_text": "🚨 Kitchen noise interference (SNR 9.4 dB < 15 dB). Test rejected to prevent false fault diagnosis.",
        "created_at": "11:44:02 IST",
        "last_updated": "11:44:08 IST",
        "cost": {"part": 450, "labor": 300, "total": 750},
        "technician": {
            "name": "Pending Intake",
            "phone": "N/A",
            "badge": "Samsung Care Lead",
            "upi_vpa": "N/A",
            "rating": "N/A"
        },
        "escrow": {
            "order_id": "PENDING_VALIDATION",
            "amount": 750.0,
            "status": "AWAITING_CLEAN_AUDIO",
            "provider": "Pine Labs Plural",
            "technician": "Pending Assignment"
        },
        "logistics": {
            "waybill": "PENDING",
            "hub": "BLR_WHITEFIELD_GW",
            "status": "ON_HOLD",
            "reverse_docket": "N/A"
        },
        "telemetry": {
            "snr_db": 9.4,
            "snr_status": "REJECTED_LOW_SNR",
            "peak_freq_hz": 2400.0,
            "lrt_score": 0.0,
            "lrt_threshold": 2.45,
            "lrt_verdict": "BLOCKED_BY_NOISE",
            "anti_spoofing": "NOT_EVALUATED"
        },
        "supervisor_docket": {
            "docket_id": "DOC_SUP_819",
            "status": "GATING_ACTIVE",
            "assigned_supervisor": "Inspector R. Sundaram (#804)",
            "notes": "Low SNR (9.4 dB) caught by Rule 3 noise floor filter. No false dispatch triggered.",
            "override_history": []
        },
        "audit_timeline": [
            {"time": "11:44:02", "event": "Audio Sample Uploaded", "detail": "User submitted 4s clip of vibrating machine"},
            {"time": "11:44:06", "event": "Noise Floor Evaluation", "detail": "Background pressure cooker whistle measuring 68 dB SPL (Machine: 65 dB SPL)"},
            {"time": "11:44:08", "event": "SNR Gating Enforced", "detail": "Rule 3 Triggered: SNR 9.4 dB < 15 dB threshold. Classification aborted to avoid false positive."}
        ],
        "messages_customer": [
            {"sender": "user", "time": "11:44:02", "text": "[Audio recording with loud pressure cooker whistle whistling in kitchen]", "is_audio": True, "audio_label": "Kitchen Recording (0:04)"},
            {"sender": "agent", "time": "11:44:08", "text": "⚠️ *आस-पास का शोर बहुत अधिक है (SNR 9.4 dB)*\n\nकिचन के प्रेशर कुकर की सीटी का शोर मशीन की आवाज़ को दबा रहा है। गलत डायग्नोसिस से बचने के लिए हमने टेस्ट रोक दिया है।\n\n👉 कृपया किचन का दरवाज़ा बंद करें और 5 सेकंड की नई रिकॉर्डिंग भेजें।"}
        ],
        "messages_technician": [
            {"sender": "agent", "time": "11:44:09", "text": "ℹ️ Technician dispatch held pending user clean acoustic re-submission."}
        ]
    },
    "SES_1045_RAJESH": {
        "id": "SES_1045_RAJESH",
        "ticket_no": "1045",
        "customer_name": "Rajesh Kumar",
        "phone": "+91 99001 77234",
        "location": "Andheri West, Mumbai 400058",
        "pincode": "400058",
        "appliance": "Whirlpool 260L Frost-Free Fridge",
        "model_no": "IF-INV-278",
        "fault_name": "Capillary Expansion Valve Whistle",
        "fault_code": "REFRIGERANT_VALVE",
        "sku": "VALVE-WP-260",
        "state": "REPAIR_REJECTED",
        "alarm": "REPLAY_SPOOF_BLOCKED",
        "alarm_text": "🚨 FRAUD DETECTED: Technician played canned audio via phone speaker (DAC spike, low rumble absent). Escrow LOCKED.",
        "created_at": "12:05:00 IST",
        "last_updated": "12:08:20 IST",
        "cost": {"part": 700, "labor": 400, "total": 1100},
        "technician": {
            "name": "Dinesh Patil",
            "phone": "+91 98200 44321",
            "badge": "Mumbai Contractor #918",
            "upi_vpa": "dinesh.patil@icici",
            "rating": "3.80 / 5.0 (FLAGGED)"
        },
        "escrow": {
            "order_id": "PL_ORD_7719B021",
            "amount": 1100.0,
            "status": "LOCKED_FRAUD_HOLD",
            "provider": "Pine Labs Plural",
            "technician": "Dinesh Patil (+91 98200 44321)"
        },
        "logistics": {
            "waybill": "DEL9921440182",
            "hub": "BOM_ANDHERI_GW",
            "status": "DELIVERED",
            "reverse_docket": "PENDING"
        },
        "telemetry": {
            "snr_db": 24.5,
            "snr_status": "CLEAN",
            "peak_freq_hz": 120.0,
            "lrt_score": 0.42,
            "lrt_threshold": 2.45,
            "lrt_verdict": "BLOCKED_BY_SPOOF",
            "anti_spoofing": "FAILED (p_replay = 0.98 > 0.05, Low-Freq Energy: 2.1 dB < 15 dB)"
        },
        "supervisor_docket": {
            "docket_id": "DOC_SUP_822",
            "status": "SUPERVISOR_ACTION_REQUIRED",
            "assigned_supervisor": "Inspector R. Sundaram (#804)",
            "notes": "Acoustic spectrum indicates high DAC jitter at 16kHz from phone loudspeaker. Low-frequency motor vibration absent. Payout frozen. Supervisor action required.",
            "override_history": []
        },
        "audit_timeline": [
            {"time": "12:05:00", "event": "Ticket Initialized", "detail": "Refrigerant valve noise reported; pre-auth ₹1,100 locked"},
            {"time": "12:08:10", "event": "Technician Claimed Repair", "detail": "Technician Dinesh Patil submitted audio test"},
            {"time": "12:08:18", "event": "Anti-Spoofing Audit", "detail": "Spectral analysis revealed 16kHz DAC quantization harmonic; physical motor rumble absent (<120Hz = 2.1 dB)"},
            {"time": "12:08:20", "event": "Replay Fraud Blocked", "detail": "Rule 4 Enforced: Payout withheld. Technician flagged in Pine Labs merchant risk ledger."},
            {"time": "12:08:25", "event": "Supervisor Escalation Docket Issued", "detail": "Docket DOC_SUP_822 assigned to Inspector R. Sundaram (#804)"}
        ],
        "messages_customer": [
            {"sender": "agent", "time": "12:08:20", "text": "🚨 *सुरक्षा चेतावनी (FRAUD ALERT)*\n\nतकनीशियन द्वारा सबमिट किया गया टेस्ट ऑडियो अमान्य पाया गया है (मोबाइल स्पीकर से प्लेबैक का संदेह)।\n\nआपके ₹1,100 एस्क्रो में पूरी तरह सुरक्षित हैं। जब तक AcuDiag क्वालिटी सुपरवाइजर जांच पूरी नहीं करते, भुगतान जारी नहीं किया जाएगा।"}
        ],
        "messages_technician": [
            {"sender": "agent", "time": "12:05:00", "text": "📍 *JOB DISPATCH:* Whirlpool 260L (Refrigerant Valve). Customer: Rajesh Kumar, Andheri West. Escrow: ₹1,100."},
            {"sender": "tech", "time": "12:08:10", "text": "Dinesh: Valve replace ho gaya. Audio recording bhej raha hoon verification ke liye.", "is_audio": True, "audio_label": "Submitted Audio (0:05)"},
            {"sender": "agent", "time": "12:08:20", "text": "🚨 *FRAUD ALERT: REPLAY ATTACK DETECTED*\n\nसबमिट किया गया ऑडियो मोबाइल लाउडस्पीकर से बजाया गया है (DAC क्वांटाइजेशन 16kHz, वास्तविक मोटर कंपन गायब)।\n\n• पाइन लैब्स एस्क्रो भुगतान (₹1,100) रोक दिया गया है।\n• तकनीशियन दिनेश पाटिल की जांच सुपरवाइजर डॉकेट DOC_SUP_822 में दर्ज है।"},
            {"sender": "tech", "time": "12:08:45", "text": "Dinesh: Sir galti se purana clip chala gaya tha, main genuine spin test karta hoon."}
        ]
    },
    "SES_1046_AMIT": {
        "id": "SES_1046_AMIT",
        "ticket_no": "1046",
        "customer_name": "Amit Verma",
        "phone": "+91 98860 33912",
        "location": "Indiranagar, Bengaluru 560038",
        "pincode": "560038",
        "appliance": "Bosch Series 6 Front-Load",
        "model_no": "WAT28461IN",
        "fault_name": "Drain Pump Impeller Cavitation",
        "fault_code": "DRAIN_PUMP_BLOCK",
        "sku": "PUMP-BOSCH-SER6",
        "state": "ESCROW_LOCKED_AUDIT",
        "alarm": "FAKE_REPAIR_LOCKED",
        "alarm_text": "🚨 Incomplete repair: 820 Hz impeller screech harmonic still present (LRT 8.42 > 2.45). Escrow LOCKED.",
        "created_at": "12:35:00 IST",
        "last_updated": "12:39:00 IST",
        "cost": {"part": 600, "labor": 400, "total": 1000},
        "technician": {
            "name": "Manoj Tiwari",
            "phone": "+91 98455 66778",
            "badge": "Bosch Regional Tech #302",
            "upi_vpa": "manoj.tiwari@paytm",
            "rating": "4.10 / 5.0"
        },
        "escrow": {
            "order_id": "PL_ORD_4491A882",
            "amount": 1000.0,
            "status": "ESCROW_LOCKED_FAILED_TEST",
            "provider": "Pine Labs Plural",
            "technician": "Manoj Tiwari (+91 98455 66778)"
        },
        "logistics": {
            "waybill": "DEL8821094412",
            "hub": "BLR_INDIRANAGAR_GW",
            "status": "DELIVERED",
            "reverse_docket": "PENDING"
        },
        "telemetry": {
            "snr_db": 21.0,
            "snr_status": "CLEAN",
            "peak_freq_hz": 820.0,
            "lrt_score": 8.42,
            "lrt_threshold": 2.45,
            "lrt_verdict": "FAIL",
            "anti_spoofing": "PASSED"
        },
        "supervisor_docket": {
            "docket_id": "DOC_SUP_826",
            "status": "SUPERVISOR_ACTION_REQUIRED",
            "assigned_supervisor": "Inspector R. Sundaram (#804)",
            "notes": "Drain pump impeller screech harmonic persists at 820 Hz (LRT Lambda 8.42). Repair is physically incomplete. Escrow withheld. Supervisor override available.",
            "override_history": []
        },
        "audit_timeline": [
            {"time": "12:35:00", "event": "Ticket Initialized", "detail": "Drain pump cavitation screech reported; ₹1,000 escrow pre-auth locked"},
            {"time": "12:38:15", "event": "Technician Claimed Repair", "detail": "Technician Manoj claimed: 'Pump cleared and tightened. Job done.'"},
            {"time": "12:38:50", "event": "Neyman-Pearson LRT Executed", "detail": "Post-repair test audio revealed persistent 820 Hz screech peak (LRT Lambda = 8.42 > 2.45)"},
            {"time": "12:39:00", "event": "Fake Repair Blocked", "detail": "Rule 6 Enforced: KEEP ESCROW LOCKED. Payout withheld. Scheduling secondary supervisor."},
            {"time": "12:39:05", "event": "Supervisor Escalation Docket Issued", "detail": "Docket DOC_SUP_826 assigned to Inspector R. Sundaram (#804)"}
        ],
        "messages_customer": [
            {"sender": "agent", "time": "12:39:00", "type": "verification_card", "title": "Verification FAILED: Defect Still Present", "lrt": "8.42 (Threshold 2.45)", "status": "FAIL - Impeller Screech Active", "text": "❌ Acoustic verification FAILED. The 820 Hz drain pump cavitation screech is still present."},
            {"sender": "agent", "time": "12:39:05", "text": "⚠️ *PINE LABS ESCROW LOCKED*\n\nरिपेयर अधूरा पाया गया है। ₹1,000 का भुगतान रोक दिया गया है। सुपरवाइजर रिव्यू डॉकेट DOC_SUP_826 सक्रिय है।"}
        ],
        "messages_technician": [
            {"sender": "agent", "time": "12:35:00", "text": "📍 *JOB DISPATCH:* Bosch Series 6 (Drain Pump). Customer: Amit Verma, Indiranagar. Escrow: ₹1,000."},
            {"sender": "tech", "time": "12:38:15", "text": "Manoj: Pump cleared and tightened. Job done. Please release payment."},
            {"sender": "agent", "time": "12:39:00", "text": "❌ *VERIFICATION FAILED: HARMONIC ACTIVE*\n\n• 820 Hz cavitation screech अभी भी सक्रिय है (LRT Lambda: 8.42 > 2.45)।\n• भुगतान रोक दिया गया है। डॉकेट DOC_SUP_826 सुपरवाइजर को भेजा गया है।"},
            {"sender": "tech", "time": "12:39:25", "text": "Manoj: Sir customer was in a hurry, I will disassemble and replace the complete impeller assembly."}
        ]
    },
    "SES_1047_SUNITA": {
        "id": "SES_1047_SUNITA",
        "ticket_no": "1047",
        "customer_name": "Sunita Rao",
        "phone": "+91 94480 55123",
        "location": "Malleshwaram, Bengaluru 560003",
        "pincode": "560003",
        "appliance": "IFB Senator 8kg Smart",
        "model_no": "Senator Smart SX",
        "fault_name": "Motor Tachometer Hall Sensor Failure",
        "fault_code": "MOTOR_TACHO_FAIL",
        "sku": "TACHO-IFB-SEN8",
        "state": "CAPTURED_SETTLED",
        "alarm": "BANK_TIMEOUT_IDEMPOTENT",
        "alarm_text": "⚠️ Pine Labs 504 Gateway Timeout recovered via SHA-256 idempotency key. Zero duplicate billing.",
        "created_at": "13:10:00 IST",
        "last_updated": "13:12:30 IST",
        "cost": {"part": 1150, "labor": 400, "total": 1550},
        "technician": {
            "name": "Ramesh Kumar",
            "phone": "+91 98450 77112",
            "badge": "IFB Senior Tech #108",
            "upi_vpa": "ramesh.k@okaxis",
            "rating": "4.85 / 5.0"
        },
        "escrow": {
            "order_id": "PL_ORD_9921D304",
            "amount": 1550.0,
            "status": "CAPTURED_SETTLED",
            "provider": "Pine Labs Plural",
            "technician": "Ramesh Kumar (+91 98450 77112)",
            "idempotency_key": "SHA256_PL_TXN_99214D"
        },
        "logistics": {
            "waybill": "DEL771920441",
            "hub": "BLR_MALLESHWARAM_GW",
            "status": "DELIVERED_POD",
            "reverse_docket": "DEL_REV_33190"
        },
        "telemetry": {
            "snr_db": 23.0,
            "snr_status": "CLEAN",
            "peak_freq_hz": 404.5,
            "lrt_score": 0.29,
            "lrt_threshold": 2.45,
            "lrt_verdict": "PASS",
            "anti_spoofing": "PASSED"
        },
        "supervisor_docket": {
            "docket_id": "DOC_SUP_830",
            "status": "AUTO_RECOVERED",
            "assigned_supervisor": "Inspector R. Sundaram (#804)",
            "notes": "504 Gateway Timeout intercepted and resolved via idempotency key without supervisor intervention.",
            "override_history": []
        },
        "audit_timeline": [
            {"time": "13:10:00", "event": "Ticket Initialized", "detail": "IFB motor speed hunting reported; ₹1,550 escrow hold created"},
            {"time": "13:12:10", "event": "Post-Repair Test PASSED", "detail": "Tacho signal locked cleanly; LRT 0.29 <= 2.45"},
            {"time": "13:12:22", "event": "Pine Labs 504 Timeout Caught", "detail": "Bank switch timed out during capture call"},
            {"time": "13:12:25", "event": "Idempotency Protection Enforced", "detail": "Rule 7 Enforced: Did not retry duplicate debit. Queued SHA-256 idempotency key."},
            {"time": "13:12:30", "event": "Webhook Settlement Confirmed", "detail": "Plural webhook confirmed settlement; ₹1,550 settled cleanly to Ramesh Kumar."}
        ],
        "messages_customer": [
            {"sender": "user", "time": "13:12:10", "text": "Spin test chal gaya, tacho sensor replaced."},
            {"sender": "agent", "time": "13:12:20", "text": "✅ Acoustic & Motor test verified! Releasing escrow..."},
            {"sender": "agent", "time": "13:12:25", "text": "⚠️ Upstream bank switch timed out (504). AcuDiag Idempotency Protection engaged.\n\nTransaction key verified with Plural. Zero duplicate charge."},
            {"sender": "agent", "time": "13:12:30", "text": "💰 Settlement Confirmed: ₹1,550 released to technician Ramesh Kumar. 90-Day Warranty active."}
        ],
        "messages_technician": [
            {"sender": "agent", "time": "13:10:00", "text": "📍 *JOB DISPATCH:* IFB Senator 8kg (Motor Tacho). Customer: Sunita Rao. Escrow: ₹1,550."},
            {"sender": "tech", "time": "13:12:10", "text": "Ramesh: Tacho replaced. Spin test initiated."},
            {"sender": "agent", "time": "13:12:30", "text": "💰 *SETTLEMENT CONFIRMED:* ₹1,550 credited to your UPI: `ramesh.k@okaxis`. Bank timeout resolved idempotently."}
        ]
    }
}

# Attach backward-compatible "messages" key referencing messages_customer
for s in INITIAL_SESSIONS.values():
    s["messages"] = s["messages_customer"]

# In-memory working copy
SESSIONS = copy.deepcopy(INITIAL_SESSIONS)

def get_all_sessions_summary():
    """Returns summary list of all sessions for the Incident Inbox queue."""
    summaries = []
    for s_id, s in SESSIONS.items():
        last_cust_msg = s["messages_customer"][-1]["text"] if s.get("messages_customer") else ""
        last_tech_msg = s["messages_technician"][-1]["text"] if s.get("messages_technician") else ""
        summaries.append({
            "id": s["id"],
            "ticket_no": s["ticket_no"],
            "customer_name": s["customer_name"],
            "phone": s["phone"],
            "location": s["location"],
            "appliance": s["appliance"],
            "fault_name": s["fault_name"],
            "fault_code": s["fault_code"],
            "state": s["state"],
            "alarm": s["alarm"],
            "alarm_text": s["alarm_text"],
            "cost_total": s["cost"]["total"],
            "technician_name": s["technician"]["name"],
            "supervisor_status": s["supervisor_docket"]["status"],
            "supervisor_docket_id": s["supervisor_docket"]["docket_id"],
            "last_updated": s["last_updated"],
            "last_message": last_cust_msg[:75] + ("..." if len(last_cust_msg) > 75 else ""),
            "last_tech_message": last_tech_msg[:75] + ("..." if len(last_tech_msg) > 75 else "")
        })
    return summaries

def get_session(session_id: str):
    """Returns complete session envelope by ID."""
    session = SESSIONS.get(session_id)
    if session and "messages" not in session:
        session["messages"] = session.get("messages_customer", [])
    return session

def add_user_message(session_id: str, text: str, sender: str = "user", channel: str = "customer"):
    """Appends message to customer or technician stream and triggers reactive agent logic."""
    session = SESSIONS.get(session_id)
    if not session:
        return None

    curr_time = time.strftime("%H:%M:%S IST")
    session["last_updated"] = curr_time

    target_stream = "messages_technician" if channel == "technician" else "messages_customer"
    session[target_stream].append({
        "sender": sender,
        "time": curr_time,
        "text": text
    })

    # Keep backward-compatible pointer
    session["messages"] = session["messages_customer"]

    # Reactive Agent Logic
    b_lower = text.lower()
    if channel == "customer":
        if any(k in b_lower for k in ["nahi", "no", "cancel", "expensive", "mehenga", "decline"]):
            session["state"] = "AWAITING_APPROVAL"
            session["alarm"] = "QUOTE_DECLINED"
            session["alarm_text"] = "🚨 User declined quote. Escrow hold cancelled. Zero funds debited."
            session["escrow"]["status"] = "UNBOOKED_CANCELLED"
            session["audit_timeline"].append({
                "time": curr_time,
                "event": "Quote Declined by User",
                "detail": f"User cancelled repair: '{text}'. Escrow pre-auth released."
            })
            session["messages_customer"].append({
                "sender": "agent",
                "time": curr_time,
                "text": "समझ गया। रिपेयर रोक दी गई है। आपके खाते से कोई राशि नहीं काटी गई है।"
            })
            session["messages_technician"].append({
                "sender": "agent",
                "time": curr_time,
                "text": "ℹ️ Job cancelled. Customer declined repair quote."
            })
        elif any(k in b_lower for k in ["approve", "lock", "yes", "ha", "haan", "theek", "ok", "proceed"]):
            order_id = f"PL_ORD_{uuid.uuid4().hex[:8].upper()}"
            waybill = f"DEL{int(time.time()) % 10000000:08d}"
            session["state"] = "PARTS_DISPATCHED"
            session["alarm"] = "NONE"
            session["escrow"]["order_id"] = order_id
            session["escrow"]["status"] = "PRE_AUTH_LOCKED"
            session["logistics"]["waybill"] = waybill
            session["logistics"]["status"] = "MANIFESTED_IN_TRANSIT"
            session["audit_timeline"].append({
                "time": curr_time,
                "event": "Escrow Pre-Auth Locked",
                "detail": f"Order {order_id} locked ₹{session['cost']['total']} hold"
            })
            session["messages_customer"].append({
                "sender": "agent",
                "time": curr_time,
                "text": f"✅ Pine Labs Escrow Locked (₹{session['cost']['total']} held).\n• Order ID: {order_id}\n• Delhivery Waybill: {waybill}"
            })
            session["messages_technician"].append({
                "sender": "agent",
                "time": curr_time,
                "text": f"📍 Job active! Delhivery OEM parts dispatched (Waybill: {waybill})."
            })
        elif any(k in b_lower for k in ["spin", "test", "done", "fixed", "verify"]):
            session["state"] = "VERIFIED_SETTLED"
            session["alarm"] = "NONE"
            session["escrow"]["status"] = "CAPTURED_SETTLED"
            session["telemetry"]["lrt_score"] = 0.35
            session["telemetry"]["lrt_verdict"] = "PASS"
            session["audit_timeline"].append({
                "time": curr_time,
                "event": "Post-Repair Acoustic Verified",
                "detail": "Neyman-Pearson LRT = 0.35 <= 2.45. Harmonics eradicated."
            })
            session["messages_customer"].append({
                "sender": "agent",
                "time": curr_time,
                "text": f"💰 Pine Labs Escrow Released! ₹{session['cost']['total']} settled to technician."
            })
            session["messages_technician"].append({
                "sender": "agent",
                "time": curr_time,
                "text": f"💰 Payout Released! ₹{session['cost']['total']} settled to your UPI account."
            })

    elif channel == "technician":
        session["audit_timeline"].append({
            "time": curr_time,
            "event": "Technician Message Received",
            "detail": f"{session['technician']['name']}: {text}"
        })
        session["messages_technician"].append({
            "sender": "agent",
            "time": curr_time,
            "text": f"AcuDiag System noted technician update: '{text}'."
        })

    return session

def execute_supervisor_override(session_id: str, action: str, reason: str = ""):
    """Executes a formal Human-in-the-Loop Quality Supervisor override."""
    session = SESSIONS.get(session_id)
    if not session:
        return None

    curr_time = time.strftime("%H:%M:%S IST")
    session["last_updated"] = curr_time
    docket = session["supervisor_docket"]
    supervisor = docket.get("assigned_supervisor", "Inspector R. Sundaram (#804)")

    override_record = {
        "time": curr_time,
        "action": action,
        "supervisor": supervisor,
        "reason": reason or "Supervisor quality review executed."
    }
    docket["override_history"].append(override_record)

    if action == "UPHOLD_FRAUD_LOCK":
        docket["status"] = "UPHELD_FRAUD_LOCK"
        session["state"] = "SUPERVISOR_UPHELD_FRAUD"
        session["alarm"] = "REPLAY_SPOOF_BLOCKED"
        session["alarm_text"] = "🛡️ SUPERVISOR VERDICT: Fraud upheld. Contractor blacklisted. Customer card refunded."
        session["escrow"]["status"] = "FORFEITED_FRAUD_LOCKED"
        session["audit_timeline"].append({
            "time": curr_time,
            "event": "Supervisor Override: Fraud Upheld",
            "detail": f"{supervisor} verified DAC speaker replay. Tech penalized. Full refund queued."
        })
        session["messages_customer"].append({
            "sender": "agent",
            "time": curr_time,
            "text": f"🛡️ *सुपरवाइजर फैसला ({supervisor})*\n\nतकनीशियन द्वारा धोखाधड़ी की पुष्टि हुई है। आपका ₹{session['cost']['total']} एस्क्रो रिफंड प्रोसेस किया जा रहा है। नया सीनियर तकनीशियन मुफ्त में भेजा जा रहा है।"
        })
        session["messages_technician"].append({
            "sender": "agent",
            "time": curr_time,
            "text": f"🚫 *SUPERVISOR OVERRIDE ({supervisor})*\n\nReplay fraud audit UPHELD. Payout cancelled. Contractor ID flagged with Pine Labs Risk Registry."
        })

    elif action == "DISPATCH_SENIOR_TECH":
        docket["status"] = "SENIOR_TECH_RE_DISPATCHED"
        session["state"] = "RE_DISPATCHED_SENIOR_TECH"
        new_waybill = f"DEL_SR_{int(time.time()) % 10000000:08d}"
        session["logistics"]["waybill"] = new_waybill
        session["technician"]["name"] = "R. Sundaram (Quality Lead)"
        session["audit_timeline"].append({
            "time": curr_time,
            "event": "Supervisor Override: Senior Tech Re-Dispatched",
            "detail": f"{supervisor} assigned Master Technician. Replacement waybill: {new_waybill} (Zero customer charge)."
        })
        session["messages_customer"].append({
            "sender": "agent",
            "time": curr_time,
            "text": f"🔧 *सुपरवाइजर फैसला ({supervisor})*\n\nअधूरे काम के कारण सीनियर मास्टर तकनीशियन नियुक्त किया गया है (Waybill: {new_waybill})। आपसे कोई अतिरिक्त शुल्क नहीं लिया जाएगा।"
        })
        session["messages_technician"].append({
            "sender": "agent",
            "time": curr_time,
            "text": f"ℹ️ Ticket re-assigned to Senior Quality Lead {supervisor}. Contractor ticket closed."
        })

    elif action == "RELEASE_CUSTOMER_REFUND":
        docket["status"] = "CUSTOMER_REFUND_COMPLETED"
        session["state"] = "CUSTOMER_REFUNDED"
        session["escrow"]["status"] = "REFUNDED_TO_CUSTOMER"
        session["audit_timeline"].append({
            "time": curr_time,
            "event": "Supervisor Override: Full Escrow Refund",
            "detail": f"{supervisor} authorized 100% refund of ₹{session['cost']['total']} via Pine Labs Plural API."
        })
        session["messages_customer"].append({
            "sender": "agent",
            "time": curr_time,
            "text": f"💳 *एस्क्रो रिफंड पूरा हुआ*\n\nसुपरवाइजर {supervisor} द्वारा ₹{session['cost']['total']} आपके बैंक खाते में वापस भेज दिया गया है।"
        })

    return session

def reset_all_sessions():
    """Resets working sessions to initial baseline."""
    global SESSIONS
    SESSIONS = copy.deepcopy(INITIAL_SESSIONS)
    return True
