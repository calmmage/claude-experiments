#!/usr/bin/env python3

import os
import sys
import argparse
import shutil
import json
from datetime import datetime
from pathlib import Path
import hashlib
from collections import defaultdict

class FileOrganizer:
    def __init__(self, directory='.', dry_run=False):
        self.directory = Path(directory).resolve()
        self.dry_run = dry_run
        self.undo_log = []
        self.undo_file = self.directory / '.file_organizer_undo.json'
        
        self.default_categories = {
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
            'Archives': ['.zip', '.tar', '.gz', '.rar', '.7z', '.bz2'],
            'Code': ['.py', '.js', '.html', '.css', '.cpp', '.java', '.c', '.h', '.go', '.rs'],
            'Data': ['.json', '.xml', '.csv', '.sql', '.db']
        }
        
    def organize_by_type(self, recursive=False):
        """Organize files by their type/extension"""
        extension_to_category = {}
        for category, extensions in self.default_categories.items():
            for ext in extensions:
                extension_to_category[ext.lower()] = category
        
        files_to_move = self._get_files(recursive)
        moves = []
        
        for file_path in files_to_move:
            if file_path.is_file():
                extension = file_path.suffix.lower()
                category = extension_to_category.get(extension, 'Others')
                
                target_dir = self.directory / category
                target_path = target_dir / file_path.name
                
                if file_path != target_path:
                    moves.append((file_path, target_path))
        
        self._execute_moves(moves)
    
    def organize_by_date(self, recursive=False, date_format='%Y-%m'):
        """Organize files by their modification date"""
        files_to_move = self._get_files(recursive)
        moves = []
        
        for file_path in files_to_move:
            if file_path.is_file():
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                date_folder = mtime.strftime(date_format)
                
                target_dir = self.directory / date_folder
                target_path = target_dir / file_path.name
                
                if file_path != target_path:
                    moves.append((file_path, target_path))
        
        self._execute_moves(moves)
    
    def organize_by_custom_rules(self, config_file, recursive=False):
        """Organize files based on custom rules from config file"""
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        rules = config.get('rules', [])
        files_to_move = self._get_files(recursive)
        moves = []
        
        for file_path in files_to_move:
            if file_path.is_file():
                for rule in rules:
                    if self._matches_rule(file_path, rule):
                        folder = rule.get('folder', 'Others')
                        target_dir = self.directory / folder
                        target_path = target_dir / file_path.name
                        
                        if file_path != target_path:
                            moves.append((file_path, target_path))
                            break
        
        self._execute_moves(moves)
    
    def undo_last_operation(self):
        """Undo the last organization operation"""
        if not self.undo_file.exists():
            print("No undo log found.")
            return
        
        with open(self.undo_file, 'r') as f:
            undo_data = json.load(f)
        
        last_operation = undo_data.get('operations', [])
        if not last_operation:
            print("No operations to undo.")
            return
        
        print(f"Undoing {len(last_operation)} file movements...")
        
        for move in reversed(last_operation):
            src = Path(move['to'])
            dst = Path(move['from'])
            
            if src.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                print(f"Restored: {src.name} → {dst.parent.name}/")
        
        self.undo_file.unlink()
        print("Undo completed successfully.")
    
    def _get_files(self, recursive):
        """Get list of files to organize"""
        if recursive:
            files = [f for f in self.directory.rglob('*') if f.is_file()]
        else:
            files = [f for f in self.directory.iterdir() if f.is_file()]
        
        # Filter out hidden files and the undo log
        files = [f for f in files if not f.name.startswith('.')]
        return files
    
    def _matches_rule(self, file_path, rule):
        """Check if a file matches a custom rule"""
        # Check extensions
        extensions = rule.get('extensions', [])
        if extensions and file_path.suffix.lower() in [ext.lower() for ext in extensions]:
            return True
        
        # Check pattern
        pattern = rule.get('pattern', '')
        if pattern:
            import fnmatch
            if fnmatch.fnmatch(file_path.name, pattern):
                return True
        
        return False
    
    def _execute_moves(self, moves):
        """Execute the file movements"""
        if not moves:
            print("No files to organize.")
            return
        
        if self.dry_run:
            print("DRY RUN MODE - No files will be moved")
            print("-" * 50)
        
        successful_moves = []
        
        for src, dst in moves:
            dst_dir = dst.parent
            
            # Create target directory if needed
            if not self.dry_run and not dst_dir.exists():
                dst_dir.mkdir(parents=True, exist_ok=True)
            
            # Handle duplicates
            final_dst = self._handle_duplicate(dst)
            
            if self.dry_run:
                print(f"Would move: {src.name} → {dst_dir.name}/{final_dst.name}")
            else:
                try:
                    shutil.move(str(src), str(final_dst))
                    print(f"Moved: {src.name} → {dst_dir.name}/{final_dst.name}")
                    successful_moves.append({
                        'from': str(src),
                        'to': str(final_dst)
                    })
                except Exception as e:
                    print(f"Error moving {src.name}: {e}")
        
        # Save undo log
        if successful_moves and not self.dry_run:
            self._save_undo_log(successful_moves)
            print(f"\nOrganized {len(successful_moves)} files successfully.")
    
    def _handle_duplicate(self, target_path):
        """Handle duplicate files by adding a number suffix"""
        if not target_path.exists():
            return target_path
        
        stem = target_path.stem
        suffix = target_path.suffix
        parent = target_path.parent
        
        counter = 1
        while True:
            new_name = f"{stem}_{counter}{suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1
    
    def _save_undo_log(self, moves):
        """Save the moves for undo functionality"""
        undo_data = {'operations': moves, 'timestamp': datetime.now().isoformat()}
        with open(self.undo_file, 'w') as f:
            json.dump(undo_data, f, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description='Organize files in a directory by type, date, or custom rules'
    )
    parser.add_argument('directory', nargs='?', default='.',
                        help='Directory to organize (default: current directory)')
    parser.add_argument('-t', '--type', action='store_true', default=True,
                        help='Organize by file type (default)')
    parser.add_argument('-d', '--date', action='store_true',
                        help='Organize by modification date')
    parser.add_argument('-c', '--custom', metavar='CONFIG',
                        help='Use custom configuration file')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='Include subdirectories')
    parser.add_argument('-n', '--dry-run', action='store_true',
                        help='Preview changes without moving files')
    parser.add_argument('-u', '--undo', action='store_true',
                        help='Undo the last organization')
    
    args = parser.parse_args()
    
    # Validate directory
    if not os.path.exists(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist.")
        sys.exit(1)
    
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a directory.")
        sys.exit(1)
    
    # Check write permissions
    if not args.dry_run and not os.access(args.directory, os.W_OK):
        print(f"Error: No write permission for directory '{args.directory}'.")
        sys.exit(1)
    
    organizer = FileOrganizer(args.directory, args.dry_run)
    
    try:
        if args.undo:
            organizer.undo_last_operation()
        elif args.custom:
            if not os.path.exists(args.custom):
                print(f"Error: Configuration file '{args.custom}' not found.")
                sys.exit(1)
            organizer.organize_by_custom_rules(args.custom, args.recursive)
        elif args.date:
            organizer.organize_by_date(args.recursive)
        else:
            organizer.organize_by_type(args.recursive)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()