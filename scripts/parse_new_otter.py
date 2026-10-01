import json

with open(r"C:\Users\jaswa\.gemini\antigravity\brain\8ef42ec7-c94e-42cf-a5aa-28f392b85668\.system_generated\steps\2572\output.txt", "r", encoding="utf-8") as f:
    text = f.read()

start = text.find("{")
decoder = json.JSONDecoder()
data, _ = decoder.raw_decode(text[start:])
print("Status:", data.get("status"))
print("Total turns:", data.get("count"))
turns = data.get("allTurns", [])
print(f"\n--- ALL TURNS ({len(turns)}) ---")
lines = []
for i, t in enumerate(turns):
    spk = t.get("speaker") or "Unknown"
    txt = t.get("text") or ""
    line = f"[{i}] {spk}: {txt}"
    lines.append(line)
    print(line)

with open(r"C:\Users\jaswa\Antigravity\01_Projects\AcuDiag\databank\LIVE_PINE_LABS_DEMO_PART2.txt", "w", encoding="utf-8") as out:
    out.write("\n".join(lines))
