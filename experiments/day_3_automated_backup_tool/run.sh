#!/bin/bash

# Automated Backup Tool Runner Script

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed"
    exit 1
fi

# Display help if no arguments provided
if [ $# -eq 0 ]; then
    echo "Automated Backup Tool"
    echo "Usage: ./run.sh <command> [options]"
    echo ""
    echo "Commands:"
    echo "  backup              - Run backup for all configured sources"
    echo "  list                - List existing backups"
    echo "  add-source <path>   - Add a new backup source"
    echo "  remove-source <path> - Remove a backup source"
    echo "  config              - Show current configuration"
    echo ""
    echo "Examples:"
    echo "  ./run.sh backup"
    echo "  ./run.sh list"
    echo "  ./run.sh add-source ~/Projects"
    echo "  ./run.sh config"
    exit 0
fi

# Execute the backup tool with provided arguments
python3 backup.py "$@"