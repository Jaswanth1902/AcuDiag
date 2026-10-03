import json

with open(r"C:\Users\jaswa\.gemini\antigravity\brain\8ef42ec7-c94e-42cf-a5aa-28f392b85668\.system_generated\steps\2489\output.txt", "r", encoding="utf-8") as f:
    text = f.read()

start = text.find("{")
decoder = json.JSONDecoder()
data, _ = decoder.raw_decode(text[start:])

print("Keys returned:", list(data.keys()))

for k, v in data.items():
    if isinstance(v, dict):
        status = v.get("status")
        if status:
            print(f"{k} -> status {status}")
        else:
            print(f"{k} -> keys: {list(v.keys())}")
            # check for summary / chat / notes content
            for subk in ["summary", "notes", "messages", "outline", "speech"]:
                if subk in v:
                    print(f"  Found {subk}: type={type(v[subk])}")
                    val_str = str(v[subk])
                    print(f"  Length: {len(val_str)}")
                    if "github" in val_str.lower() or "repo" in val_str.lower():
                        print(f"  *** MATCH FOUND IN {k} / {subk} ***")
                        # print context
                        import re
                        for m in re.finditer(r'(.{0,100}(?:github|repo|tool).{0,100})', val_str, re.IGNORECASE):
                            print("   MATCH:", m.group(1))

# Let's inspect speech transcripts in detail
speech = data.get("/forward/api/v1/speech?otid=OqV_3qXSQiIo5cvE7e0w8l4lBBU", {}).get("speech", {})
transcripts = speech.get("transcripts", [])
print(f"\nTotal transcripts: {len(transcripts)}")

# Search all transcripts for github, repo, link, etc.
for i, t in enumerate(transcripts):
    txt = t.get("transcript", "")
    spk = t.get("sdk_speaker") or t.get("speaker_id")
    low = txt.lower()
    if any(w in low for w in ["github", "repo", "git", "link", "url", "drive", "sample", "postman", "swagger"]):
        print(f"[{i}] {spk}: {txt}")
