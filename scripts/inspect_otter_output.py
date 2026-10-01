import json

with open(r"C:\Users\jaswa\.gemini\antigravity\brain\8ef42ec7-c94e-42cf-a5aa-28f392b85668\.system_generated\steps\2453\output.txt", "r", encoding="utf-8") as f:
    text = f.read()

start = text.find("{")
decoder = json.JSONDecoder()
obj, _ = decoder.raw_decode(text[start:])
print("totalTranscripts:", obj.get("totalTranscripts"))
print("\n--- Recent transcripts ---")
for t in obj.get("recentTranscripts", []):
    print(f"{t.get('speaker')}: {t.get('text')}")

print("\n--- GH / Tools Transcripts ---")
for t in obj.get("ghTranscriptsSample", []):
    print(f"{t.get('speaker')}: {t.get('text')}")

print("\n--- External Links ---")
for l in obj.get("links", []):
    print(l)

print("\n--- DOM Matches ---")
for m in obj.get("domMatches", []):
    print(m)
