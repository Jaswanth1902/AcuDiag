import json
import re

with open(r"C:\Users\jaswa\.gemini\antigravity\brain\8ef42ec7-c94e-42cf-a5aa-28f392b85668\.system_generated\steps\2620\output.txt", "r", encoding="utf-8") as f:
    text = f.read()

start = text.find("{")
decoder = json.JSONDecoder()
data, _ = decoder.raw_decode(text[start:])
full_text = data.get("text", "")

# Find where Devansh Mangal appears
pos = full_text.find("Devansh Mangal")
if pos != -1:
    print("Found Devansh Mangal at pos:", pos)
    qa_segment = full_text[pos:]
else:
    # search for 50: or 48:
    print("Devansh Mangal not found directly, searching regex...")
    m = re.search(r'(?:50:\d\d|Devansh)', full_text)
    if m:
        pos = m.start()
        qa_segment = full_text[pos:]
    else:
        qa_segment = full_text[-15000:]

print("Length of QA segment:", len(qa_segment))
out_path = r"C:\Users\jaswa\Antigravity\01_Projects\AcuDiag\databank\FIREFLIES_QA_SESSION.txt"
with open(out_path, "w", encoding="utf-8") as out:
    out.write(qa_segment)

print("\n--- FIRST 2000 CHARS OF QA SEGMENT ---")
print(qa_segment[:2000])

print("\n--- LAST 2000 CHARS OF QA SEGMENT ---")
print(qa_segment[-2000:])
