import json

with open("prompt_download.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("parsed_content.md", "w", encoding="utf-8") as out:
    for c in data.get("chunkedPrompt", {}).get("chunks", []):
        role = c.get("role", "unknown")
        text = c.get("text", "")
        out.write(f"## Role: {role}\n\n{text}\n\n---\n\n")

print("Done parsing.")
