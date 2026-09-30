# 📱 Real WhatsApp & Operations Console Testing Setup Guide

> **Target**: Step-by-Step Instructions for You & Your Teammates  
> **Compliance**: The Ken Round 3 Rules (*"Every other connector must be the real tool... A team member can play the user on the other end."*)

---

## 🎯 Executive Dual-Track Strategy

The Council approved two complementary tracks:

| Track | What It Is | Best Used For | Setup Effort |
| :--- | :--- | :--- | :--- |
| **Track A: In-Browser 3-Pane Console** | Pixel-perfect Operations Command Desk with WhatsApp simulator, dual customer/technician switcher, audio player, and supervisor console. | **Submission Video Recording (1080p, crisp, zero glare)** | **0 seconds** (instant) |
| **Track B: Physical Phone WhatsApp** | Live Twilio WhatsApp Sandbox webhook sending messages and audio notes from your physical smartphone. | **Empirical Physical Proof & Interactive Testing** | **2 minutes** |

---

## 🖥️ Track A: Instant In-Browser Operations Console (For Your Video)

This is already 100% built and running locally.

### Step 1: Start the Server (if not already running)
Open a terminal in `01_Projects/AcuDiag/` and run:
```powershell
python databank/03_Mock_Server/mock_server.py
```
It starts on **`http://localhost:8000`**.

### Step 2: Open the Operations Desk
Open your browser to: **[http://localhost:8000](http://localhost:8000)**

### Step 3: Run the 4-Case Narrative Walkthrough (Follow `docs/SCREEN_RECORDING_GUIDE.md`)
1. **Case 1: Priya Sharma (Happy Path - ₹1,250 Settlement)**:
   - Click Priya in Pane 1.
   - Listen to the washing machine screech audio bubble in Pane 2.
   - Tap `[👤 Customer]` vs `[🔧 Technician]` in the top pill switch to show Suresh Kumar's field dispatch.
   - Show Pine Labs Escrow ₹1,250 and Delhivery tracking in Pane 3.
2. **Case 2: Rajesh Kumar (Replay Fraud Blocked)**:
   - Click Rajesh in Pane 1.
   - Show the red alarm banner: `REPLAY_SPOOF_BLOCKED (DAC Jitter Detected)`.
   - In Pane 3, click `[ 🛡️ Uphold Fraud Lock ]` to demonstrate Supervisor R. Sundaram's cryptographic override.
3. **Case 3: Amit Verma (Fake Repair Locked)**:
   - Click Amit in Pane 1.
   - Show the red alarm banner: `FAKE_REPAIR_LOCKED (Post-Repair Screech Active)`.
   - In Pane 3, click `[ 🔄 Dispatch Senior Tech ]` to re-assign a Master Tech.
4. **Case 4: Ananya Iyer (Low SNR Rejection)**:
   - Click Ananya in Pane 1.
   - Show ambient pressure cooker noise rejected ($9.4\text{ dB} < 15.0\text{ dB}$).

---

## 📱 Track B: Live WhatsApp From Your Physical Smartphone

If you or an evaluator want to send live WhatsApp messages from an actual phone:

### Step 1: Start the Local Mock Server
```powershell
python databank/03_Mock_Server/mock_server.py
```

### Step 2: Expose Your Server to Public HTTPS
In a second terminal, run:
```powershell
npx localtunnel --port 8000
```
*Note your public HTTPS URL*, e.g.: `https://shy-foxes-sing.loca.lt`

### Step 3: Set Webhook in Free Twilio Sandbox (2 Minutes)
1. Log in or create a free account at [twilio.com/console](https://www.twilio.com/console).
2. Go to: **Messaging** $\rightarrow$ **Try it out** $\rightarrow$ **Send a WhatsApp message**.
3. Under **Sandbox Settings** $\rightarrow$ **"When a message comes in"**:
   - Paste URL: `https://<YOUR_LOCALTUNNEL_URL>/api/whatsapp/webhook`
   - Method: `HTTP POST`
   - Click **Save**.

### Step 4: Send Messages From Your Phone!
1. **Join Sandbox**: Open WhatsApp on your phone and send the join code (e.g. `join silver-fox`) to `+1 415 523 8886`.
2. **Send Symptom**:
   - Send: *"Machine spin karte waqt ajeeb awaz aa rahi hai"* (or send an audio voice note).
   - AcuDiag replies with the diagnostic report and ₹1,250 quote card.
3. **Authorize Escrow**:
   - Reply: *"APPROVE"*.
   - AcuDiag replies with Pine Labs Order ID and Delhivery Waybill!
4. **Verify Live Sync**:
   - Look at your laptop screen at `http://localhost:8000`.
   - Notice that your phone's message appeared live inside Priya's chat in Pane 2!
5. **Verify Repair**:
   - Reply: *"spin test done"*.
   - AcuDiag verifies harmonics and releases escrow to technician Suresh!
