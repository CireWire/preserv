#!/usr/bin/env python3
"""
Simple run script for Preserv Archive Integrity Checker
"""

import sys
import os
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import tkinter
        import ttkbootstrap
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
        return False

def main():
    """Main run function."""
    print("🚀 Preserv - Archive Integrity Checker")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    print("✅ Dependencies verified")
    
    # Import and run the application
    try:
        from main import main as app_main
        print("✅ Starting Preserv...")
        app_main()
    except KeyboardInterrupt:
        print("\n👋 Preserv stopped by user")
    except Exception as e:
        print(f"❌ Error starting Preserv: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
