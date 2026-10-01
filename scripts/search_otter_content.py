import re

file_path = r"C:\Users\jaswa\.gemini\antigravity\brain\8ef42ec7-c94e-42cf-a5aa-28f392b85668\.system_generated\steps\2317\content.md"

try:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    print("Total length:", len(text))
    # Check if there is transcript text
    # In Otter.ai, transcript sentences usually appear in JSON or data attributes
    # Look for spoken words or phrases
    patterns = [r'"transcript"[^"]*', r'"speech"[^"]*', r'"text":"[^"]+"', r'"summary"[^"]*', r'"title":"[^"]+"']
    for p in patterns:
        m = re.findall(p, text)
        print(f"Pattern {p}: found {len(m)}")
        if m:
            print("Sample:", m[:5])

except Exception as e:
    print("Error:", e)
