import json
import urllib.request

file_path = r"C:\Users\jaswa\.gemini\antigravity\brain\8ef42ec7-c94e-42cf-a5aa-28f392b85668\.system_generated\steps\2419\output.txt"
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

start = text.find("{")
decoder = json.JSONDecoder()
payload, _ = decoder.raw_decode(text[start:])
images = payload.get("images", [])
print(f"Total screenshots captured by Otter: {len(images)}")

# Download the last 3 screenshots
for i, img in enumerate(images[-3:]):
    url = img.get("image_url")
    offset = img.get("offset")
    dest = rf"C:\Users\jaswa\Antigravity\01_Projects\AcuDiag\databank\otter_screenshot_{i}.png"
    print(f"Downloading screenshot offset {offset} to {dest}...")
    try:
        urllib.request.urlretrieve(url, dest)
        print("Done!")
    except Exception as e:
        print("Failed:", e)
