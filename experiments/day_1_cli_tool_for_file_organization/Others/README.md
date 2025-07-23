# File Organization CLI Tool

A powerful command-line tool for organizing files in directories based on their types, dates, or custom rules.

## Features

- **Organize by file type**: Automatically sort files into folders based on their extensions
- **Date-based organization**: Sort files by creation/modification date
- **Custom rules**: Define your own organization patterns
- **Dry run mode**: Preview changes before applying them
- **Undo capability**: Revert the last organization operation
- **Recursive organization**: Organize files in subdirectories
- **Duplicate handling**: Smart handling of duplicate files

## Requirements

- Python 3.7+
- No external dependencies (uses standard library only)

## Installation

1. Clone or download this project
2. Make the run script executable:
   ```bash
   chmod +x run.sh
   ```

## Usage

Run the tool using the provided script:

```bash
./run.sh [OPTIONS] [DIRECTORY]
```

### Options

- `-t, --type`: Organize files by type (default)
- `-d, --date`: Organize files by date
- `-c, --custom <config>`: Use custom configuration file
- `-r, --recursive`: Include subdirectories
- `-n, --dry-run`: Preview changes without executing
- `-u, --undo`: Undo the last organization
- `-h, --help`: Show help message

### Examples

1. **Organize current directory by file type:**
   ```bash
   ./run.sh
   ```

2. **Organize Downloads folder by file type:**
   ```bash
   ./run.sh ~/Downloads
   ```

3. **Organize by date:**
   ```bash
   ./run.sh -d ~/Documents
   ```

4. **Dry run to preview changes:**
   ```bash
   ./run.sh -n ~/Desktop
   ```

5. **Recursive organization:**
   ```bash
   ./run.sh -r ~/Projects
   ```

6. **Custom rules:**
   ```bash
   ./run.sh -c custom_rules.json ~/Files
   ```

## Default File Type Categories

- **Documents**: pdf, doc, docx, txt, odt, xls, xlsx, ppt, pptx
- **Images**: jpg, jpeg, png, gif, bmp, svg, webp, ico
- **Videos**: mp4, avi, mkv, mov, wmv, flv, webm
- **Audio**: mp3, wav, flac, aac, ogg, wma, m4a
- **Archives**: zip, tar, gz, rar, 7z, bz2
- **Code**: py, js, html, css, cpp, java, c, h, go, rs
- **Data**: json, xml, csv, sql, db

## Custom Configuration

Create a JSON file to define custom organization rules:

```json
{
  "rules": [
    {
      "name": "Work Files",
      "extensions": [".doc", ".xls", ".ppt"],
      "folder": "Work"
    },
    {
      "name": "Personal Photos",
      "pattern": "IMG_*",
      "folder": "Photos/Personal"
    }
  ]
}
```

## Safety Features

- **Dry run mode**: Always preview changes before applying
- **Undo log**: Tracks all file movements for easy reversal
- **Duplicate handling**: Renames duplicates instead of overwriting
- **Permission checks**: Verifies write permissions before moving files

## License

MIT License