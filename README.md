# Preserv - Archive Integrity Checker

A desktop application for archivists to maintain digital preservation integrity through cryptographic hashing and automated verification.

![Preserv Logo](https://img.shields.io/badge/Preserv-Archive%20Integrity%20Checker-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- **SHA-256 Hashing**: Hashing for maximum integrity assurance
- **Incremental Checking**: Only re-hash files when size or modification time changes
- **Comprehensive Logging**: Detailed activity logs for preservation documentation
- **Command-line Mode**: Headless operation for automated scheduling
- **Docker Support**: Containerized deployment for consistent environments
- **Export Reports**: Generate HTML and text preservation reports

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/CireWire/preserv.git
   cd Preserv
   ```

2. **Build and run with Docker**:
   ```bash
   # Build the image
   docker build -t preserv .
   
   # Run with GUI (Linux with X11)
   docker run -it --rm \
     -v /tmp/.X11-unix:/tmp/.X11-unix \
     -e DISPLAY=$DISPLAY \
     -v $(pwd)/data:/app/data \
     -v /path/to/your/archive:/archives:ro \
     preserv
   
   # Or use docker-compose
   ARCHIVE_PATH=/path/to/your/archive docker-compose up
   ```

### Local Installation

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

### GUI Mode

Launch the application and use the intuitive interface:

1. **Select Archive Folder**: Click "Browse..." to choose your archive directory
2. **Generate Manifest**: Creates initial SHA-256 hashes for all files
3. **Verify Integrity**: Compares current files against stored hashes
4. **View Results**: Check the activity log for detailed results
5. **Export Reports**: Generate preservation documentation

### Command-line Mode

```bash
# Generate manifest for an archive
python main.py --generate /path/to/archive

# Verify integrity
python main.py --verify /path/to/archive

# Verify and add new files to manifest
python main.py --verify --add-new /path/to/archive

# Show help
python main.py --help
```

### Automated Scheduling

#### Windows Task Scheduler
```batch
# Create a batch file (verify_archive.bat)
python C:\path\to\preserv\main.py --verify C:\path\to\archive

# Schedule to run monthly via Task Scheduler
```

#### Linux/macOS Cron
```bash
# Add to crontab (crontab -e)
0 2 1 * * cd /path/to/preserv && python main.py --verify /path/to/archive >> /var/log/preserv.log 2>&1
```

## File Structure

```
Preserv/
├── main.py                 # Application entry point
├── integrity.py            # Core hashing & verification logic
├── gui.py                  # Tkinter GUI interface
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker container definition
├── docker-compose.yml     # Docker Compose configuration
├── README.md              # This file
└── data/                  # Generated files (created at runtime)
    ├── manifest.csv       # File manifest with hashes
    ├── integrity_log.txt  # Activity log
    └── config.json        # User settings
```

## Configuration

The application automatically creates a `config.json` file with settings:

```json
{
  "archive_path": "/path/to/archive",
  "last_run": "2024-01-15T10:30:00",
  "add_new_files": true,
  "log_level": "INFO"
}
```

## Manifest Format

The `manifest.csv` file contains:

| Column | Description |
|--------|-------------|
| file_path | Relative path from archive root |
| checksum | SHA-256 hash of file content |
| size | File size in bytes |
| modified_time | File modification timestamp |
| date_generated | When hash was calculated |

## Logging

All activities are logged to `integrity_log.txt` with timestamps:

```
2024-01-15 10:30:15 - INFO - Generating manifest for: /path/to/archive
2024-01-15 10:30:16 - INFO - Processing: document1.pdf
2024-01-15 10:30:17 - INFO - Processing: document2.docx
2024-01-15 10:30:18 - INFO - Manifest generation complete: 2 files processed
```

## Docker Configuration

### Environment Variables

- `ARCHIVE_PATH`: Path to archive directory (default: `./archives`)
- `DISPLAY`: X11 display for GUI (default: `:0`)

### Volumes

- `/app/data`: Persistent data storage
- `/archives`: Read-only archive access
- `/tmp/.X11-unix`: X11 socket for GUI (Linux)

### Ports

- `8080`: Reserved for future web interface

## Development

### Prerequisites

- Python 3.8+
- tkinter (usually included with Python)
- Docker (optional)

### Running Tests

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/
```

### Building Docker Image

```bash
# Build image
docker build -t preserv .

# Run with specific archive
docker run -it --rm \
  -v /path/to/archive:/archives:ro \
  -v $(pwd)/data:/app/data \
  preserv
```

## Troubleshooting

### GUI Issues

**Problem**: GUI doesn't start on Linux
**Solution**: Install X11 forwarding or use command-line mode

**Problem**: GUI doesn't start on Windows
**Solution**: Ensure tkinter is installed: `python -m tkinter`

### Docker Issues

**Problem**: GUI doesn't work in Docker
**Solution**: Use command-line mode or configure X11 forwarding

**Problem**: Permission denied accessing archive
**Solution**: Check volume mount permissions and SELinux settings

### Performance Issues

**Problem**: Slow processing of large archives
**Solution**: The application uses incremental checking - only changed files are re-hashed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built for archivists and digital preservation professionals
- Uses SHA-256 cryptographic hashing for maximum integrity
- Inspired by archival best practices and preservation standards

## Support

For issues and questions:
- Check the troubleshooting section
- Review the logs in `integrity_log.txt`
- Open an issue on [GitHub](https://github.com/CireWire/preserv)

---

**Preserv** - Archival integrity checking for today.
Brought to you by The Helix Corp.
