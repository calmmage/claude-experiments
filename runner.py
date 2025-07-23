#!/usr/bin/env python3
import subprocess
import time
import random
from pathlib import Path
from pydantic_settings import BaseSettings

class RunnerSettings(BaseSettings):
    """Settings for the experiment runner"""
    # todo: use
    mode: str = "ai"  # "ai" or "random"
    call_timeout: int = 600  # seconds for Claude Code to respond


    class Config:
        env_prefix = "RUNNER_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = RunnerSettings()

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
    # Simplified prompt for better reliability
    prompt = f"""Create a {idea}. Output format:
### FILE: filename
file contents here
### FILE: another_filename
more contents

Include: README.md explaining the project, run.sh to start it, and all needed code files."""
    
    cmd = [
        "claude",
        "--print", prompt
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=settings.call_timeout)
        
        if result.returncode != 0:
            raise Exception(f"Claude Code failed: {result.stderr}")
        
        # Parse output and create files
        create_files_from_output(experiment_dir, result.stdout)
        
        return result.stdout
    except subprocess.TimeoutExpired:
        raise Exception("Claude Code timed out after 60 seconds")

def create_files_from_output(experiment_dir, output):
    """Parse Claude's output and create files"""
    lines = output.split('\n')
    current_file = None
    current_content = []
    
    for line in lines:
        if line.startswith("### FILE:"):
            # Save previous file if any
            if current_file:
                file_path = experiment_dir / current_file
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text('\n'.join(current_content))
                if current_file == "run.sh":
                    file_path.chmod(0o755)
            
            # Start new file
            current_file = line.replace("### FILE:", "").strip()
            current_content = []
        elif current_file:
            current_content.append(line)
    
    # Save last file
    if current_file:
        file_path = experiment_dir / current_file
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text('\n'.join(current_content))
        if current_file == "run.sh":
            file_path.chmod(0o755)

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
    idea = get_experiment_idea("random")  # or "random"
    
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