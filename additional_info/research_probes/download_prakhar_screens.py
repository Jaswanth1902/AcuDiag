import urllib.request
import json
import os

with open(r"C:\Users\jaswa\.gemini\antigravity\brain\8ef42ec7-c94e-42cf-a5aa-28f392b85668\.system_generated\steps\2497\output.txt", "r", encoding="utf-8") as f:
    text = f.read()

start = text.find("[")
decoder = json.JSONDecoder()
data, _ = decoder.raw_decode(text[start:])

# Get latest shared snapshots
snapshots = [x for x in data if "SHARED_snapshot" in x.get("src", "") and x.get("width") == 1400]
print(f"Total valid snapshots: {len(snapshots)}")

latest = snapshots[-3:]
out_dir = r"C:\Users\jaswa\Antigravity\01_Projects\AcuDiag\databank"

downloaded = []
for i, s in enumerate(latest):
    url = s["src"]
    # get timestamp from url
    fname = f"prakhar_screen_{i}.png"
    fpath = os.path.join(out_dir, fname)
    print(f"Downloading {fname} from {url[:80]}...")
    urllib.request.urlretrieve(url, fpath)
    downloaded.append(fpath)

print("Downloaded files:", downloaded)
