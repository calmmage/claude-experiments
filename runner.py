#!/usr/bin/env python3
import subprocess
import time
from pathlib import Path
from pydantic_settings import BaseSettings
from loguru import logger

from src.idea_generator import get_experiment_idea
from src.experiment_builder import ExperimentBuilder, ImplementationLevel

class RunnerSettings(BaseSettings):
    """Settings for the experiment runner"""
    idea_mode: str = "random"  # "random", "structured", "ai", "structured_ai"
    implementation_level: str = "mvp"  # "simple_test", "mvp", "full_scenario"
    call_timeout: int = 1200  # seconds for Claude Code to respond (20 minutes)


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


def run_claude_code(experiment_dir, idea, retry_context=None):
    """Run Claude Code with the experiment idea"""
    start_time = time.time()
    
    # Get implementation level
    level = ImplementationLevel(settings.implementation_level)
    
    # Build appropriate prompt
    if retry_context:
        prompt = ExperimentBuilder.get_retry_prompt(retry_context, idea, level)
    else:
        prompt = ExperimentBuilder.build_prompt(idea, level)
    
    # Change working directory to experiment dir for file creation
    cmd = [
        "claude",
        "-p", prompt,
        "--dangerously-skip-permissions"
    ]
    
    logger.info(f"Running Claude Code with prompt: {prompt[:100]}...")
    
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=settings.call_timeout,
            cwd=str(experiment_dir)  # Run in experiment directory
        )
        
        elapsed = time.time() - start_time
        logger.info(f"Claude Code completed in {elapsed:.2f}s")
        
        if result.returncode != 0 and result.stderr:
            logger.error(f"Claude Code failed with stderr: {result.stderr}")
            raise Exception(f"Claude Code failed: {result.stderr}")
        elif result.returncode != 0:
            logger.warning(f"Claude Code exited with code {result.returncode} but no stderr")
        
        # Save both stdout and stderr for debugging
        output = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        
        return output
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        logger.error(f"Claude Code timed out after {elapsed:.2f}s")
        raise Exception(f"Claude Code timed out after {settings.call_timeout} seconds")

def list_created_files(experiment_dir):
    """List all files created in the experiment directory"""
    files = []
    for item in experiment_dir.rglob('*'):
        if item.is_file():
            files.append(str(item.relative_to(experiment_dir)))
    return files

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

def commit_experiment(experiment_dir, idea):
    """Commit the experiment to git"""
    try:
        logger.info("Committing experiment to git...")
        
        # Add the experiment directory
        subprocess.run(["git", "add", str(experiment_dir)], check=True)
        
        # Create commit message
        day_name = experiment_dir.name
        commit_msg = f"Add {day_name}: {idea}"
        
        # Commit
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        logger.success(f"✓ Committed: {commit_msg}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to commit experiment: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during commit: {e}")

def main():
    logger.info("Starting experiment runner")
    start_time = time.time()
    
    # Create experiments directory
    EXPERIMENTS_DIR.mkdir(exist_ok=True)
    
    # Get experiment details
    day_num = get_next_day_number()
    idea = get_experiment_idea(settings.idea_mode)
    
    # Create experiment directory
    exp_name = idea.lower().replace(" ", "_")[:30]  # First 30 chars
    experiment_dir = EXPERIMENTS_DIR / f"day_{day_num}_{exp_name}"
    experiment_dir.mkdir()
    
    logger.info(f"Creating experiment: {experiment_dir.name}")
    logger.info(f"Idea: {idea}")
    
    # Run Claude Code with retry logic
    max_attempts = 2
    retry_context = None
    
    for attempt in range(max_attempts):
        logger.info(f"Attempt {attempt + 1}/{max_attempts}")
        
        # Run Claude Code
        output = run_claude_code(experiment_dir, idea, retry_context)
        
        # Save output
        with open(experiment_dir / "claude_output.txt", "w") as f:
            f.write(output)
        
        # List created files
        created_files = list_created_files(experiment_dir)
        logger.info(f"Created files: {created_files}")
        
        # Verify experiment
        logger.info("Verifying experiment...")
        verify_start = time.time()
        success, message = verify_experiment(experiment_dir)
        logger.info(f"Verification took {time.time() - verify_start:.2f}s")
        
        if success:
            logger.success(f"✓ Experiment verified: {message}")
            break
        else:
            logger.warning(f"✗ Verification failed: {message}")
            if attempt < max_attempts - 1:
                retry_context = message
                logger.info("Retrying with error context...")
            else:
                logger.error("Max attempts reached, giving up")
    
    total_time = time.time() - start_time
    logger.info(f"Experiment saved to: {experiment_dir}")
    logger.info(f"Total execution time: {total_time:.2f}s")
    
    # Commit the experiment
    if success:
        commit_experiment(experiment_dir, idea)

if __name__ == "__main__":
    main()