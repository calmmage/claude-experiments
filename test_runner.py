#!/usr/bin/env python3
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent
EXPERIMENTS_DIR = REPO_ROOT / "experiments"

def main():
    # Create test directory
    EXPERIMENTS_DIR.mkdir(exist_ok=True)
    test_dir = EXPERIMENTS_DIR / "test_experiment"
    test_dir.mkdir(exist_ok=True)
    
    prompt = f"""Create a simple hello world Python script at {test_dir}/hello.py that prints 'Hello from experiment!'"""
    
    cmd = [
        "claude",
        "--print", prompt,
        "--add-dir", str(test_dir)
    ]
    
    print("Running command:", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print("Return code:", result.returncode)
    print("Stdout:", result.stdout[:500])
    print("Stderr:", result.stderr[:500])
    
    # Check if file was created
    hello_file = test_dir / "hello.py"
    if hello_file.exists():
        print(f"\nFile created! Contents:")
        print(hello_file.read_text())
    else:
        print("\nFile was not created")

if __name__ == "__main__":
    main()