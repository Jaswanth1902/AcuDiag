import json

file_path = r"C:\Users\jaswa\.gemini\antigravity\brain\8ef42ec7-c94e-42cf-a5aa-28f392b85668\.system_generated\steps\2349\output.txt"
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

start = text.find("{")
decoder = json.JSONDecoder()
payload, _ = decoder.raw_decode(text[start:])
data = payload.get("dataSample", {})
speech = data.get("speech", {})
transcripts = speech.get("transcripts", [])

lines = []
for t in transcripts:
    spk = t.get("sdk_speaker") or t.get("speaker_id") or "Unknown"
    content = t.get("transcript", "").strip()
    start_sec = t.get("start_offset", 0) / 1000000.0  # start_offset is in microseconds
    if content:
        lines.append(f"[{start_sec/60:.1f}m] {spk}: {content}")

print(f"Total extracted spoken turns: {len(lines)}")
print("\n" + "="*50)
for l in lines:
    print(l)
print("="*50)

out_path = r"C:\Users\jaswa\Antigravity\01_Projects\AcuDiag\databank\LIVE_PINE_LABS_DEMO_TRANSCRIPT.txt"
with open(out_path, "w", encoding="utf-8") as out:
    out.write("\n".join(lines))
