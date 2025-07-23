#!/usr/bin/env python3
"""
Automated Backup Tool - Core functionality
"""

import os
import shutil
import json
import datetime
from pathlib import Path
import argparse
import sys

class BackupTool:
    def __init__(self, config_file="backup_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Load backup configuration from file"""
        if not os.path.exists(self.config_file):
            return self.create_default_config()
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration"""
        default_config = {
            "backup_sources": [
                str(Path.home() / "Documents"),
                str(Path.home() / "Desktop")
            ],
            "backup_destination": str(Path.home() / "Backups"),
            "exclude_patterns": [
                "*.tmp",
                "*.log",
                "__pycache__",
                ".git"
            ]
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        print(f"Created default config at {self.config_file}")
        return default_config
    
    def should_exclude(self, path):
        """Check if path should be excluded based on patterns"""
        path_str = str(path)
        for pattern in self.config.get("exclude_patterns", []):
            if pattern.startswith("*"):
                if path_str.endswith(pattern[1:]):
                    return True
            elif pattern in path_str:
                return True
        return False
    
    def backup_directory(self, source, destination):
        """Backup a single directory"""
        source_path = Path(source)
        if not source_path.exists():
            print(f"Source path does not exist: {source}")
            return False
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{source_path.name}_{timestamp}"
        dest_path = Path(destination) / backup_name
        
        try:
            dest_path.mkdir(parents=True, exist_ok=True)
            
            total_files = 0
            copied_files = 0
            
            for root, dirs, files in os.walk(source_path):
                root_path = Path(root)
                
                # Filter out excluded directories
                dirs[:] = [d for d in dirs if not self.should_exclude(root_path / d)]
                
                for file in files:
                    file_path = root_path / file
                    total_files += 1
                    
                    if self.should_exclude(file_path):
                        continue
                    
                    # Calculate relative path and create destination
                    rel_path = file_path.relative_to(source_path)
                    dest_file = dest_path / rel_path
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    try:
                        shutil.copy2(file_path, dest_file)
                        copied_files += 1
                    except Exception as e:
                        print(f"Error copying {file_path}: {e}")
            
            print(f"Backup completed: {source}")
            print(f"  Files processed: {total_files}")
            print(f"  Files copied: {copied_files}")
            print(f"  Destination: {dest_path}")
            return True
            
        except Exception as e:
            print(f"Error backing up {source}: {e}")
            return False
    
    def run_backup(self):
        """Run backup for all configured sources"""
        print("Starting automated backup...")
        print(f"Timestamp: {datetime.datetime.now()}")
        
        destination = self.config["backup_destination"]
        sources = self.config["backup_sources"]
        
        if not sources:
            print("No backup sources configured")
            return False
        
        success_count = 0
        for source in sources:
            if self.backup_directory(source, destination):
                success_count += 1
        
        print(f"\nBackup completed: {success_count}/{len(sources)} successful")
        return success_count == len(sources)
    
    def list_backups(self):
        """List existing backups"""
        backup_dir = Path(self.config["backup_destination"])
        if not backup_dir.exists():
            print("No backup directory found")
            return
        
        backups = [d for d in backup_dir.iterdir() if d.is_dir()]
        if not backups:
            print("No backups found")
            return
        
        print("Existing backups:")
        for backup in sorted(backups, key=lambda x: x.stat().st_mtime, reverse=True):
            size = sum(f.stat().st_size for f in backup.rglob('*') if f.is_file())
            size_mb = size / (1024 * 1024)
            mtime = datetime.datetime.fromtimestamp(backup.stat().st_mtime)
            print(f"  {backup.name} - {size_mb:.1f}MB - {mtime.strftime('%Y-%m-%d %H:%M')}")
    
    def add_source(self, path):
        """Add a new backup source"""
        source_path = str(Path(path).resolve())
        if source_path not in self.config["backup_sources"]:
            self.config["backup_sources"].append(source_path)
            self.save_config()
            print(f"Added backup source: {source_path}")
        else:
            print(f"Source already exists: {source_path}")
    
    def remove_source(self, path):
        """Remove a backup source"""
        source_path = str(Path(path).resolve())
        if source_path in self.config["backup_sources"]:
            self.config["backup_sources"].remove(source_path)
            self.save_config()
            print(f"Removed backup source: {source_path}")
        else:
            print(f"Source not found: {source_path}")
    
    def save_config(self):
        """Save current configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Automated Backup Tool")
    parser.add_argument("command", choices=["backup", "list", "add-source", "remove-source", "config"], 
                       help="Command to execute")
    parser.add_argument("--path", help="Path for add-source/remove-source commands")
    
    args = parser.parse_args()
    
    backup_tool = BackupTool()
    
    if args.command == "backup":
        backup_tool.run_backup()
    elif args.command == "list":
        backup_tool.list_backups()
    elif args.command == "add-source":
        if not args.path:
            print("--path required for add-source command")
            sys.exit(1)
        backup_tool.add_source(args.path)
    elif args.command == "remove-source":
        if not args.path:
            print("--path required for remove-source command")
            sys.exit(1)
        backup_tool.remove_source(args.path)
    elif args.command == "config":
        print(f"Configuration file: {backup_tool.config_file}")
        print(json.dumps(backup_tool.config, indent=2))

if __name__ == "__main__":
    main()