import json

with open(r"C:\Users\jaswa\.gemini\antigravity\brain\8ef42ec7-c94e-42cf-a5aa-28f392b85668\.system_generated\logs\transcript.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)
        idx = obj.get("step_index")
        if 2234 <= idx <= 2276 and obj.get("type") == "PLANNER_RESPONSE":
            tc = obj.get("tool_calls", [])
            for t in tc:
                name = t.get("name")
                args = t.get("args", {})
                print(f"Step {idx}: {name} | {str(args)[:150]}")
