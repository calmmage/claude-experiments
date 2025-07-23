#!/usr/bin/env python3
import subprocess
import json
import time
import random
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent
EXPERIMENTS_DIR = REPO_ROOT / "experiments"

def get_next_day_number():
    """Get the next day number based on existing experiments"""
    if not EXPERIMENTS_DIR.exists():
        return 1
    
    day_nums = []
    for exp_dir in EXPERIMENTS_DIR.iterdir():
        if exp_dir.is_dir() and exp_dir.name.startswith("day_"):
            try:
                num = int(exp_dir.name.split("_")[1])
                day_nums.append(num)
            except:
                pass
    
    return max(day_nums, default=0) + 1

def get_experiment_idea(mode="ai"):
    """Get experiment idea either from AI or predefined list"""
    if mode == "random":
        ideas = [
            "CLI tool for file organization",
            "Visualization of sorting algorithms",
            "Simple REST API with FastAPI",
            "Web scraper for news headlines",
            "Pomodoro timer with notifications",
            "Markdown to HTML converter",
            "Password strength checker",
            "CSV data analyzer",
            "Image metadata extractor",
            "Mini text-based adventure game"
        ]
        return random.choice(ideas)
    else:
        # AI generates idea
        return "Generate a creative programming experiment idea"

def run_claude_code(experiment_dir, idea):
    """Run Claude Code with the experiment idea"""
    prompt = f"""Create a programming experiment: {idea}

Requirements:
1. Create all files in {experiment_dir}
2. Include a run.sh script that starts/runs the experiment
3. Make it self-contained and immediately runnable
4. Add a brief README.md explaining what it does

Implementation should be complete and working."""
    
    cmd = [
        "claude",
        "--print", prompt,
        "--add-dir", str(experiment_dir)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Claude Code failed: {result.stderr}")
    
    return result.stdout

def verify_experiment(experiment_dir):
    """Verify the experiment has run.sh and it works"""
    run_script = experiment_dir / "run.sh"
    
    if not run_script.exists():
        return False, "No run.sh found"
    
    # Make executable
    run_script.chmod(0o755)
    
    # Try to run it
    try:
        proc = subprocess.Popen(
            ["bash", str(run_script)],
            cwd=experiment_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a few seconds
        time.sleep(3)
        
        # Check if still running or crashed
        if proc.poll() is None:
            # Still running, good
            proc.terminate()
            return True, "run.sh executed successfully"
        else:
            # Exited, check return code
            if proc.returncode == 0:
                return True, "run.sh completed successfully"
            else:
                stderr = proc.stderr.read().decode() if proc.stderr else ""
                return False, f"run.sh failed with code {proc.returncode}: {stderr[:200]}"
    except Exception as e:
        return False, f"Error running run.sh: {str(e)}"

def main():
    # Create experiments directory
    EXPERIMENTS_DIR.mkdir(exist_ok=True)
    
    # Get experiment details
    day_num = get_next_day_number()
    idea = get_experiment_idea("ai")  # or "random"
    
    # Create experiment directory
    exp_name = idea.lower().replace(" ", "_")[:30]  # First 30 chars
    experiment_dir = EXPERIMENTS_DIR / f"day_{day_num}_{exp_name}"
    experiment_dir.mkdir()
    
    print(f"Creating experiment: {experiment_dir.name}")
    print(f"Idea: {idea}")
    
    # Run Claude Code
    print("Running Claude Code...")
    output = run_claude_code(experiment_dir, idea)
    
    # Save output
    with open(experiment_dir / "claude_output.txt", "w") as f:
        f.write(output)
    
    # Verify experiment
    print("Verifying experiment...")
    success, message = verify_experiment(experiment_dir)
    
    if success:
        print(f"✓ Experiment verified: {message}")
    else:
        print(f"✗ Verification failed: {message}")
        # Could run Claude Code again to fix issues
    
    print(f"Experiment saved to: {experiment_dir}")

if __name__ == "__main__":
    main()