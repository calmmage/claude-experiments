# Automated Backup Tool

A simple, lightweight automated backup tool for creating timestamped backups of your important directories.

## Features

- **Automated Directory Backup**: Create timestamped backups of configured directories
- **Configurable Sources**: Add/remove backup sources dynamically
- **Exclusion Patterns**: Skip unwanted files (temp files, logs, git repos, etc.)
- **CLI Interface**: Simple command-line interface for all operations
- **JSON Configuration**: Easy-to-edit configuration file
- **Backup Listing**: View existing backups with size and timestamp info

## Quick Start

1. **Run the tool**:
   ```bash
   ./run.sh
   ```

2. **Create your first backup**:
   ```bash
   ./run.sh backup
   ```

3. **List existing backups**:
   ```bash
   ./run.sh list
   ```

## Commands

### Backup Operations
- `./run.sh backup` - Run backup for all configured sources
- `./run.sh list` - List existing backups with details

### Configuration Management
- `./run.sh config` - Show current configuration
- `./run.sh add-source <path>` - Add a new backup source
- `./run.sh remove-source <path>` - Remove a backup source

## Default Configuration

On first run, the tool creates a default configuration (`backup_config.json`):

```json
{
  "backup_sources": [
    "/Users/username/Documents",
    "/Users/username/Desktop"
  ],
  "backup_destination": "/Users/username/Backups",
  "exclude_patterns": [
    "*.tmp",
    "*.log",
    "__pycache__",
    ".git"
  ]
}
```

## Examples

### Add a custom backup source
```bash
./run.sh add-source ~/Projects
```

### Remove a backup source
```bash
./run.sh remove-source ~/Desktop
```

### View configuration
```bash
./run.sh config
```

## Backup Structure

Backups are organized as follows:
```
~/Backups/
├── Documents_20240123_143022/
├── Desktop_20240123_143045/
└── Projects_20240123_143102/
```

Each backup directory contains a complete copy of the source directory at the time of backup, with excluded files filtered out.

## Requirements

- Python 3.6+
- Unix-like system (macOS, Linux)
- Write permissions to backup destination

## Customization

Edit `backup_config.json` to customize:
- **backup_sources**: List of directories to backup
- **backup_destination**: Where to store backups
- **exclude_patterns**: File patterns to skip during backup

## Error Handling

The tool includes basic error handling for:
- Missing source directories
- Permission issues
- File copy errors
- Configuration file problems

Failed operations are logged to the console with descriptive error messages.

## Limitations

- No compression (creates full file copies)
- No incremental backups
- No network/cloud backup support
- No scheduling (use system cron for automation)

## License

This is a minimal viable product (MVP). Use at your own discretion.