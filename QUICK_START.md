# Preserv Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Option 1: Using Docker (Recommended)

```bash
# Build and run with Docker
docker build -t preserv .
docker run -it --rm -v /path/to/your/archive:/archives:ro preserv
```

### Option 2: Local Installation

1. **Install Python 3.8+** (if not already installed)
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run Preserv**:
   ```bash
   python main.py
   ```

### Option 3: Using Platform Scripts

**Windows**: Double-click `run.bat` or run `.\run.bat`

**Linux/macOS**: Run `./run.sh` or `bash run.sh`

## 🎯 First Steps

1. **Launch the application** - You'll see the Preserv GUI
2. **Select Archive Folder** - Click "Browse..." to choose your archive directory
3. **Generate Manifest** - Click "Generate Manifest" to create initial hashes
4. **Verify Integrity** - Click "Verify Integrity" to check for changes

## 📋 What Preserv Does

- **SHA-256 Hashing**: Creates cryptographically strong hashes of all files
- **Incremental Checking**: Only re-hashes files that have changed
- **Comprehensive Logging**: Records all activities for preservation documentation
- **Change Detection**: Identifies modified, missing, and new files
- **Export Reports**: Generates professional preservation reports

## 🔧 Command Line Usage

```bash
# Generate manifest
python main.py --generate /path/to/archive

# Verify integrity
python main.py --verify /path/to/archive

# Verify and add new files
python main.py --verify --add-new /path/to/archive
```

## 📁 Generated Files

After running Preserv, you'll find these files in your project directory:

- `manifest.csv` - File manifest with SHA-256 hashes
- `integrity_log.txt` - Detailed activity log
- `config.json` - User settings and preferences

## 🧪 Test the Installation

Run the test suite to verify everything works:

```bash
python test_preserv.py
```

## 📖 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check the [troubleshooting section](README.md#troubleshooting) if you encounter issues
- Explore the [Docker configuration](README.md#docker-configuration) for advanced deployment

## 🆘 Need Help?

- Check the logs in `integrity_log.txt`
- Review the [troubleshooting section](README.md#troubleshooting)
- Open an issue on [GitHub](https://github.com/CireWire/preserv)

---

**Preserv** - Professional archival integrity checking for the digital age.
