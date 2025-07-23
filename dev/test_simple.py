#!/usr/bin/env python3
import subprocess

result = subprocess.run(
    ["claude", "--print", "Write a one-line Python print statement"],
    capture_output=True,
    text=True,
    timeout=10
)

print("Return code:", result.returncode)
print("Output:", result.stdout)
print("Error:", result.stderr)