# 🎮 AcuDiag Tactical Cockpit: Step-by-Step User Walkthrough

> **URL**: [http://localhost:8000](http://localhost:8000) or [http://127.0.0.1:8000](http://127.0.0.1:8000)  
> **Target**: Hackathon Screen Recording, Interactive Testing & Live Demo

---

## 🚀 Option 1: The Automated 90-Second Demo (Fastest & Best for Video)

If you are recording your screen or showing it to someone:
1. Open [http://localhost:8000](http://localhost:8000) in your browser.
2. In the top-right header, click the gold button: **`▶ Start 90s Live Demo Flow`**.
3. **Sit back and watch**:
   - The **9-State Machine Track** moves automatically from `01 Onboard` $\rightarrow$ `09 Settlement`.
   - The **60 FPS Spectrogram** lights up with the screeching bearing frequency.
   - The **Escrow Vault** locks ₹1,250, displays the Pine Labs order ID, and generates the Delhivery tracking waybill (`DEL16100984`).
   - The **Event Terminal** prints live timestamps and decisions.
   - At step 09, it verifies the post-repair spin, unlocks the escrow, and releases payout to technician Suresh Kumar.

---

## 🛠️ Option 2: Step-by-Step Manual Interactive Flow (Hands-on Testing)

Follow this 5-step test sequence to try every capability manually:

### Step 1: Click "Bearing Spall" to Inject Fault Audio
- On the left column under the Spectrogram, click the red button: **`Bearing Spall`**.
- **What happens**: The canvas shows real-time FFT waterfall spikes at 1,450 Hz. The SNR indicator reads `26.4 dB` (clean capture), and the Neyman-Pearson LRT score triggers a critical bearing defect.

### Step 2: Step Through the 9-State Machine
- Click the numbered circles along the top track:
  - **`03 Acoustic`**: Agent receives the audio and runs Butterworth 4th-order SOS filtering.
  - **`04 Classify`**: Diagnoses drum bearing failure (SKU `BEAR-6205-2RS`).
  - **`05 Escrow Lock`**: The Escrow Vault on the right lights up in amber — ₹1,250 locked via Pine Labs Plural pre-auth hold.
  - **`06 Delhivery`**: Delhivery CMU rail shows dispatch from Peenya Hub to 560059.

### Step 3: Test Real Live Microphone Audio
- Click **`🎙 Microphone`**.
- Allow browser mic permissions.
- Hum, tap, or make noise near your laptop mic:
  - Watch the live 60 FPS WebAudio visualizer react instantly.
  - Notice the SNR calculation updating in real time.

### Step 4: Inject Chaos Scenarios (Bottom Deck)
Click any scenario card in the bottom **Chaos Injection Deck**:
1. **No Rider Available (Delhivery 503)**:
   - Simulates delivery partner stockout; agent triggers 4-hour buffered dispatch.
2. **Low Card Balance (Pine Labs 402)**:
   - Simulates customer card decline; agent routes alternative UPI / NetBanking link.
3. **Ambient Kitchen Noise (SNR < 15 dB)**:
   - Pressure cooker noise detected; agent pauses and prompts user to close the kitchen door.
4. **Replay Fraud Attack**:
   - Replay detector spots smartphone loudspeaker playback (missing sub-50Hz physical motor rumble); agent blocks fraud attempt.

### Step 5: Verify Final Resolution
- Click step **`08 Post-Test`** $\rightarrow$ then **`09 Settlement`**.
- The Escrow Vault turns **emerald green**: status changes to `CAPTURED_AND_RELEASED`, and warranty receipt is logged.
