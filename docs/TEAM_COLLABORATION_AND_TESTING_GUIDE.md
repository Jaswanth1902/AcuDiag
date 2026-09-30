# 👥 Team Collaboration, Roles & Remote Test Execution Guide

> **Event**: The Ken Case-Build Competition 2026: Round 3 (Build Stage)  
> **Target**: Multi-Member Co-Op, Human Actor Setup & Remote Testing Protocol

---

## 1. 🎭 What Your Friend Should Be Doing (Assigned Roles)

According to The Ken's official Round 3 rules:
> *"A team member can play the 'user' on the other end, like the user sending a voice note or approving a payment, but they do it through an actual tool. Then run it again with at least two different human inputs, like the user saying no or replying late, and show how your agent's output changes."*

### Role A: The Real-World Human Actor (Mandatory for Screen Recording)
1. **The Distressed Homeowner (Happy Run)**:
   - Sends real voice notes via WhatsApp / Telegram in Hindi / Hinglish (*"Machine se ajeeb awaz aa rahi hai"*).
   - Approves the ₹1,250 pre-auth escrow hold link received on his phone.
2. **The Adversarial Homeowner (Perturbed Run 1 — "User Says NO")**:
   - Rejects the estimate (*"Too expensive, cancel this service"*).
   - Verifies agent executes clean escrow cancellation and Delhivery order recall.
3. **The Unresponsive Homeowner (Perturbed Run 2 — "Late Reply / Timeout")**:
   - Delays replying to the confirmation prompt for >5 minutes to trigger the agent's scheduled reminder logic.
4. **The Field Technician**:
   - Holds his smartphone next to a spinning appliance or audio speaker to trigger the 10-second post-repair acoustic verification.

### Role B: The Chaos & Edge-Case QA Lead
- Uses the Tactical Cockpit chaos switches (injects `no_rider`, `low_balance`, `bank_timeout`, `malformed_json`) and validates error containment.

---

## 2. 🔑 How to Give Him Complete Access (3 Channels)

### Channel 1: Instant Zero-Install Web Access (Recommended for Live Testing)
Your friend does not need Python or Git installed on his machine to test the diagnostic engine and UI.
1. Run the local tunnel script on your machine:
   ```powershell
   python 01_Projects/AcuDiag/scripts/start_tunnel.py
   ```
2. Send him the generated public HTTPS URL (e.g., `https://acudiag-demo.loca.lt` or ngrok URL).
3. He can open it directly in Safari / Chrome on his iPhone / Android or laptop:
   - He can record real physical machine audio using his phone's microphone.
   - He can trigger simulated diagnostic runs and inspect real-time spectrograms.
   - He can monitor the 9-state blackboard transitions live.

### Channel 2: Full Code & Test Harness Access (GitHub)
If he wants to run pytests and inspection locally on his computer:
1. Initialize and push `01_Projects/AcuDiag` to a private GitHub repo:
   ```powershell
   cd 01_Projects/AcuDiag
   git init
   git add .
   git commit -m "feat: complete AcuDiag Round 3 build"
   gh repo create AcuDiag-TheKen --private --source=. --push
   ```
2. Add your friend's GitHub handle as a collaborator:
   ```powershell
   gh repo collaborator add <friend-github-username> --permission admin
   ```
3. He clones the repo, installs dependencies (`pip install -r requirements.txt`), and runs:
   ```powershell
   python run_full_verification.py
   ```

### Channel 3: Pine Labs AgenticOrg Platform Co-Pilot
1. Have your friend sign in at: [https://agenticorg.hackathon.pinelabs.com](https://agenticorg.hackathon.pinelabs.com)
2. Ensure he selects **Join existing organization** $\rightarrow$ select `Ken's case competition`.
3. In the platform, verify that you are both assigned to the same domain (`ops`) so he can view, edit, and co-run the `AcuDiag Orchestrator` virtual employee and its connectors.

---

## 3. 🎬 Rehearsal Protocol for the Final Screen Recording

1. **Setup**: You share screen on Google Meet / Zoom while recording via OBS or QuickTime.
2. **Actor Cue**: On your signal, your friend sends the real voice note via WhatsApp.
3. **Observation**: Screen recording shows Pine Labs AgenticOrg receiving the webhook, invoking Gnani STT, evaluating the DSP diagnosis, holding Pine Labs escrow, and dispatching Delhivery logistics.
4. **Variations**: Repeat for the "User saying NO" and "User replying late" runs.
