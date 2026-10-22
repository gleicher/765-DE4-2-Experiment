"""Print a prompt from PROMPTS.md: a student prompt ID (with the common tail) or DEBRIEF."""
import re, sys
text = open("PROMPTS.md").read()
key = sys.argv[1]
blocks = re.findall(r"```\n(.*?)```", text, re.S)
tail, debrief = blocks[0].strip(), blocks[1].strip()
if key == "DEBRIEF":
    print(debrief)
else:
    m = re.search(r"^\| " + re.escape(key) + r" \| (.*?) \|$", text, re.M)
    if not m:
        sys.exit(f"unknown prompt {key}")
    print(m.group(1).strip() + "\n\n" + tail)
