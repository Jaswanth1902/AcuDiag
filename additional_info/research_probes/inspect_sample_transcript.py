import json

file_path = r"C:\Users\jaswa\.gemini\antigravity\brain\8ef42ec7-c94e-42cf-a5aa-28f392b85668\.system_generated\steps\2349\output.txt"
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

start = text.find("{")
decoder = json.JSONDecoder()
payload, _ = decoder.raw_decode(text[start:])
data = payload.get("dataSample", {})
speech = data.get("speech", {})

print("Speech keys:", list(speech.keys()))
if "transcripts" in speech and speech["transcripts"]:
    print("Transcript[0] sample keys:", list(speech["transcripts"][0].keys()))
    print("Transcript[0] sample:", speech["transcripts"][0])
