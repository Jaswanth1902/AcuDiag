# 📱 Real WhatsApp User Testing Setup Guide

> **Target**: Physical Phone WhatsApp Testing (You or Teammate as "The User")  
> **Compliance**: Mandated by The Ken Round 3 Rules (*"Every other connector must be the real tool... A team member can play the user on the other end."*)

---

## 🎯 How It Works in Physical Reality

```
┌─────────────────────────────────┐
│ YOUR / FRIEND'S PHONE           │
│ (Real WhatsApp App)             │
└────────────────┬────────────────┘
                 │ 1. Voice Note / Text ("Machine se awaz aa rahi hai")
                 ▼
┌─────────────────────────────────┐
│ Twilio / Meta WhatsApp Gateway  │ (Official Public Number)
└────────────────┬────────────────┘
                 │ 2. Webhook POST to Public HTTPS Tunnel
                 ▼
┌─────────────────────────────────┐
│ AcuDiag Mock Server             │ (http://127.0.0.1:8000/api/whatsapp/webhook)
│ • Gnani STT + Butterworth DSP   │
│ • Pine Labs Escrow Hold (₹1,250)│
│ • Delhivery CMU Dispatch        │
└────────────────┬────────────────┘
                 │ 3. Automated WhatsApp Reply
                 ▼
┌─────────────────────────────────┐
│ YOUR / FRIEND'S PHONE           │
│ "⚠️ Fault: Drum Bearing Spall.  │
│  Quote: ₹1,250. Reply APPROVE"  │
└─────────────────────────────────┘
```

---

## 🚀 3-Step Setup for Live Phone WhatsApp Testing

### Step 1: Expose Your Local Server to Public HTTPS
WhatsApp servers cannot talk to `localhost:8000` directly. You need a public HTTPS tunnel.
Run our tunnel script:
```powershell
python 01_Projects/AcuDiag/scripts/start_tunnel.py
```
*Note your public URL*, e.g.: `https://acudiag-live.ngrok-free.app` or `https://xxxx.trycloudflare.com`.

---

### Step 2: Configure Twilio WhatsApp Sandbox (Free & Instant)
1. Go to your Twilio Console $\rightarrow$ **Messaging** $\rightarrow$ **Try it out** $\rightarrow$ **Send a WhatsApp message**.
2. Under **Sandbox Settings** $\rightarrow$ **"When a message comes in"**:
   - Set URL to: `https://<YOUR_TUNNEL_URL>/api/whatsapp/webhook`
   - Method: `HTTP POST`
   - Click **Save**.

---

### Step 3: Test From Your Phone's WhatsApp!
1. **Join Sandbox**: Open WhatsApp on your phone and send the join code (e.g., `join silver-fox`) to the Twilio number (`+1 415 523 8886`).
2. **Send Audio / Message**:
   - Send text: *"Washing machine spin karte waqt ajeeb awaz aa rahi hai"*
   - Or hold the mic button in WhatsApp and send a 4-second audio note!
3. **Receive Diagnosis**:
   - AcuDiag replies instantly on your WhatsApp with:
     ```text
     ⚠️ AcuDiag Diagnostic Report:
     • Appliance: Godrej 7kg Front-Load
     • Defect: Drum Bearing Outer Race Wear (BPFO 1,450 Hz)
     • Quote: Part ₹850 + Labor ₹400 = Total ₹1,250
     👉 Reply APPROVE to lock ₹1,250 in Pine Labs Escrow & dispatch Delhivery OEM parts.
     ```
4. **Approve Escrow**:
   - Reply: *"APPROVE"*
   - AcuDiag responds with:
     ```text
     ✅ Escrow Locked & Dispatched!
     • Pine Labs Order: PL_ORD_XXXXXXXX (₹1,250 held)
     • Delhivery Waybill: DELXXXXXXXX
     • Assigned Tech: Suresh Kumar (+91 98450 12345)
     • ETA: Tomorrow by 11:30 AM
     ```
5. **Run Post-Repair Verification**:
   - Send text: *"Post-repair spin test done"*
   - AcuDiag responds with:
     ```text
     🎉 Acoustic Repair Verified!
     • Neyman-Pearson LRT: 0.02 (PASS)
     • Pine Labs Escrow: ₹1,250 Released to Suresh Kumar
     • Warranty: 90-Day Digital Protection Issued
     ```

---

## ⚡ Alternative: Zero-Config Telegram Option
If you don't have a Twilio account, The Ken explicitly permits Telegram:
> *"Every other connector must be the real tool. WhatsApp, Telegram, Gmail..."*
You can create a Telegram bot via `@BotFather` in 30 seconds and send real voice notes directly from the Telegram app on your phone.
